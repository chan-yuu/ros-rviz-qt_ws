#指定项目所需的最低 CMake 版本。
cmake_minimum_required(VERSION 3.0.2)
#定义项目的名称
project(progressBar_panel)

#查找并导入外部依赖库
find_package(catkin REQUIRED COMPONENTS
  rviz
  plugin_msg
)

## This plugin includes Qt widgets, so we must include Qt.
## We'll use the version that rviz used so they are compatible.
if(rviz_QT_VERSION VERSION_LESS "5")
  message(STATUS "Using Qt4 based on the rviz_QT_VERSION: ${rviz_QT_VERSION}")
  find_package(Qt4 ${rviz_QT_VERSION} EXACT REQUIRED QtCore QtGui)
  ## pull in all required include dirs, define QT_LIBRARIES, etc.
  include(${QT_USE_FILE})
  macro(qt_wrap_ui)
    qt4_wrap_ui(${ARGN})
  endmacro()
else()
  message(STATUS "Using Qt5 based on the rviz_QT_VERSION: ${rviz_QT_VERSION}")
  find_package(Qt5 ${rviz_QT_VERSION} EXACT REQUIRED Core Widgets)
  ## make target_link_libraries(${QT_LIBRARIES}) pull in all required dependencies
  set(QT_LIBRARIES Qt5::Widgets)
  macro(qt_wrap_ui)
    qt5_wrap_ui(${ARGN})
  endmacro()
endif()

#添加头文件搜索路径，编译器使用这些目录来查找头文件,第一个参数“include”表示包中的include/目录也是路径的一部分。
include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

## I prefer the Qt signals and slots to avoid defining "emit", "slots",
## etc because they can conflict with boost signals, so define QT_NO_KEYWORDS here.
add_definitions(-DQT_NO_KEYWORDS)

## I prefer the Qt signals and slots to avoid defining "emit", "slots",
## etc because they can conflict with boost signals, so define QT_NO_KEYWORDS here.
add_definitions(-DQT_NO_KEYWORDS)

# 设置相关变量
# 自动添加当前目录至路径中
set(CMAKE_INCLUDE_CURRENT_DIR ON)
# 自动生成moc文件,自动运行moc
set(CMAKE_AUTOMOC ON)
# 自动运行uic
#set(CMAKE_AUTOUIC ON)
# 自动运行rcc
set(CMAKE_AUTORCC ON)

qt_wrap_ui(UIC_FILES
  ui/panel_widget.ui
)

#用来匹配指定路径下所有符合通配符条件的文件的命令。具体来说，GLOB_RECURSE 是递归查找目录下的所有文件，file() 命令则可以用来获取文件列表。
file(GLOB_RECURSE SOURCE_CPP
 "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp"
)
file(GLOB_RECURSE SOURCE_H
  "${CMAKE_CURRENT_SOURCE_DIR}/include/${PROJECT_NAME}/*.h"
)

#生成库
add_library(${PROJECT_NAME}
  ${SOURCE_H}
  ${SOURCE_CPP}
  ${UIC_FILES}
)

#在定义消息类型时，编译的库依赖这些动态生成的代码
add_dependencies(${PROJECT_NAME} plugin_msg_generate_messages_cpp)

#设置链接库，需要用到系统或者第三方库函数时候进行配置，第一个参数是可执行文件名，后面依次写入需要链接的库
#设置生成库依赖的库
target_link_libraries(${PROJECT_NAME}
  ${catkin_LIBRARIES}
  ${QT_LIBRARIES}
)
