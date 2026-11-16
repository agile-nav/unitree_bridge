"""Launch the velocity bridge and wireless-controller reader."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """Start unitree bridge nodes."""
    return LaunchDescription([
        Node(
            package='unitree_bridge',
            executable='cmd_vel_bridge',
            name='cmd_vel_bridge',
            output='screen',
        ),
        Node(
            package='unitree_bridge',
            executable='wireless_controller',
            name='wireless_controller',
            output='screen',
        ),
    ])
