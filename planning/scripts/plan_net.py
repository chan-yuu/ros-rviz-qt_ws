#!/usr/bin/env python3
#coding=utf-8
'''
采棉机全局规划程序
author： CYUN
description： 根据打点信息规划处需要的路径
'''

from scipy.spatial import cKDTree
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

import numpy as np
import math
import json

import rospy
from car_interfaces.msg import GlobalPathPlanningInterface
from car_interfaces.msg import  NetStartEndPointInterface,GpsImuInterface
from car_interfaces.msg import HmiStartEndPointInterface
from hmi.msg import NodePointsInterface


import time
import matplotlib.patches as patches

import pyproj
import signal
import threading
import matplotlib


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import rospy
from queue import Queue
import sys
import threading
import random
import matplotlib.pyplot as plt
import warnings
from matplotlib import MatplotlibDeprecationWarning
warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning)
from PyQt5.QtGui import QIcon, QPixmap
import matplotlib.pyplot as plt
import threading
import os

import threading
from tqdm import tqdm
import time

import yaml
import std_msgs.msg

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, message="Glyph .* missing from current font")

import os
import sys
# 获取当前脚本文件的所在目录
script_directory = os.path.dirname(os.path.abspath(__file__))
# 图片文件相对于脚本文件的路径
image_relative_path = 'lib'
# 构建图片文件的完整路径
icon_path = os.path.join(script_directory, image_relative_path)
# absolute_path = os.path.abspath(icon_path)

# print(absolute_path)
sys.path.append(icon_path)
from base_function import from_latlon,readMap


Map = []
now_pos_x = 0.0
now_pos_y = 0.0
now_pos_head = 0.0
now_speed = 0.0
q = 0

speed = 0 # hmi 发送来的

roadid = 0
stationid = 0
flag_hmi = 0
q = 1  # 从1开始数
insec_point = []
station_point = []

# 在类外部创建锁对象
class MainWindow(QMainWindow):
    # def __init__(self, x_list, y_list):
    def __init__(self, *args, point_list=None, insec_point=None):
        super().__init__()
        self.setWindowTitle("Path Plot")

        # 获取当前脚本文件的所在目录
        script_directory = os.path.dirname(os.path.abspath(__file__))
        # 图片文件相对于脚本文件的路径
        image_relative_path = "../config/1.png"
        # 构建图片文件的完整路径
        icon_path = os.path.join(script_directory, image_relative_path)

        # 加载图片并设置图标
        # icon_path = "/home/cyun/document/cotton_ws/1.png"  # 将路径替换为你自己的图片路径
        pixmap = QPixmap(icon_path)
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)

        self.canvas = FigureCanvas(plt.figure())
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)
        
        self.tracks = [(args[i], args[i+1]) for i in range(0, len(args), 2)]
        # 创建一个存储轨迹颜色的列表，用于在绘图时选择颜色
        self.colors = ['blue', 'green', 'red', 'orange', 'purple']
        # 创建一个存储轨迹名称的列表，用于在图例中显示轨迹名称
        self.labels = ['Road1', 'Road2', 'Road3', 'Road4', 'Road5']
        # self.x_list = x_list
        # self.y_list = y_list
        self.car_position = (0, 0)  # Initial car position

        # self.point_list_initialized = threading.Event()  # 创建Event对象，表示point_list是否已初始化
        self.point_list = point_list  # 初始化point_list属性
        self.insec_point = insec_point
        # self.point_list_initialized.set()

        self.plot_queue = Queue()
        self.update_thread = threading.Thread(target=self.update_car_position)
        self.update_thread.daemon = True
        self.update_thread.start()

        self.plot_thread = threading.Thread(target=self.plot_car_position)
        self.plot_thread.daemon = True
        self.plot_thread.start()


    def plot_car_position(self):
        # self.point_list_initialized.wait()

        while True:
            tracks, car_position = self.plot_queue.get()
            self.plot(tracks, car_position, self.point_list, self.insec_point)

    def plot(self, tracks, car_position, point_list, insec_point):
        ax = self.canvas.figure.add_subplot(111, label="axes1")
        ax.clear()

        for i, (x_list, y_list) in enumerate(tracks):
            color = self.colors[i % len(self.colors)]
            label = self.labels[i % len(self.labels)]

            ax.plot(x_list, y_list, color=color, label=label)

        ax.scatter(car_position[0], car_position[1], color='red', label='Car Position', marker='o')
        
        # 绘制固定的点
        if point_list:
            points = list(zip(*point_list))
            ax.scatter(points[0], points[1], color='black', label='Station', marker='x')
            # # 在每个点旁边添加点名称
            # for i, (x, y) in enumerate(point_list):
            #     ax.text(x, y, f'S{i+1}', fontsize=12, ha='right', va='bottom')
            # 在每个点旁边添加点名称，使用引线标签
            for i, (x, y) in enumerate(point_list):
                if i<=5:
                    label = f'S{i+1}'
                    ax.annotate(label, (x, y), textcoords="offset points", xytext=(0, -20),color='b', ha='center', fontsize=20)
                if i > 5 and i <= 10:
                    label = f'S{i+1}'
                    ax.annotate(label, (x, y), textcoords="offset points", xytext=(20, 5),color='y', ha='center', fontsize=20)
                if i > 10:
                    label = f'S{i+1}'
                    ax.annotate(label, (x, y), textcoords="offset points", xytext=(0, 10),color='r', ha='center', fontsize=20)
        if insec_point:
            points = list(zip(*insec_point))
            ax.scatter(points[0], points[1], color='black', label='Crossing', marker='s')                                
            for i, (x, y) in enumerate(insec_point):
                label = f'C{i+1}'
                ax.annotate(label, (x, y), textcoords="offset points", xytext=(0, -20),color='black', ha='center', fontsize=20)
            

        ax.set_xlabel('X coordinate')
        ax.set_ylabel('Y coordinate')
        ax.set_title('Road network map')
        ax.legend(fontsize=12, loc='upper right')
        ax.grid(True)
        self.canvas.draw()

    def update_car_position(self):
        global now_pos_x
        global now_pos_y

        while True:
            # now_pos_x = 388624.6230967276
            # now_pos_y =  4963399.26195412
            now_pos_x = now_pos_x
            now_pos_y =  now_pos_y
            # # new_y = random.uniform(min(self.y_list), max(self.y_list))
            self.car_position = (now_pos_x, now_pos_y)

            # new_x = random.uniform(min(self.x_list), max(self.x_list))
            # new_y = random.uniform(min(self.y_list), max(self.y_list))
            # self.car_position = (new_x, new_y)

            self.plot_queue.put((self.tracks, self.car_position))
            threading.Event().wait(1)  # Simulate delay for car position update

