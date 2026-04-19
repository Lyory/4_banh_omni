import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # 1. Khai báo các đường dẫn
    pkg_share = get_package_share_directory('robot')
    
    # Lấy đường dẫn tới package turtlebot3_gazebo
    pkg_tb3_gazebo = get_package_share_directory('turtlebot3_gazebo')
    
    # Chọn map Waffle
    world_path = os.path.join(pkg_tb3_gazebo, 'worlds', 'turtlebot3_world.world')
    
    # Duong dan den workspace_models
    workspace_models_path = os.path.join(pkg_share, '..')

    # 2. Xử lý file URDF
    xacro_file = os.path.join(pkg_share, 'urdf', 'robot.urdf')
    robot_desc = xacro.process_file(xacro_file).toxml()

    # 3. Thiết lập biến môi trường GAZEBO_MODEL_PATH
    set_gazebo_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=[
            os.environ.get('GAZEBO_MODEL_PATH', ''), 
            ':', workspace_models_path,
            ':', os.path.join(pkg_tb3_gazebo, 'models')
        ]
    )

    # 4. Node Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}]
    )

    # 5. Mở Gazebo và Nạp Map
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': world_path}.items()
    )

    # 6. Node Spawn Robot
    # Chỉnh tọa độ spawn 
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description', 
            '-entity', 'my_robot',
            '-x', '-2.0', '-y', '-0.5', '-z', '0.01'
        ],
        output='screen'
    )

   # Khai báo đường dẫn tới file cấu hình RViz của bạn
    rviz_config_path = os.path.join(pkg_share, 'rviz', 'robot.rviz')

    # Node RViz2 
    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        # Thêm arguments '-d' để nạp file cấu hình
        arguments=['-d', rviz_config_path], 
        parameters=[{'use_sim_time': True}]
    )

    # 8. Controller Spawners
    load_joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    load_joint_position_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_position_controller"],
    )

    return LaunchDescription([
        set_gazebo_model_path,
        robot_state_publisher,
        gazebo,
        spawn_entity,
        rviz2,
        load_joint_state_broadcaster,
        load_joint_position_controller,
    ])