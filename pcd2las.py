# -*- coding: utf-8 -*-
import numpy as np
import __builtin__
from __builtin__ import property
import os
import pcl
import pcl.pcl_visualization
import liblas
from liblas import file
from liblas import header
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext

file_paths_read = []
file_paths_write = []

def all_filepath(rootdir):
    for root, dirs, files in os.walk(rootdir):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.split(".")[-1] == "las":
                file_paths_read.append(file_path)
            if file_path.split(".")[-1] == "pcd":
                file_paths_write.append(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            all_filepath(dir_path)
    return file_paths_read,file_paths_write

def read():
    for path in file_paths_read:
        f = liblas.file.File(path,mode= 'r')
        las_header_read = f.header
        print('主版本号：' + str(las_header_read.major_version))
        print('副版本号：' + str(las_header_read.minor_version))
        print('最小值：%f,%f,%f' % (las_header_read.min[0],las_header_read.min[1],las_header_read.min[2]))
        print('最大值：%f,%f,%f' % (las_header_read.max[0], las_header_read.max[1], las_header_read.max[2]))
        print('比例：%f,%f,%f' % (las_header_read.scale[0], las_header_read.scale[1], las_header_read.scale[2]))
        print('偏移量：%f,%f,%f' % (las_header_read.offset[0], las_header_read.offset[1], las_header_read.offset[2]))
        print('点云数量:%d' % (las_header_read.point_records_count))
def write():
    for path in file_paths_write:
        print path
        cloud = pcl.load_XYZI(path)
        # viewer = pcl.pcl_visualization.CloudViewing()
        # viewer.ShowColorCloud(cloud, b'cloud')
        las_header_write = header.Header()
        las_header_write.scale = [0.0001, 0.0001, 0.0001]
        las_header_write.offset = [0,0,0]
        las_header_write.dataformat_id = 1
        las_header_write.minor_version = 2
        las_path = path.split(".")[0] + ".las"
        x_col = []
        y_col = []
        z_col = []
        for i in range(0, cloud.size):
            if int(cloud[i][3]) > 5 and int(cloud[i][3]) < 15:
                x_col.append(cloud[i][0])
                y_col.append(cloud[i][1])
                z_col.append(cloud[i][2])
        x_col.sort()
        y_col.sort()
        z_col.sort()
        # print [x_col[0],y_col[0],z_col[0]]
        las_header_write.min = [x_col[0],y_col[0],z_col[0]]
        las_header_write.max = [x_col[-1],y_col[-1],z_col[-1]]
        fw = file.File(las_path, mode="w", header=las_header_write)
        pt = liblas.point.Point()
        for i in range(0, cloud.size):
            if int(cloud[i][3]) > 5 and int(cloud[i][3]) < 15:
                pt.x = round(cloud[i][0] * 10000, 0)
                pt.y = round(cloud[i][1] * 10000, 0)
                pt.z = round(cloud[i][2] * 10000, 0)
                pt.intensity = int(cloud[i][3])
            fw.write(pt)
        print('主版本号：' + str(las_header_write.major_version))
        print('副版本号：' + str(las_header_write.minor_version))
        print('最小值：%f,%f,%f' % (las_header_write.min[0], las_header_write.min[1], las_header_write.min[2]))
        print('最大值：%f,%f,%f' % (las_header_write.max[0], las_header_write.max[1], las_header_write.max[2]))
        print('比例：%f,%f,%f' % (las_header_write.scale[0], las_header_write.scale[1], las_header_write.scale[2]))
        print('偏移量：%f,%f,%f' % (las_header_write.offset[0], las_header_write.offset[1], las_header_write.offset[2]))
        print('点云数量:%d' % (las_header_write.point_records_count))
        fw.close()


if __name__ == "__main__":
    file_paths = all_filepath('/media/sf_E/jingjintang_highway/pointcloud_rgb')
    write()
    print 'write over'
    # read()
    # print 'read over'
