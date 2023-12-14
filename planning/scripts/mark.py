#!/usr/bin/env python3
#coding=utf-8
# import rospy
# from visualization_msgs.msg import Marker
# from geometry_msgs.msg import Point

# rospy.init_node("vehicle_marker_publisher")
# marker_pub = rospy.Publisher("vehicle_marker", Marker, queue_size=10)

# def publish_marker(position):
#     marker = Marker()
#     marker.header.frame_id = "map"  # 指定坐标系
#     marker.type = Marker.ARROW  # 类型为箭头
#     marker.action = Marker.ADD
#     marker.pose.position = position
#     marker.scale.x = 2.0  # 箭头的长度
#     marker.scale.y = 0.5  # 箭头的宽度
#     marker.scale.z = 0.5  # 箭头的高度
#     marker.color.a = 1.0
#     marker.color.r = 1.0
#     marker.color.g = 0.0
#     marker.color.b = 0.0

#     marker_pub.publish(marker)

# if __name__ == "__main__":
#     # 假设车辆的位置是 (1, 2, 0)
#     vehicle_position = Point()
#     vehicle_position.x = 1.0
#     vehicle_position.y = 2.0
#     vehicle_position.z = 0.0
#     while not rospy.is_shutdown():

#         publish_marker(vehicle_position)


# import rospy
# from visualization_msgs.msg import Marker
# from geometry_msgs.msg import Point, Quaternion

# rospy.init_node("vehicle_marker_publisher")
# marker_pub = rospy.Publisher("vehicle_marker", Marker, queue_size=10)

# def publish_marker(position):
#     marker = Marker()
#     marker.header.frame_id = "map"  # 指定坐标系
#     marker.type = Marker.CUBE  # 类型为立方体
#     marker.action = Marker.ADD
#     marker.pose.position = position
#     marker.scale.x = 0.5  # 立方体的长度
#     marker.scale.y = 0.5  # 立方体的宽度
#     marker.scale.z = 0.5  # 立方体的高度
#     marker.color.a = 1.0
#     marker.color.r = 1.0
#     marker.color.g = 0.0
#     marker.color.b = 0.0

#     marker_pub.publish(marker)

# if __name__ == "__main__":
#     # 假设车辆的位置是 (1, 2, 0)，姿态为单位四元数
#     vehicle_position = Point()
#     vehicle_position.x = 0
#     vehicle_position.y = 0
#     vehicle_position.z = 0.0

#     vehicle_orientation = Quaternion()
#     vehicle_orientation.x = 0.0
#     vehicle_orientation.y = 0.0
#     vehicle_orientation.z = 0.0
#     vehicle_orientation.w = 1.0
#     while not rospy.is_shutdown():

#         publish_marker(vehicle_position)
#         print("pub ok")



# import rospy
# from geometry_msgs.msg import Point, Quaternion
# from visualization_msgs.msg import Marker

# def publish_marker(position):
#     marker = Marker()
#     marker.header.frame_id = "map"  # 指定坐标系
#     marker.type = Marker.CUBE  # 类型为立方体
#     marker.action = Marker.ADD
#     marker.pose.position = position
#     marker.scale.x = 0.5  # 立方体的长度
#     marker.scale.y = 0.5  # 立方体的宽度
#     marker.scale.z = 0.5  # 立方体的高度
#     marker.color.a = 1.0
#     marker.color.r = 1.0
#     marker.color.g = 0.0
#     marker.color.b = 0.0

#     marker_pub.publish(marker)  # 发布标记消息

# if __name__ == "__main__":
#     rospy.init_node("vehicle_position_publisher")  # 初始化节点
#     marker_pub = rospy.Publisher("vehicle_marker", Marker, queue_size=10)  # 创建发布器

#     x_list = [0.0, -0.020003830082714558, -0.03977670427411795, -0.05815447121858597, -0.07466500904411077, -0.0925592971034348, -0.10664395184721798, -0.12727083603385836, -0.15047023666556925, -0.1684636998688802, -0.18610443058423698, -0.20907843916211277, -0.22599001799244434, -0.24560933839529753, -0.2634167189244181, -0.28321477270219475, -0.3006322644650936, -0.32632120267953724, -0.3484522959915921, -0.373700481839478, -0.4046931806951761, -0.4329629868734628, -0.4582506255246699, -0.4845929219154641, -0.518355182139203, -0.5513713187538087, -0.5770913822343573, -0.6002357975812629, -0.6310352910077199, -0.6677167352754623, -0.693903828272596, -0.7219919990748167]
#     y_list = [0.0, -0.5300979670137167, -1.070207079872489, -1.6062520276755095, -2.1299448711797595, -2.6920422948896885, -3.2137415083125234, -3.747774476185441, -4.3008802477270365, -4.806086822412908, -5.330288467928767, -5.858232658356428, -6.362739720381796, -6.914540369063616, -7.431069943122566, -7.947456534951925, -8.44738438539207, -8.967047133482993, -9.495070547796786, -10.068201684392989, -10.700872661545873, -11.242224974557757, -11.767032138071954, -12.270955670624971, -12.823169962503016, -13.342720253393054, -13.882340404205024, -14.38513102568686, -14.891183882020414, -15.400845781899989, -15.910380659624934, -16.41887891944498]

#     rate = rospy.Rate(10)  # 设置发布频率为10Hz

