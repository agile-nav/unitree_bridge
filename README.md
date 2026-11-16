# unitree_bridge

## 中文

### 功能包简介
`unitree_bridge` 是一个 ROS 2 功能包，用于将 Unitree 机器人的控制接口和 ROS 2 生态连接起来。它主要负责把 ROS 2 的命令消息转换为 Unitree 机器人支持的运动控制请求，同时读取无线手柄状态并转换为运动使能信号。

该功能包当前包含以下节点：

- `cmd_vel_bridge`
  - 订阅 `/cmd_vel`
  - 将线速度和角速度转换成 Unitree 的运动请求
  - 仅在 `START` 键触发后才允许运动
  - 在 `B` 键按下或 `/cmd_vel` 超时后发送停止命令

- `wireless_controller`
  - 订阅 `/wirelesscontroller`
  - 解析无线手柄按键状态
  - 发布 `/motion_enabled` 布尔消息
  - 通过 `START` 和 `B` 键控制机器人是否允许运动

- `image_bridge`
  - 使用 GStreamer 读取视频流
  - 将图像以压缩图像的形式发布到 ROS 2 主题
  - 适合接入 Unitree 机器人相机/网络视频流

### 依赖说明
该功能包依赖以下 ROS 2 / 机器人相关组件：

- `rclpy`
- `geometry_msgs`
- `std_msgs`
- `sensor_msgs`（图像桥接模块）
- `cv_bridge`
- `unitree_api`
- `unitree_go`

另外，图像桥接模块依赖 OpenCV 和 GStreamer，以便读取并压缩视频流。

### 构建方式
在 ROS 2 工作空间根目录执行：

```bash
cd /home/jiewang/nav_release_ws
colcon build --packages-select unitree_bridge
source install/setup.bash
```

### 启动方式
启动功能包中的默认节点：

```bash
ros2 launch unitree_bridge unitree_bridge.launch.py
```

默认启动的两个节点：

- `cmd_vel_bridge`
- `wireless_controller`

### 关键主题

| 主题 | 方向 | 说明 |
| --- | --- | --- |
| `/cmd_vel` | 订阅 | ROS 2 的速度控制命令 |
| `/api/sport/request` | 发布 | 发送给 Unitree 的运动 API 请求 |
| `/wirelesscontroller` | 订阅 | Unitree 无线手柄状态 |
| `/motion_enabled` | 发布 | 运动是否允许执行的布尔信号 |
| `/camera/image/compressed` | 发布 | 压缩图像流（如果启用图像桥接） |

### 使用说明
1. 确认 Unitree 相关 API 和底层驱动已经正常运行。
2. 启动功能包：
   ```bash
   ros2 launch unitree_bridge unitree_bridge.launch.py
   ```
3. 通过 ROS 2 发布 `/cmd_vel` 速度命令。
4. 先按手柄 `START` 键，机器人才会接受运动命令。
5. 按手柄 `B` 键可立即停止运动。
6. 若 `/cmd_vel` 长时间未更新，节点会自动发送停止命令，防止机器人持续运动。

### 注意事项
- `cmd_vel_bridge` 只在明确启用运动后才会发送控制命令。
- `wireless_controller` 会过滤掉短暂的重复按键抖动，并将按键事件按边沿处理。
- `image_bridge` 默认使用 GStreamer pipeline，需确认相机网络和参数配置正确。

---

## English

### Package Overview
`unitree_bridge` is a ROS 2 package that connects the Unitree robot interface to the ROS 2 ecosystem. It translates ROS 2 control messages into Unitree motion requests and reads wireless controller state to enable or disable motion safely.

The package currently includes the following nodes:

- `cmd_vel_bridge`
  - subscribes to `/cmd_vel`
  - forwards linear and angular velocity into Unitree motion requests
  - allows motion only after the `START` button is pressed
  - sends a stop command when `B` is pressed or when `/cmd_vel` times out

- `wireless_controller`
  - subscribes to `/wirelesscontroller`
  - decodes button states from the wireless controller
  - publishes `/motion_enabled` as a boolean value
  - enables or disables robot motion via `START` and `B`

- `image_bridge`
  - reads a video stream through GStreamer
  - publishes the stream as compressed ROS 2 image messages
  - suitable for camera or network video inputs from a Unitree robot

### Dependencies
This package relies on the following ROS 2 and robot-related components:

- `rclpy`
- `geometry_msgs`
- `std_msgs`
- `sensor_msgs` (for image bridge)
- `cv_bridge`
- `unitree_api`
- `unitree_go`

The image bridge also depends on OpenCV and GStreamer for capture and JPEG compression.

### Build Instructions
From the ROS 2 workspace root, run:

```bash
cd /home/jiewang/nav_release_ws
colcon build --packages-select unitree_bridge
source install/setup.bash
```

### Launch Instructions
Start the default launch file:

```bash
ros2 launch unitree_bridge unitree_bridge.launch.py
```

The default launch includes:

- `cmd_vel_bridge`
- `wireless_controller`

### Key Topics

| Topic | Direction | Description |
| --- | --- | --- |
| `/cmd_vel` | subscribe | command velocity from ROS 2 |
| `/api/sport/request` | publish | Unitree sport request message |
| `/wirelesscontroller` | subscribe | Unitree wireless controller state |
| `/motion_enabled` | publish | whether motion is currently enabled |
| `/camera/image/compressed` | publish | compressed image stream from the camera bridge |

### Usage
1. Make sure the Unitree robot API and underlying drivers are available.
2. Launch the package:
   ```bash
   ros2 launch unitree_bridge unitree_bridge.launch.py
   ```
3. Publish velocity commands on `/cmd_vel` from ROS 2.
4. Press the controller `START` button before motion will be accepted.
5. Press `B` to stop motion immediately.
6. If `/cmd_vel` stops updating for a while, the node will automatically send a stop request.

### Notes
- `cmd_vel_bridge` only emits motion commands when motion is explicitly enabled.
- `wireless_controller` filters repeated key events and handles button changes at the edge level.
- `image_bridge` depends on a valid GStreamer pipeline and network/camera configuration.

---

## 结论 / Summary
`unitree_bridge` 主要用于将 ROS 2 控制命令和 Unitree 机器人的运动接口进行桥接，适合在移动机器人、编队与遥控控制场景中使用。它提供了运动控制、安全使能、按键识别和视频流桥接等基础能力，是连接 ROS 2 与 Unitree 机器人系统的重要中间层。

`unitree_bridge` is a ROS 2 bridge package that connects ROS 2 control commands with the Unitree robot motion interface. It is useful in mobile robot control, teleoperation, and robot integration scenarios, providing motion forwarding, safety gating, wireless controller handling, and video-stream bridging.
