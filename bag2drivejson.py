#!/usr/bin/python2
# encoding: utf-8
import json
import math
import shapefile
import rosbag
import tkinter as tk
from tkinter import filedialog
import string

def cal_road():
    center = {"centerx":centerx, "centery":centery}
    leftB = []
    rightB = []
    road_feature = []
    i = 0
    while i <= len(center["centerx"]) - 1:
        j = 0
        leftBorder_pointSets = []
        leftBorder = {}
        while j <= len(center["centerx"][i]) - 1:
            leftBorder_point = {}
            leftBorder_point["x"] = center["centerx"][i][j]
            leftBorder_point["y"] = center["centery"][i][j]
            leftBorder_point["z"] = 0
            leftBorder_pointSets.append(leftBorder_point)
            j += 1
        leftBorder["virtual"] = "FALSE"
        leftBorder["type"] = "broken"
        leftBorder["color"] = "white"
        leftBorder["pointSet"] = leftBorder_pointSets
        leftB.append(leftBorder)
        i += 1
    i = 0
    while i <= len(center["centerx"]) - 1:
        j = 0
        rightBorder_pointSets = []
        rightBorder = {}
        while j <= len(center["centerx"][i]) - 1:
            rightBorder_point = {}
            rightBorder_point["x"] = center["centerx"][i][j]
            rightBorder_point["y"] = center["centery"][i][j]
            rightBorder_point["z"] = 0
            rightBorder_pointSets.append(rightBorder_point)
            j += 1
        rightBorder["virtual"] = "FALSE"
        rightBorder["type"] = "broken"
        rightBorder["color"] = "white"
        rightBorder["pointSet"] = rightBorder_pointSets
        rightB.append(rightBorder)
        i += 1
    i=0
    while i <= len(centerx)-1:
        n=0
        centerLine=[]
        sum_length = 0
        while n<=len(centerx[i])-1:
            if n == 0:
                x = centerx[i][0]
                y = centery[i][0]
                # print x,y
                x_next = centerx[i][1]
                y_next = centery[i][1]
                heading = math.atan2(y_next - y, x_next - x)
                length = 0
            elif 0 < n < len(centerx[i])-1:
                x = centerx[i][n]
                y = centery[i][n]
                x_pre = centerx[i][n - 1]
                y_pre = centery[i][n - 1]
                x_next = centerx[i][n + 1]
                y_next = centery[i][n + 1]
                heading1 = math.atan2(y - y_pre, x - x_pre)
                heading2 = math.atan2(y_next - y, x_next - x)
                heading = (heading1 + heading2) / 2
                length = math.sqrt((y - y_pre) ** 2 + (x - x_pre) ** 2)
            elif n == len(centerx[i])-1:
                x = centerx[i][n]
                y = centery[i][n]
                x_pre = centerx[i][n - 1]
                y_pre = centery[i][n - 1]
                heading = math.atan2(y - y_pre, x - x_pre)
                length = math.sqrt((y - y_pre) ** 2 + (x - x_pre) ** 2)
            sum_length += length
            centerLine_points = {}
            centerLine_points["id"] = str(1000 + i) + "_" + str(i) + "_" + str(n)
            centerLine_points["heading"] = heading
            centerLine_points["x"] = centerx[i][n]
            centerLine_points["y"] = centery[i][n]
            centerLine_points["z"] = 0
            centerLine_points["lenIntegral"] = sum_length
            centerLine.append(centerLine_points)
            n+=1
        lane_feature = {}
        lanes_feature = []
        lanesection_feature = []
        lane_section = {}
        section_feature = {}
        lane_feature["id"] = 0
        lane_feature["uid"] = str(1000 + i) + "_" + str(0)
        lane_feature["type"] = "driving"
        # lane_feature["change"] = 0
        lane_feature["turnType"] = "noTurn"
        lane_feature["speedLimit"] = 20
        if len(centerx) == 1:
            lane_feature["link"] = {"predecessors": [], "successors": []}
            lane_feature["laneOverlapGroup"] = []
        elif len(centerx) == 2:
            if i == 0:
                successors = [{"id": str(1001) + "_" + str(0)}]
                lane_feature["link"] = {"predecessors": [],"successors": successors}
                lane_feature["laneOverlapGroup"] = []
            else:
                predecessors = [{"id": str(1000) + "_" + str(0)}]
                lane_feature["link"] = {"predecessors": predecessors, "successors": []}
                lane_feature["laneOverlapGroup"] = []
        elif len(centerx) > 2:
            if i == 0:
                successors = [{"id": str(1001 + i) + "_" + str(0)}]
                lane_feature["link"] = {"predecessors": [], "successors": successors}
                lane_feature["laneOverlapGroup"] = []
            elif i > 0 and i < len(centerx) - 1:
                predecessors = [{"id": str(999 + i) + "_" + str(0)}]
                successors = [{"id": str(1001 + i) + "_" + str(0)}]
                lane_feature["link"] = {"predecessors": predecessors, "successors": successors}
                lane_feature["laneOverlapGroup"] = []
            else:
                predecessors = [{"id": str(999 + i) + "_" + str(0)}]
                lane_feature["link"] = {"predecessors": predecessors, "successors": []}
                lane_feature["laneOverlapGroup"] = []
        lane_feature["centerLine"] = centerLine
        lane_feature["leftBorder"] = leftB[i]
        lane_feature["rightBorder"] = rightB[i]
        lane_feature["lenIntegrals"] = []
        lanes_feature.append(lane_feature)
        lane_section["boundaries"] = []
        lane_section["lanes"] = lanes_feature
        lanesection_feature.append(lane_section)
        section_feature["id"] = 1000 + i
        section_feature["junction"] = -1
        if len(centerx) == 1:
            section_feature["link"] = {"predecessors": [], "successors": []}
        elif len(centerx) == 2:
            if i == 0:
                successors = [{"elementType": "road", "elementId": str(1001), "contactPoint": "end"}]
                section_feature["link"] = {"predecessors": [], "successors": successors}
            else:
                predecessors = [{"elementType": "road", "elementId": str(1000), "contactPoint": "start"}]
                section_feature["link"] = {"predecessors": predecessors, "successors": []}
        elif len(centerx) > 2:
            if i == 0:
                successors = [{"elementType": "road", "elementId": str(1001 + i), "contactPoint": "end"}]
                section_feature["link"] = {"predecessors": [], "successors": successors}
            elif i > 0 and i < len(centerx) - 1:
                predecessors = [{"elementType": "road", "elementId": str(999 + i), "contactPoint": "start"}]
                successors = [{"elementType": "road", "elementId": str(1001 + i), "contactPoint": "end"}]
                section_feature["link"] = {"predecessors": predecessors, "successors": successors}
            else:
                predecessors = [{"elementType": "road", "elementId": str(999 + i), "contactPoint": "start"}]
                section_feature["link"] = {"predecessors": predecessors, "successors": []}
        section_feature["laneSections"] = lanesection_feature
        road_feature.append(section_feature)
        i += 1
    return road_feature


