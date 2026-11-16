"""Publish a GStreamer video stream to a ROS 2 image topic."""

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage, Image


class GStreamerImageBridge(Node):
    """Open a GStreamer pipeline and publish frames as ROS2 images."""

    def __init__(self):
        super().__init__('gstreamer_image_bridge')
        self.declare_parameter('gstreamer_pipeline',
            'udpsrc address=230.1.1.1 port=1720 multicast-iface=eth0 '
            '! application/x-rtp, media=video, encoding-name=H264 '
            '! rtph264depay ! h264parse ! avdec_h264 ! videoconvert '
            '! video/x-raw,width=1280,height=720,format=BGR ! appsink drop=1')
        self.declare_parameter('image_topic', '/camera/image')
        self.declare_parameter('compressed_image_topic', '/camera/image/compressed')
        self.declare_parameter('frame_id', 'base')
        self.declare_parameter('jpeg_quality', 70)

        pipeline = self.get_parameter('gstreamer_pipeline').value
        topic = self.get_parameter('image_topic').value
        compressed_topic = self.get_parameter('compressed_image_topic').value
        frame_id = self.get_parameter('frame_id').value
        jpeg_quality = int(self.get_parameter('jpeg_quality').value)

        self._bridge = CvBridge()
        self._publisher = self.create_publisher(Image, topic, 10)
        self._compressed_publisher = self.create_publisher(CompressedImage, compressed_topic, 10)
        self._jpeg_quality = max(1, min(100, jpeg_quality))
        self._cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
        if not self._cap.isOpened():
            self.get_logger().error(f'Failed to open GStreamer pipeline: {pipeline}')
            raise RuntimeError('Unable to open GStreamer pipeline')

        self._frame_id = frame_id
        self._publish_period = 1.0 / 15.0
        self._timer = self.create_timer(self._publish_period, self._publish_frame)
        self.get_logger().info(f'Publishing GStreamer stream to {topic} at 15 Hz')

    def _publish_frame(self):
        ret, frame = self._cap.read()
        if not ret or frame is None:
            self.get_logger().warning('No frame received from GStreamer pipeline')
            return

        stamp = self.get_clock().now().to_msg()

        image_msg = self._bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        image_msg.header.stamp = stamp
        image_msg.header.frame_id = self._frame_id
        # self._publisher.publish(image_msg)

        success, encoded = cv2.imencode(
            '.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, self._jpeg_quality])
        if not success:
            self.get_logger().warning('Failed to compress frame before publishing')
            return

        compressed_msg = CompressedImage()
        compressed_msg.header.stamp = stamp
        compressed_msg.header.frame_id = self._frame_id
        compressed_msg.format = 'jpeg'
        compressed_msg.data = encoded.tobytes()
        self._compressed_publisher.publish(compressed_msg)

    def destroy_node(self):
        if hasattr(self, '_cap') and self._cap is not None:
            self._cap.release()
        return super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = GStreamerImageBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()