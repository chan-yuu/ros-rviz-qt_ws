# float64  timestamp  #时间戳
# int8 Perception_Fault # 1）毫米波雷达CAN通信故障，2）雷达自身检测故障、3）相机通信故障、4）视觉检测故障、5）组合惯导CAN通信故障、
#                       # 6）组合惯导搜星数量不足，7）GPS-RTK非固定解，8）棉箱是否装满传感故障。从高字节到低字节，每个bit设置为1表示有故障，0表示没有故障。 
# int8  Actuator_Fault # 1）转向线控系统故障、2）制动线控系统故障、3）油门线控故障、4）采头线控驱动故障、5）采头高度反馈故障、6）棉箱升降线控故障、# 7）棉箱倾斜线控故障、8）卸棉线控驱动故障。从高字节到低字节，每个bit设置为1表示有故障，0表示没有故障。
# int8 VCU_DCU_Fault # 底盘与驾驶域控故障：1）VCU通信故障、2）电池电压故障、3）VCU其他故障、
#                    # 4）公网通信故障。从高字节到低字节，每个bit设置为1表示有故障，0表示没有故障。
# float32  process_time    # 进程处理时间
# int8 brake_faultCode
# int8 vcu_faultCode2
# int8 Steering_faultCode3


# int8 vcu_CfaultCode
# int8 Steering_faultCode
# int8 Gps_Cfault
# int8 search_stars_unenough
# int8 Gps_state
# int8 radar_state
# int8 radar_error

# time 9.1
bool Gps_state_fault 				#惯导通讯故障 0：异常；1：正常
bool drive_by_wire_fault 			#线控油门故障
bool cotton_box_driver_fault 			#棉箱驱动故障
bool cotton_box_full_moniter_fault		#棉箱满载监控故障
bool search_stars_unenough_fault 		#搜星不足故障 0：异常；1：正常
bool brake_fault 				# 线控刹车故障 0：异常；1：正常
bool Steering_fault	 			#线控转向故障 0：异常；1：正常
bool vision_detect_fault			#视觉检测故障
bool radar_state_fault 			#毫米波雷达状态 0：异常；1：正常
bool head_driver_fault				#采头驱动故障
bool vcu_communication_fault			#vcu通信故障
bool public_communication_fault		#公网通信故障


int32  system_state                		#惯导模式（2-true；其余-false）
int32  satellite_status              		#卫星状态（0-false  4-true  其余-黄）
bool  gps_communication_fault 		#惯导通信故障
bool   radar_communication_fault   		#雷达通信故障