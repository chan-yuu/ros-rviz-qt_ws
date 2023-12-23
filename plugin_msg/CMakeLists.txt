#指定项目所需的最低 CMake 版本。
cmake_minimum_required(VERSION 3.0.2)
#定义项目的名称
project(plugin_msg)

#查找并导入外部依赖库。
find_package(catkin REQUIRED COMPONENTS
  std_msgs
  message_generation #增加message编译时依赖模块到（message_generation）
)

#增加自定义的msg文件
add_message_files(
  FILES
  ProgressBarMsg.msg
)

#生成msg需要依赖的消息以及服务
generate_messages(
  DEPENDENCIES
  std_msgs
)

#这用于指定包的依赖关系，由依赖于这个包的其他软件包使用。
catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES custom_msg
  CATKIN_DEPENDS message_runtime #增加message运行时依赖模块message_runtime
#  DEPENDS system_lib
)