#     for i in range(len(x_list)):
#         vehicle_position = Point()
#         vehicle_position.x = x_list[i]
#         vehicle_position.y = y_list[i]
#         vehicle_position.z = 0.0

#         publish_marker(vehicle_position)  # 发布车辆位置标记
#         print("Published vehicle position marker.")

#         rate.sleep()


import rospy,math
from geometry_msgs.msg import Point, Quaternion
from visualization_msgs.msg import Marker
from tf.transformations import quaternion_from_euler

def publish_marker(position, heading):
    marker = Marker()
    marker.header.frame_id = "map"  # 指定坐标系
    marker.type = Marker.CUBE  # 类型为立方体
    marker.action = Marker.ADD
    marker.pose.position = position
    
    # 设置姿态
    quaternion = quaternion_from_euler(0, 0, heading)
    marker.pose.orientation.x = quaternion[0]
    marker.pose.orientation.y = quaternion[1]
    marker.pose.orientation.z = quaternion[2]
    marker.pose.orientation.w = quaternion[3]

    marker.scale.x = 1  # 立方体的长度
    marker.scale.y = 0.4  # 立方体的宽度
    marker.scale.z = 0.4  # 立方体的高度
    marker.color.a = 1.0
    marker.color.r = 1.0
    marker.color.g = 0.0
    marker.color.b = 0.0

    marker_pub.publish(marker)  # 发布标记消息
def convert_deg_to_rad(heading_deg):
    # 将角度转换为弧度
    heading_rad = math.radians(heading_deg)
    
    # 将弧度限制在 π 到 2π 的范围内
    if heading_rad < math.pi:
        heading_rad += math.pi
    elif heading_rad >= 2 * math.pi:
        heading_rad -= math.pi
        
    return heading_rad

if __name__ == "__main__":
    rospy.init_node("vehicle_position_publisher")  # 初始化节点
    marker_pub = rospy.Publisher("vehicle_marker", Marker, queue_size=10)  # 创建发布器

    # 假设车辆位置和航向数据
    x_list = [0.0, -0.020003830082714558, -0.03977670427411795, -0.05815447121858597, -0.07466500904411077, -0.0925592971034348, -0.10664395184721798, -0.12727083603385836, -0.15047023666556925, -0.1684636998688802, -0.18610443058423698, -0.20907843916211277, -0.22599001799244434, -0.24560933839529753, -0.2634167189244181, -0.28321477270219475, -0.3006322644650936, -0.32632120267953724, -0.3484522959915921, -0.373700481839478, -0.4046931806951761, -0.4329629868734628, -0.4582506255246699, -0.4845929219154641, -0.518355182139203, -0.5513713187538087, -0.5770913822343573, -0.6002357975812629, -0.6310352910077199, -0.6677167352754623, -0.693903828272596, -0.7219919990748167]
    y_list = [0.0, -0.5300979670137167, -1.070207079872489, -1.6062520276755095, -2.1299448711797595, -2.6920422948896885, -3.2137415083125234, -3.747774476185441, -4.3008802477270365, -4.806086822412908, -5.330288467928767, -5.858232658356428, -6.362739720381796, -6.914540369063616, -7.431069943122566, -7.947456534951925, -8.44738438539207, -8.967047133482993, -9.495070547796786, -10.068201684392989, -10.700872661545873, -11.242224974557757, -11.767032138071954, -12.270955670624971, -12.823169962503016, -13.342720253393054, -13.882340404205024, -14.38513102568686, -14.891183882020414, -15.400845781899989, -15.910380659624934, -16.41887891944498]
    heading_list = [0.0, 0.5300979670137167, 1.070207079872489, 1.6062520276755095, 2.1299448711797595, 2.6920422948896885, 3.137415083125234, 1.747774476185441, 1.3008802477270365, 1.806086822412908, 1.330288467928767, 1.858232658356428, 1.362739720381796, 1.914540369063616, 1.431069943122566, 1.947456534951925, 1.44738438539207, 1.967047133482993, 1.495070547796786, 1.068201684392989, 1.700872661545873, 1.242224974557757,1.767032138071954, 1.270955670624971, 1.823169962503016, 1.342720253393054, 1.882340404205024, 1.38513102568686, 1.891183882020414, 1.400845781899989, 1.910380659624934, 1.41887891944498]
    heading_list = []*len(x_list)
    heading_list = [-91.639420237, -91.644014679, -91.656882717, -91.673809578, -91.684739468, -91.715631598, -91.718989781, -91.737396187, -91.763918393, -91.780636552, -91.781375784, -91.804165259, -91.817652754, -91.843980325, -91.861138288, -91.889428669, -91.928986231, -91.980167855, -92.015523417, -92.063746175, -92.136384727, -92.195615073, -92.23863206, -92.275751482, -92.332983395, -92.38729585, -92.452238863, -92.499274543, -92.547569335, -92.613044959, -92.653767865, -92.710789363]
    for i in range(len(heading_list)):
        heading_list[i]=convert_deg_to_rad(heading_list[i])
    # heading_list = [math.pi/2]*len(x_list)
    rate = rospy.Rate(10)  # 设置发布频率为10Hz

    for i in range(len(x_list)):
        vehicle_position = Point()
        vehicle_position.x = x_list[i]
        vehicle_position.y = y_list[i]
        vehicle_position.z = 0.0

        heading = heading_list[i]

        publish_marker(vehicle_position, heading)  # 发布车辆位置标记
        print("Published vehicle position marker.")

        rate.sleep()