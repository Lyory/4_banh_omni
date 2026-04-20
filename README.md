# Mô phỏng robot 4 bánh Omni trong ROS2 trên Ubuntu Humble 22.04 

Dự án mô phỏng một robot di động đa hướng (4-wheel Omni-directional) tích hợp cơ cấu tay máy nâng hạ bằng vít me (2-DOF) trong môi trường ROS 2 (Humble) và Gazebo.

## Tính năng nổi bật
* **Khung gầm Đa hướng (Omni-drive):** Sử dụng 4 bánh xe cấu hình X-drive, cho phép di chuyển tịnh tiến đa hướng và xoay tại chỗ (sử dụng plugin `gazebo_ros_planar_move`).
* **Cơ cấu Vít me:** Tay máy 2 bậc tự do (1 khớp xoay, 1 khớp tịnh tiến) được điều khiển thông qua `ros2_control` (JointPositionController).
* **Hệ thống Cảm biến:** Tích hợp Lidar 2D (phạm vi 12m), Camera RGB và cảm biến IMU, xuất dữ liệu trực tiếp lên RViz.
* **Tự động hóa:** Cung cấp Node Python cho phép nhập tọa độ điều khiển cơ cấu vít me theo chu trình 

---

## Yêu cầu hệ thống (Prerequisites)

Robot được mô phỏng trên:
* **OS:** Ubuntu 22.04 LTS
* **ROS 2:** Humble Hawksbill
* **Gazebo:** Gazebo Classic (phiên bản đi kèm ROS 2 Humble)

### Các thư viện cần thiết 
Mở Terminal và chạy lệnh sau để cài đặt các package cần thiết cho dự án:


`sudo apt update`

`sudo apt install ros-humble-gazebo-ros-pkgs \ros-humble-ros2-control \ ros-humble-gazebo-ros2-control \ ros-humble-teleop-twist-keyboard \ ros-humble-xacro \ ros-humble-rviz-imu-plugin`


Sau khi clone Repository về, cần tạo workplace để có thể chạy chương trình: 
Chạy lệnh:

`mkdir -p ~/my_robot/src
cd ~/my_robot/src`

Giải nén file, sau đó vào đường dẫn `/src/` tạo 1 folder có tên là robot sau đó tiến hành copy các file trong thư mục đã giải nén (config, launch, meshes,...) vào trong folder robot.

Trỏ vào workplace sau đó tiến hành colcon build dự án, source lại môi trường trước khi chạy file launch.

`cd ~/my_robot
colcon build --packages-select robot
source install/setup.bash`

Mở cùng lúc 3 terminal và tiến hành source môi trường cho cả 3:

**Chạy file launch:**
`ros2 launch robot display.launch.py`

**Điều khiển robot di chuyển:**
`ros2 run teleop_twist_keyboard teleop_twist_keyboard`

**Điều khiển tay máy robot sử dụng câu lệnh:**
`ros2 run robot arm_controller.py`

Nhập lệnh dạng ' Góc xoay , Độ cao '
