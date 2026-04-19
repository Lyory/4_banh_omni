#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import time

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('arm_sequential_controller')
    
    publisher = node.create_publisher(
        Float64MultiArray, 
        '/joint_position_controller/commands', 
        10)
    
    # trang thai hien tai cua robot
    current_angle = 0.0
    current_height = 0.0


    try:
        while rclpy.ok():
            print("Giới hạn (Xoay: -3.14 đến 3.14 rad, Nâng -0.05 đến 0.07m)")
            user_input = input("Nhập lệnh (Xoay Nâng): ")
            
            if user_input.lower() == 'q':
                break
                
            parts = user_input.split()
            if len(parts) != 2:
                print("Error\n")
                continue
                
            try:
                target_angle = float(parts[0])
                target_height = float(parts[1])
                # Xoay
                print(f"Đang xoay đến góc {target_angle} rad...")
                msg = Float64MultiArray()
                msg.data = [target_angle, current_height] # Gửi góc mới, độ cao cũ
                publisher.publish(msg)
                
                # stop
                time.sleep(2.0) 
                # Điều khiển tịnh tiến
                print(f"Đang tịnh tiến đến độ cao {target_height} m...")
                msg.data = [target_angle, target_height] # Gửi góc MỚI, độ cao MỚI
                publisher.publish(msg)
                
                # Tạm dừng 2 giây chờ nâng xong
                time.sleep(2.0)
                
                print("Finished\n")
                
               # Cập nhật vị trí
                current_angle = target_angle
                current_height = target_height
                
            except ValueError:
                print("Error\n")

    except KeyboardInterrupt:
        node.get_logger().info('shutting down arm controller node...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()