def call_back_CurGNSS(msg):
    global content
    global now_pos_x
    global now_pos_y
    global now_pos_head

    try:
        content = json.loads(msg.data)
        now = from_latlon(content['Lat'], content['Lon'])
        # print("now", now)
        now_pos_x = content["UTM_x"]#525913.2#content["UTM_x"]#now[0]#25810.633631279794#now[0]
        now_pos_y = content["UTM_y"]#4316333.7#content["UTM_y"]#now[1]#16495.487913915887#now[1]
        now_pos_head = content['Head']

    except:
        print('content error')
        content = content

def hmi_start_end_point_data_callback(msg):
    #在函数里面global
    global roadid
    global stationid
    global flag_hmi #hmi 发送成功，恒=1

    roadid = msg.roadid
    stationid = msg.stationid
    flag_hmi = msg.flag


def node_point_data_callback(msg):
    global insec_point
    global station_point
    #NOTE 红路灯路口的站点信息

    station_point = msg.stationpoint
    insec_point = msg.incppoint
    station_point = insec_point

    insec_point = [526075.9223862926, 4316161.714272074]
    station_point = insec_point


def euclidean_distance(x1,y1,x2,y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_k(x1,y1,x2,y2):
    k = (y2 - y1) / (x2 - x1)
    return k


# 计算航向的list，输入为路径x_list和y_list
def calculate_head(x,y):
    # 计算每个点的航向角
    headings = []
    head_list = []
    for i in range(len(x)):
        if i == 0:
            # 第一个点，使用后一个点计算航向角
            dx = x[i + 1] - x[i]
            dy = y[i + 1] - y[i]
        elif i == len(x) - 1:
            # 最后一个点，使用前一个点计算航向角
            dx = x[i] - x[i - 1]
            dy = y[i] - y[i - 1]
        else:
            # 中间点，使用前后两个点计算航向角
            dx = x[i + 1] - x[i]
            dy = y[i + 1] - y[i]

        # 计算航向角
        heading = np.arctan2(dy, dx) # radian [rad]
        headings_angle = math.degrees(math.atan2(dy, dx))#np.arctan2(dy, dx)*180/np.pi  # angle [°]

        headings.append(heading)
        head_list.append(headings_angle)
    # return headings,headings_angles
    return head_list



def run_progress_bar(total_iterations):
    progress_bar = tqdm(total=total_iterations, desc="路径显示中，请稍等", unit="iteration")
    for _ in range(total_iterations):
        progress_bar.update(1)
        time.sleep(0.02)
    progress_bar.close()



def cal_road(roadid):
    # 定义地图文件路径的前缀
    path_prefix = "../../hmi/config/"

    # 创建包含100个映射关系的字典
    map_files = {roadid: "{}{}.map".format(path_prefix, roadid) for roadid in range(1, 1001)}

    if roadid in map_files:
        # 获取当前脚本文件的所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建地图文件的完整路径
        mapfile = os.path.join(script_dir, map_files[roadid])

        # x_list, y_list, head_list = readMap(mapfile)
        # head_list_cal = calculate_head(x_list, y_list)
        # vel_list = [1 for _ in x_list]
        # curva_list = [0 for _ in x_list]
        # print(mapfile)
    else:
        print("Invalid roadid: {}".format(roadid))
    return mapfile


def main():
    
    global routedata
    global now_pos_x
    global now_pos_y
    global now_pos_head
    global now_speed
    global q

    # global turning_distance
    # global result_list
    global speed

    global now_pos_head
    global yaml_data
    global roadid
    global stationid
    global flag_hmi #hmi 发送成功，恒=1
    global insec_point
    global station_point


    signal.signal(signal.SIGINT, quit)

    rospy.init_node('global_path_planning')
    rospy.logwarn("plan start success")
    rospy.logwarn("**********需要先打开gps**********")
    rospy.logwarn("**********等待交互界面下发指令**********")
    rospy.logwarn("**********请选择道路id**********")
    rospy.logwarn("**********请选择导入路口/站点*************")


    pub = rospy.Publisher("global_path_planning_data", GlobalPathPlanningInterface, queue_size = 10)

    rospy.Subscriber("hmi_start_end_point_data", HmiStartEndPointInterface, hmi_start_end_point_data_callback)
    rospy.Subscriber("node_points_data", NodePointsInterface, node_point_data_callback)
    rospy.Subscriber('/ztbus/location', std_msgs.msg.String, call_back_CurGNSS)

    roadid = 3
    insec_point = [526075.9223862926, 4316161.714272074]
    station_point = insec_point
    flag_hmi = 1

    x_list = []
    y_list = []
    head_list = []
    curva_list = []
    routedata = []

    rate = rospy.Rate(10)
    index = 0  # 路径数据索引
    q = 1  # 从1开始数
    segment_id = 0  # 数据片段ID
    flag = 0  # 全局路径只算一次
    flag_visual = 0
    plot_flag = 1

    while not rospy.is_shutdown():
        # roadid = 820
        # flag_hmi = 1
        start_time = time.time()
        # 计算路径，只需要执行一次  # BUG 注意标志位不能写到循环里面
        if flag == 0 and roadid != 0 and flag_hmi != 0 and len(insec_point) != 0 :
            mapfile = cal_road(roadid)
            x_list, y_list, head_list,vel_list = readMap(mapfile)
            # print(head_values)
            head_list_cal = calculate_head(x_list,y_list)
            # print(head_list)
            # vel_list = [1 for _ in x_list]
            curva_list = [0 for _ in x_list]
            # print(mapfile)

            plt.plot(x_list, y_list, marker='o', linestyle='', color='b', label="Map")
            if plot_flag == 0: # 是否进行可视化，0-不可视化 1-可视化道路
                plt.xlabel('x')
                plt.ylabel('y')
                plt.title('Visualization of Position Points')
                plt.legend()
                plt.show()

            for i in range(len(x_list)):
                routedata.append(x_list[i])
                routedata.append(y_list[i])
                routedata.append(head_list[i])
                routedata.append(vel_list[i])
                routedata.append(curva_list[i])
            # print("curva_list", curva_list)
            routedata = [str(num) for num in routedata]    
            path_len = len(routedata)  # 整个路径的点数
            if path_len < 1500:
                divisor = 300
            elif 1500 <= path_len < 5000:
                divisor = 500
            elif 5000 <= path_len < 15000:
                divisor = 1000
            elif 15000 <= path_len < 25000:
                divisor = 3000
            else:
                divisor = 5000

            print("*"*66)            
            # print("总规划点数",path_len,"每次发送的点数",divisor,"规划的横向距离", yaml_data['dis_C'], "地图更新时间", yaml_data['time_update'])

            # divisor = 1000    # 最好是自适应  # 一次发送的点数 由于不一定是它的整数倍，所以最后那一次发送能发多少就多少
            # 39*5次
            quotient = path_len // divisor  # 商的整数部分
            remainder = path_len % divisor  # 余数
            if remainder == 0:
                dia = quotient  # 能整除，返回商
            else:
                dia = quotient + 1  # 不能整除，返回商+1  dia 一共要发送的次数

            print("-"*68) 
            def show_progress(total_iterations):
                print("----------")
                print("*****正在计算路径*****")
                for i in range(1, total_iterations + 1):
                    print(f"{i}/{total_iterations}", end="", flush=True)
                    time.sleep(0.008)
                    print("\b" * (len(str(i)) + len(str(total_iterations)) + 1), end="", flush=True)
            total_iterations = 100
            show_progress(total_iterations) 
            print("正在发送路径......")
            for i in range(len(x_list)):
                x_list[i] -= 527072.047921458
                y_list[i] -= 4315751.418146324
            # print(len(x_list))
            flag = 1
        print(111)
        if len(x_list) !=0 :
            msg = GlobalPathPlanningInterface()
            # print("**************",head_list[-1])
            msg.Global_Path_Segment_Index = q  # q=1
            msg.len_path = path_len
            # msg.endpoint = [x_list[-1],y_list[-1]]
            msg.endpoint = insec_point[-2:]

            msg.x_list = x_list
            msg.y_list = y_list

            # # print(msg.endpoint)
            # if q == 1 :
            #     time.sleep(0.1)   # 只有第一次需要sleep 不然就发送不好 
            # msg.routedata = routedata

            # if index + divisor < len(routedata):   # 每次发divisor个
            #     msg.routedata = routedata[index:index+divisor]
            #     index += divisor
            
            # else:
            #     msg.routedata = routedata[index:]

            end_time = time.time()
            process_time = end_time - start_time
            msg.process_time = process_time  

            pub.publish(msg)
            rate.sleep()
            print("sent success!")            
            
            if q > dia and flag_visual == 1: #flag_visual,规划程序不再绘图 0-绘制 1-不绘制
                # script_dir = os.path.dirname(os.path.abspath(__file__))
                # 图片文件相对于脚本文件的路径
                # image_relative_path = "../../hmi/config/2.map"

                # # 构建图片文件的完整路径
                # mapfile = os.path.join(script_dir, image_relative_path)
                mapfiles = [mapfile]#, '/home/nvidia/cotton_ws_panda/src/map/scripts/newmap2.map']#'/home/cyun/cotton_ws/src/map/scripts/newmap1.map', '/home/cyun/cotton_ws/src/map/scripts/newmap2.map']
                x_list, y_list, x_list1, y_list1, x_list2, y_list2 = [], [], [], [], [], []
                
                colors = ['r', 'g', 'b', 'c', 'm', 'y']  # 自定义颜色列表，可以根据需要扩展
                for i, mapfile in enumerate(mapfiles):
                    x_values, y_values,head_values,vel_list = readMap(mapfile)
                    color = colors[i % len(colors)]  # 使用循环获取颜色
                    plt.plot(x_values, y_values, marker='o', linestyle='', color=color, label=mapfile)

                    if i == 0:
                        x_list.extend(x_values)
                        y_list.extend(y_values)

                    elif i == 1:
                        x_list1.extend(x_values)
                        y_list1.extend(y_values)

                    elif i == 2:
                        x_list2.append(x_values)
                        y_list2.append(y_values)

                        x_list2new = []
                        y_list2new = []
                        for sublist in x_list2:
                            for item in sublist:
                                x_list2new.append(item)

                        for sublist in y_list2:
                            for item in sublist:
                                y_list2new.append(item)

                # flag = 1
                if flag_visual == 0: #q > dia and flag_visual == 0: #flag_visual,规划程序不再绘图
                    total_iterations = 100
                    progress_thread = threading.Thread(target=run_progress_bar, args=(total_iterations,))
                    progress_thread.start()
                    progress_thread.join()
                    print("-"*20)
                    print("路径处理完毕！")
                    app = QApplication(sys.argv)
                    # 站点
                    station_list = []
                    for i in range(0, len(station_point), 2):
                        point = [station_point[i], station_point[i+1]]
                        station_list.append(point)
                    # 路口
                    insec_list = []
                    for i in range(0, len(insec_point), 2):
                        point = [insec_point[i], insec_point[i+1]]
                        insec_list.append(point)
                    # print(insec_list)
                    # print(now_pos_x)
                    main_window = MainWindow(x_list, y_list, point_list = station_list, insec_point= insec_list)
                    main_window.show()
                    sys.exit(app.exec_())


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
    rospy.spin()