def select_bag():
    global numberOfFiles
    global bag_name
    global output_bagname
    global filename_path_bag
    global centerx
    global centery
    bag_name = []
    drivejson = {}
    filename_path_bag = filedialog.askopenfilenames(title='请选择bag文件', filetypes=[('bag', '*.bag'), ('All Files', '*')],
                                                    initialdir='/media/sf_desktop')
    numberOfFiles = str(len(filename_path_bag))
    bag_count = 0
    for bagFile in filename_path_bag:
        centerx = []
        centery = []
        centerLinex = []
        centerLiney = []
        bag = rosbag.Bag(bagFile)
        bagName = bag.filename
        bag_name.append(bagName.rstrip('.bag').split('/')[-1])
        count_1 = 0
        count_2 = 0
        for subtopic, msg, t in bag.read_messages('/trunk_info/gnss_ins'):
            msgString = str(msg)
            msgList = string.split(msgString, '\n')
            for nameValuePair in msgList:
                splitPair = string.split(nameValuePair, ':')
                if splitPair[0] == "utm_east" or splitPair[0] == "    x":
                    if count_1 == 0 or count_1 % 10 == 0:
                        centerLinex.append(float(splitPair[1]))
                    count_1 += 1
                elif splitPair[0] == "utm_north" or splitPair[0] == "    y":
                    if count_2 == 0 or count_2 % 10 == 0:
                        centerLiney.append(float(splitPair[1]))
                    count_2 += 1
            if len(centerLinex) == len(centerLiney) == 1001:
                centerx.append(centerLinex)
                centery.append(centerLiney)
                centerLinex = [centerLinex[-1]]
                centerLiney = [centerLiney[-1]]
            elif len(centerLinex) == len(centerLiney) < 1000:
                continue
        centerx.append(centerLinex)
        centery.append(centerLiney)
        # print len(centerx),centerx,len(centery),centery
        road_feature = cal_road()
        drivejson["header"] = {"revMajor": "", "revMinor": "", "name": "", "version": "", "date": "", "north": 0,
                               "south": 0, "east": 0, "west": 0,
                               "vendor": "Trunk", "geoReference": "+proj=longlat+ellps=WSG84+datum=WGS84+no_defs"}
        drivejson["roads"] = road_feature
        drivejson["junctions"] = []
        # print drivejson
        with open("/media/sf_D/ros_python/beifen/" + str(bag_name[bag_count]) + ".json", "w+") as drivejsonfile:
            json.dump(drivejson, drivejsonfile)
            print str(bag_count + 1) + ":" + str(bag_name[bag_count]) + " transform over!"
        bag_count += 1

if __name__=="__main__":
    window = tk.Tk()
    window.title('bag2json Tool')
    window.geometry('500x300')
    button1 = tk.Button(window, text='选择bag', font=('Arial', 12), width=10, height=1, command=select_bag)
    button1.pack()
    window.mainloop()