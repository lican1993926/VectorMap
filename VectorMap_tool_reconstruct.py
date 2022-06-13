#!/usr/bin/python2
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import rosbag, csv
import string
import shapefile
import codecs
import math
# import sympy
import time
import json
# import pyperclip
from rosbag import Bag
from json import dumps
from osgeo import ogr
from fnmatch import fnmatchcase

import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
import os


class Basic(object):
    def __init__(self):
        self.ID_toobig = []
        self.laneType_error = []
        self.lane_error = []
        self.single_lane_error = []
        self.laneSpeed_error = []
        self.single_lane_error = []
        self.turnType_error = []
        self.topo_error = []
        self.ID_repeat = []
        self.ID_subrepeat = []
        self.direction_opposite_single = []
        self.direction_opposite_all = []
        self.featureDirection_starterror = []
        self.featureDirection_enderror = []
        self.section_allopposite_start = []
        self.section_allopposite_end = []
        self.feature_angle_error = []


class Table(object):
    def __init__(self):
        self.coordinates_table = []
        self.sectionID_table = []
        self.laneType_table = []
        self.laneSpeed_table = []
        self.turnType_table = []
        self.startx_table = []
        self.starty_table = []
        self.endx_table = []
        self.endy_table = []


def select_shapefile():
    global buffer
    global filename_path_shapefile
    global tag
    buffer = []
    filename_path_shapefile = filedialog.askopenfilename(title='请选择shp文件',filetypes=[('shp', '*.shp'), ('All Files', '*')],initialdir='/project')
    inputfilename_path = filename_path_shapefile.replace('\\', '\\\\')
    reader = shapefile.Reader(inputfilename_path)
    field_names = []
    fields = reader.fields[1:]
    for field in fields:
        field_names.append(field[0])
        if field[0] == "type" or field[0] == "junctionID":
            tag = 0  # 掩膜
    if len(field_names) == 6 and "virtual" in field_names:
        tag = 1  # 老L4
    elif len(field_names) == 6 and "bridge" in field_names:
        tag = 2  # 宁波港
    elif len(field_names) == 7 and "lineType" in field_names:
        tag = 3  # CL4
    elif len(field_names) == 8 and "topo" in field_names:
        tag = 4  # 新L4
    elif len(field_names) == 4 and "sectionID" in field_names:
        tag = 5  # 五洲
    if tag == 0 or tag == 5:
        shape_records = reader.shapeRecords()
        for sr in shape_records:
            record = sr.record
            atr = dict(zip(field_names, record))
            geom = sr.shape.__geo_interface__
            buffer.append(dict(type="Feature", geometry=geom, properties=atr))
    elif tag == 1:
        shape_records = reader.shapeRecords()
        for sr in shape_records:
            record = sr.record
            record_first = []
            for value in record:
                if value == "\x00" * 50:
                    new_value = value.rstrip("\x00")
                    record_first.append(new_value)
                elif value == None:
                    new_value = 0
                    record_first.append(new_value)
                elif value != None:
                    record_first.append(value)
            atr = dict(zip(field_names, record_first))
            atr_first = dict(sectionID=atr["sectionID"], laneType=atr["laneType"], laneSpeed=atr["laneSpeed"],
                             turnType=atr["turnType"], change=atr["change"], virtual=atr['virtual'])
            geom = sr.shape.__geo_interface__
            buffer.append(dict(type="Feature", geometry=geom, properties=atr_first))
    elif tag == 2:
        shape_records = reader.shapeRecords()
        for sr in shape_records:
            record = sr.record
            record_second = []
            for value in record:
                if value == "\x00" * 50:
                    new_value = value.rstrip("\x00")
                    record_second.append(new_value)
                elif value == None:
                    new_value = 0
                    record_second.append(new_value)
                elif value != None:
                    record_second.append(value)
            atr = dict(zip(field_names, record_second))
            atr_second = dict(sectionID=atr["sectionID"], laneType=atr["laneType"], laneSpeed=atr["laneSpeed"],
                              turnType=atr["turnType"], direction=atr["direction"], bridge=atr["bridge"])
            geom = sr.shape.__geo_interface__
            buffer.append(dict(type="Feature", geometry=geom, properties=atr_second))
    elif tag == 3:
        shape_records = reader.shapeRecords()
        for sr in shape_records:
            record = sr.record
            record_second = []
            for value in record:
                if value == "\x00" * 50:
                    new_value = value.rstrip("\x00")
                    record_second.append(new_value)
                elif value == None:
                    new_value = 0
                    record_second.append(new_value)
                elif value != None:
                    record_second.append(value)
            atr = dict(zip(field_names, record_second))
            atr_second = dict(sectionID=atr["sectionID"], laneType=atr["laneType"], laneSpeed=atr["laneSpeed"],
                              turnType=atr["turnType"], lineType=atr["lineType"], roadType=atr["roadType"],
                              change=atr["change"])
            geom = sr.shape.__geo_interface__
            buffer.append(dict(type="Feature", geometry=geom, properties=atr_second))
    elif tag == 4:
        shape_records = reader.shapeRecords()
        for sr in shape_records:
            record = sr.record
            record_second = []
            for value in record:
                if value == "\x00" * 50:
                    new_value = value.rstrip("\x00")
                    record_second.append(new_value)
                elif value == None:
                    new_value = 0
                    record_second.append(new_value)
                elif value != None:
                    record_second.append(value)
            atr = dict(zip(field_names, record_second))
            atr_second = dict(sectionID=atr["sectionID"], laneType=atr["laneType"], laneSpeed=atr["laneSpeed"],
                              turnType=atr["turnType"], lineType=atr["lineType"], roadType=atr["roadType"],
                              change=atr["change"], topo=atr["topo"])
            geom = sr.shape.__geo_interface__
            buffer.append(dict(type="Feature", geometry=geom, properties=atr_second))
    text.insert(tk.INSERT, "\n")
    text.insert("end", "生成的要素数为" + str(len(buffer)) + "个")
    text.insert(tk.INSERT, "\n")


def save_geojson():
    file = filedialog.asksaveasfilename(title='请输入保存文件名',initialfile=(filename_path_shapefile.split('/')[-1]).split('.')[:-1],
                                        filetypes=[('All Files', '*')])
    suffix = suffix_input.get()
    if suffix:
        geojson = codecs.open(file.split(".")[0] + "." + suffix, "w", encoding="utf-8")
    if not suffix:
        geojson = codecs.open(file.split(".")[0] + ".json", "w", encoding="utf-8")
    geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
    text.insert("end", "Path:" + str(filename_path_shapefile).lstrip("/"))
    text.insert(tk.INSERT, "\n")
    text.insert(tk.INSERT, "\n")
    text.insert("end", "格式转换完毕！")
    text.insert(tk.INSERT, "\n")
    text.insert("end", "-" * 226)


def shapefile_check(buffer):
    global ID_repeat
    global ID_subrepeat
    global feature_collection
    global direction_opposite_single
    global direction_opposite_all
    global feature_collection_flip
    global direction_opposite_single_all
    global direction_opposite_all_all
    global single_lane_error
    global distance_threshold_down
    global distance_threshold_up
    if distance_entry_down.get():
        distance_threshold_down = int(distance_entry_down.get())
    else:
        distance_threshold_down = 6
    if distance_entry_up.get():
        distance_threshold_up = int(distance_entry_up.get())
    else:
        distance_threshold_up = 8.5
    if direction_entry.get():
        direction_threshold = int(direction_entry.get())
    else:
        direction_threshold = 0
    if angle_entry.get():
        angle_threshold = float(angle_entry.get()) * 0.017453293
    else:
        angle_threshold = 0.0523599
    check = check_input.get()
    Error = Basic()
    Porperty = Table()
    direction_opposite_single_all = []
    direction_opposite_all_all = []
    new_feature_collection = []
    feature_collection = []
    feature_collection_flip = []
    single_lane_error = []
    for lane in buffer:
        geometry = lane['geometry']
        sectionID = lane["properties"]["sectionID"]
        laneSpeed = lane["properties"]["laneSpeed"]
        turnType = lane["properties"]["turnType"]
        laneType = lane["properties"]["laneType"]
        if sectionID not in [h for h in range(0, 100001)]:
            Error.ID_toobig.append(sectionID)
        Porperty.sectionID_table.append(sectionID)
        if tag == 2 or tag == 5:  # 港口
            if laneType not in [f for f in range(0, 23)]:
                Error.laneType_error.append(sectionID)
        elif tag == 1 or tag == 3 or tag == 4:  # 高速
            if laneType not in [p for p in range(0, 14)]:
                Error.laneType_error.append(sectionID)
        Porperty.laneType_table.append(laneType)
        if laneSpeed == 0:
            Error.lane_error.append(sectionID)
        elif laneSpeed not in [d for d in range(1, 121)]:
            Error.laneSpeed_error.append(sectionID)
        Porperty.laneSpeed_table.append(laneSpeed)
        if turnType not in [s for s in range(0, 3)]:
            Error.turnType_error.append(sectionID)
        Porperty.turnType_table.append(turnType)
        start = list(lane["geometry"]["coordinates"][0])
        sub_start = list(lane["geometry"]["coordinates"][1])
        end = list(lane["geometry"]["coordinates"][-1])
        sub_end = list(lane["geometry"]["coordinates"][-2])
        try:
            middle = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]
        except Exception:
            continue
        corrdinates = lane["geometry"]["coordinates"]
        Porperty.coordinates_table.append(corrdinates)
        Porperty.startx_table.append(start[0])
        Porperty.endx_table.append(end[0])
        feature = [start, end, sub_start, sub_end, middle, sectionID, laneType, laneSpeed, turnType, geometry]
        feature_collection.append(feature)
    feature_collection.sort(key=lambda feature_collection: feature_collection[-5], reverse=True)
    m = 0
    while m <= len(feature_collection) - 1:
        p = m + 1
        while p <= len(feature_collection) - 1:
            if abs(feature_collection[m][0][0] - feature_collection[p][0][0]) <= 0.01 and abs(
                    feature_collection[m][0][1] - feature_collection[p][0][1]) <= 0.01:
                if {"x": round(feature_collection[m][0][0], 6),
                    "y": round(feature_collection[m][0][1], 6)} not in Error.featureDirection_starterror:
                    Error.featureDirection_starterror.append(
                        {"x": round(feature_collection[m][0][0], 6), "y": round(feature_collection[m][0][1], 6)})
            p += 1
        m += 1
    m = 0
    while m <= len(feature_collection) - 1:
        p = m + 1
        while p <= len(feature_collection) - 1:
            if abs(feature_collection[m][1][0] - feature_collection[p][1][0]) <= 0.01 and abs(
                    feature_collection[m][1][1] - feature_collection[p][1][1]) <= 0.01:
                if {"x": round(feature_collection[m][1][0], 6),
                    "y": round(feature_collection[m][1][1], 6)} not in Error.featureDirection_enderror:
                    Error.featureDirection_enderror.append(
                        {"x": round(feature_collection[m][1][0], 6), "y": round(feature_collection[m][1][1], 6)})
            p += 1
        m += 1
    json1 = codecs.open("json1" + ".json", "w", encoding="gb2312")
    json1.write(dumps(Error.featureDirection_starterror, indent=2) + "\n")
    json2 = codecs.open("json2" + ".json", "w", encoding="gb2312")
    json2.write(dumps(Error.featureDirection_enderror, indent=2) + "\n")
    k = 0
    while k < len(feature_collection) - 1:
        if feature_collection[k][-5] == feature_collection[k + 1][-5]:
            new_feature_collection.append(feature_collection[k])
            if k == len(feature_collection) - 2:
                new_feature_collection.append(feature_collection[k + 1])
                new_feature_collection.sort(
                    key=lambda new_feature_collection: new_feature_collection[4][direction_threshold], reverse=True)
        else:
            if k == len(feature_collection) - 2:
                new_feature_collection = []
                new_feature_collection.append(feature_collection[k + 1])
                Error.single_lane_error.append(feature_collection[k + 1][-5])
                single_lane_error.append(feature_collection[k + 1][-5])
            else:
                new_feature_collection.append(feature_collection[k])
                new_feature_collection.sort(
                    key=lambda new_feature_collection: new_feature_collection[4][direction_threshold], reverse=True)
            if len(new_feature_collection) != 1:
                feature_collection_flip.append(new_feature_collection)
            else:
                Error.single_lane_error.append(new_feature_collection[0][-5])
                single_lane_error.append(new_feature_collection[0])
            new_feature_collection = []
        k += 1
    progressbar['value'] = 0
    progressbar['maximum'] = len(feature_collection_flip) - 1
    angle_1 = 0
    angle_2 = 0
    i = 0
    while i <= len(feature_collection_flip) - 1:
        Error.section_allopposite_start = []
        Error.section_allopposite_end = []
        n = 0
        while n <= len(feature_collection_flip[i]) - 1:
            Error.section_allopposite_start.append({"x": round(feature_collection_flip[i][n][0][0], 6),
                                                    "y": round(feature_collection_flip[i][n][0][1], 6)})
            Error.section_allopposite_end.append({"x": round(feature_collection_flip[i][n][1][0], 6),
                                                  "y": round(feature_collection_flip[i][n][1][1], 6)})
            n += 1
        inter_start = [ss for ss in Error.section_allopposite_start if ss in Error.featureDirection_starterror]
        inter_end = [zz for zz in Error.section_allopposite_end if zz in Error.featureDirection_enderror]
        j = 0
        while j <= len(feature_collection_flip[i]) - 1:
            tag_1 = 0
            tag_2 = 0
            if j < len(feature_collection_flip[i]) - 1:
                feature_frontstart_x = feature_collection_flip[i][j][0][0]
                feature_frontstart_y = feature_collection_flip[i][j][0][1]
                feature_frontend_x = feature_collection_flip[i][j][1][0]
                feature_frontend_y = feature_collection_flip[i][j][1][1]
                feature_nextstart_x = feature_collection_flip[i][j + 1][0][0]
                feature_nextstart_y = feature_collection_flip[i][j + 1][0][1]
                feature_nextend_x = feature_collection_flip[i][j + 1][1][0]
                feature_nextend_y = feature_collection_flip[i][j + 1][1][1]
                feature_frontmiddle_x = feature_collection_flip[i][j][4][0]
                feature_frontmiddle_y = feature_collection_flip[i][j][4][1]
                feature_nextmiddle_x = feature_collection_flip[i][j + 1][4][0]
                feature_nextmiddle_y = feature_collection_flip[i][j + 1][4][1]
            else:
                feature_frontstart_x = feature_collection_flip[i][j - 1][0][0]
                feature_frontstart_y = feature_collection_flip[i][j - 1][0][1]
                feature_frontend_x = feature_collection_flip[i][j - 1][1][0]
                feature_frontend_y = feature_collection_flip[i][j - 1][1][1]
                feature_nextstart_x = feature_collection_flip[i][j][0][0]
                feature_nextstart_y = feature_collection_flip[i][j][0][1]
                feature_nextend_x = feature_collection_flip[i][j][1][0]
                feature_nextend_y = feature_collection_flip[i][j][1][1]
                feature_frontmiddle_x = feature_collection_flip[i][j - 1][4][0]
                feature_frontmiddle_y = feature_collection_flip[i][j - 1][4][1]
                feature_nextmiddle_x = feature_collection_flip[i][j][4][0]
                feature_nextmiddle_y = feature_collection_flip[i][j][4][1]
            if feature_frontstart_x - feature_frontend_x != 0:
                slope_front = (feature_frontstart_y - feature_frontend_y) / (feature_frontstart_x - feature_frontend_x)
            else:
                slope_front = 0
            if feature_nextstart_x - feature_nextend_x != 0:
                slope_next = (feature_nextstart_y - feature_nextend_y) / (feature_nextstart_x - feature_nextend_x)
            else:
                slope_next = 0
            slope_diff = abs(slope_front - slope_next)
            line_length_front = math.sqrt(
                (feature_frontstart_x - feature_frontend_x) ** 2 + (feature_frontstart_y - feature_frontend_y) ** 2)
            line_length_next = math.sqrt(
                (feature_nextstart_x - feature_nextend_x) ** 2 + (feature_nextstart_y - feature_nextend_y) ** 2)
            line_length_diff = abs(line_length_front - line_length_next)
            section_judge = feature_collection_flip[i][j][-5]
            vector1x_diff = feature_collection_flip[i][j][2][0] - feature_collection_flip[i][j][0][0]
            vector1y_diff = feature_collection_flip[i][j][2][1] - feature_collection_flip[i][j][0][1]
            vector2x_diff = feature_collection_flip[i][j][1][0] - feature_collection_flip[i][j][3][0]
            vector2y_diff = feature_collection_flip[i][j][1][1] - feature_collection_flip[i][j][3][1]
            vector_start = [vector1x_diff, vector1y_diff]
            vector_end = [vector2x_diff, vector2y_diff]
            if math.sqrt((feature_frontmiddle_x - feature_nextmiddle_x) ** 2 + (
                    feature_frontmiddle_y - feature_nextmiddle_y) ** 2) >= distance_threshold_down \
                    and slope_diff >= 0.0001:
                Error.ID_repeat.append(section_judge)
                if math.sqrt((feature_frontmiddle_x - feature_nextmiddle_x) ** 2 + (
                        feature_frontmiddle_y - feature_nextmiddle_y) ** 2) <= distance_threshold_up:
                    Error.ID_subrepeat.append(section_judge)
            elif math.sqrt((feature_frontmiddle_x - feature_nextmiddle_x) ** 2 + (
                    feature_frontmiddle_y - feature_nextmiddle_y) ** 2) >= distance_threshold_down \
                    and slope_diff <= 0.0001 and line_length_diff >= 0.0001:
                Error.ID_repeat.append(section_judge)
                if math.sqrt((feature_frontstart_x - feature_nextstart_x) ** 2 + (
                        feature_frontstart_y - feature_nextstart_y) ** 2) <= distance_threshold_up:
                    Error.ID_subrepeat.append(section_judge)
            for start_error in Error.featureDirection_starterror:
                for end_error in Error.featureDirection_enderror:
                    if math.sqrt((feature_frontmiddle_x - feature_nextmiddle_x) ** 2 + (
                            feature_frontmiddle_y - feature_nextmiddle_y) ** 2) <= distance_threshold_down:
                        if inter_start == Error.section_allopposite_start and inter_end == Error.section_allopposite_end and math.sqrt(
                                (feature_frontstart_x - feature_nextstart_x) ** 2 + (
                                        feature_frontstart_y - feature_nextstart_y) ** 2) <= distance_threshold_down and \
                                math.sqrt((feature_frontend_x - feature_nextend_x) ** 2 + (
                                        feature_frontend_y - feature_nextend_y) ** 2) <= distance_threshold_down:
                            # print str(section_judge) + "_" + str(j), start_error, end_error
                            if round(feature_collection_flip[i][j][0][0], 6) == start_error["x"] and round(
                                    feature_collection_flip[i][j][1][0], 6) == end_error["x"] \
                                    and round(feature_collection_flip[i][j][0][1], 6) == start_error["y"] and round(
                                feature_collection_flip[i][j][1][1], 6) == end_error["y"]:
                                if j == len(feature_collection_flip[i]) - 2:
                                    section_judge = feature_collection_flip[i][j + 1][-5]
                                for filt in feature_collection_flip:
                                    for filt_feature in filt:
                                        vectorjudge1x_diff = filt_feature[2][0] - filt_feature[0][0]
                                        vectorjudge1y_diff = filt_feature[2][1] - filt_feature[0][1]
                                        vectorjudge2x_diff = filt_feature[1][0] - filt_feature[3][0]
                                        vectorjudge2y_diff = filt_feature[1][1] - filt_feature[3][1]
                                        vectorjudge_start = [vectorjudge1x_diff, vectorjudge1y_diff]
                                        vectorjudge_end = [vectorjudge2x_diff, vectorjudge2y_diff]
                                        if filt_feature[-5] != section_judge:
                                            if abs(filt_feature[0][0] - start_error["x"]) < 0.001 and abs(
                                                    filt_feature[0][1] - start_error["y"]) < 0.001:
                                                angle_1 = (vector_start[0] * vectorjudge_start[0] + vector_start[1] *
                                                           vectorjudge_start[1]) / (math.sqrt(vector_start[0] ** 2
                                                                                              + vector_start[
                                                                                                  1] ** 2) * math.sqrt(
                                                    vectorjudge_start[0] ** 2 + vectorjudge_start[1] ** 2))
                                                if angle_1 < 0:
                                                    tag_1 = 1
                                            if abs(filt_feature[1][0] - end_error["x"]) < 0.001 and abs(
                                                    filt_feature[1][1] - end_error["y"]) < 0.001:
                                                angle_2 = (vector_end[0] * vectorjudge_end[0] + vector_end[1] *
                                                           vectorjudge_end[1]) / (math.sqrt(vector_end[0] ** 2
                                                                                            + vector_end[
                                                                                                1] ** 2) * math.sqrt(
                                                    vectorjudge_end[0] ** 2 + vectorjudge_end[1] ** 2))
                                                if angle_2 < 0:
                                                    tag_2 = 1
                                if tag_1 == 1 and tag_2 == 1:
                                    Error.direction_opposite_all.append(section_judge)
                                    direction_opposite_all_all.append(feature_collection_flip[i])
                        else:
                            if round(feature_collection_flip[i][j][0][0], 6) == start_error["x"] and round(
                                    feature_collection_flip[i][j][1][0], 6) == end_error["x"] \
                                    and round(feature_collection_flip[i][j][0][1], 6) == start_error["y"] and round(
                                feature_collection_flip[i][j][1][1], 6) == end_error["y"]:
                                # print str(section_judge) + "_" + str(j), start_error, end_error
                                for filt in feature_collection_flip:
                                    for filt_feature in filt:
                                        vectorjudge1x_diff = filt_feature[2][0] - filt_feature[0][0]
                                        vectorjudge1y_diff = filt_feature[2][1] - filt_feature[0][1]
                                        vectorjudge2x_diff = filt_feature[1][0] - filt_feature[3][0]
                                        vectorjudge2y_diff = filt_feature[1][1] - filt_feature[3][1]
                                        vectorjudge_start = [vectorjudge1x_diff, vectorjudge1y_diff]
                                        vectorjudge_end = [vectorjudge2x_diff, vectorjudge2y_diff]
                                        if filt_feature[-5] != section_judge:
                                            if abs(filt_feature[0][0] - start_error["x"]) < 0.001 and abs(
                                                    filt_feature[0][1] - start_error["y"]) < 0.001:
                                                angle_1 = (vector_start[0] * vectorjudge_start[0] + vector_start[1] *
                                                           vectorjudge_start[1]) / (math.sqrt(vector_start[0] ** 2
                                                                                              + vector_start[
                                                                                                  1] ** 2) * math.sqrt(
                                                    vectorjudge_start[0] ** 2 + vectorjudge_start[1] ** 2))
                                                if angle_1 < 0:
                                                    tag_1 = 1
                                                    # print str(section_judge) + "___" + str(j), tag_1, filt_feature[
                                                    #     -5], angle_1 * 180 / math.pi
                                            if abs(filt_feature[1][0] - end_error["x"]) < 0.001 and abs(
                                                    filt_feature[1][1] - end_error["y"]) < 0.001:
                                                angle_2 = (vector_end[0] * vectorjudge_end[0] + vector_end[1] *
                                                           vectorjudge_end[1]) / (math.sqrt(vector_end[0] ** 2
                                                                                            + vector_end[
                                                                                                1] ** 2) * math.sqrt(
                                                    vectorjudge_end[0] ** 2 + vectorjudge_end[1] ** 2))
                                                if angle_2 < 0:
                                                    tag_2 = 1
                                                # print str(section_judge) + "___" + str(j), tag_2, filt_feature[-5]
                                if tag_1 == 1 and tag_2 == 1:
                                    Error.direction_opposite_single.append(section_judge)
                                    direction_opposite_single_all.append(feature_collection_flip[i][j])
            if check:
                for angle_filt in feature_collection_flip:
                    for angle_filt_feature in angle_filt:
                        angle_vectorjudge1x_diff = angle_filt_feature[2][0] - angle_filt_feature[0][0]
                        angle_vectorjudge1y_diff = angle_filt_feature[2][1] - angle_filt_feature[0][1]
                        angle_vectorjudge2x_diff = angle_filt_feature[1][0] - angle_filt_feature[3][0]
                        angle_vectorjudge2y_diff = angle_filt_feature[1][1] - angle_filt_feature[3][1]
                        angle_vectorjudge_start = [angle_vectorjudge1x_diff, angle_vectorjudge1y_diff]
                        angle_vectorjudge_end = [angle_vectorjudge2x_diff, angle_vectorjudge2y_diff]
                        if angle_filt_feature[-5] != section_judge:
                            if abs(angle_filt_feature[1][0] - feature_collection_flip[i][j][0][0]) < 0.001 and abs(
                                    angle_filt_feature[1][1] - feature_collection_flip[i][j][0][1]) < 0.001:
                                angle_filt_judge = (vector_start[0] * angle_vectorjudge_end[0] + vector_start[1] *
                                                    angle_vectorjudge_end[1]) / (
                                                           math.sqrt(vector_start[0] ** 2 + vector_start[1] ** 2) *
                                                           math.sqrt(angle_vectorjudge_end[0] ** 2 +
                                                                     angle_vectorjudge_end[1] ** 2))
                                if angle_filt_judge >= 0 and angle_filt_judge <= math.cos(angle_threshold):
                                    # print angle_filt_feature[-5], feature_collection_flip[i][j][-5], math.acos(
                                    #     angle_filt_judge) * 180 / math.pi
                                    # Error.feature_angle_error.append(str(section_judge)+ "_" +str(j))
                                    Error.feature_angle_error.append(section_judge)
            j += 1
        i += 1
        progressbar['value'] = i
        window.update()
        time.sleep(0.05)
    ID_repeat = Error.ID_repeat
    ID_subrepeat = Error.ID_subrepeat
    result1 = ''.join(["\"sectionID\"" + "=" + str(i) + " OR " for i in sorted(list(set(Error.ID_toobig)))])
    result2 = ''.join(["\"sectionID\"" + "=" + str(i) + " OR " for i in sorted(list(set(Error.laneType_error)))])
    result3 = ''.join(["\"sectionID\"" + "=" + str(i) + " OR " for i in sorted(list(set(Error.lane_error)))])
    result4 = ''.join(["\"sectionID\"" + "=" + str(i) + " OR " for i in sorted(list(set(Error.laneSpeed_error)))])
    result5 = ''.join(["\"sectionID\"" + "=" + str(i) + " OR " for i in sorted(list(set(Error.turnType_error)))])
    result6 = ''.join(["\"sectionID\"" + "=" + str(i) + " OR " for i in sorted(list(set(Error.ID_repeat)))])
    result7 = ''.join(["\"sectionID\"" + "=" + str(i) + " OR " for i in sorted(list(set(Error.ID_subrepeat)))])
    result8 = ''.join(["\"sectionID\"" + "=" + str(i) + " OR " for i in sorted(list(set(Error.single_lane_error)))])
    result9 = ''.join(
        ["\"sectionID\"" + "=" + str(i) + " OR " for i in sorted(list(set(Error.direction_opposite_single)))])
    result10 = ''.join(
        ["\"sectionID\"" + "=" + str(i) + " OR " for i in sorted(list(set(Error.direction_opposite_all)))])
    if check:
        result11 = ''.join(
            ["\"sectionID\"" + "=" + str(i) + " OR " for i in sorted(list(set(Error.feature_angle_error)))])
    text.insert("end", "Path:" + filename_path_shapefile)
    text.insert(tk.INSERT, "\n")
    text.insert(tk.INSERT, "\n")
    text.insert("end", "NO.1:ID数值错误:" + str(result1))
    text.insert(tk.INSERT, "\n")
    text.insert("end", "NO.2:车道类型错误:" + str(result2))
    text.insert(tk.INSERT, "\n")
    text.insert("end", "NO.3:辅助线错误:" + str(result3))
    text.insert(tk.INSERT, "\n")
    text.insert("end", "NO.4:限速错误:" + str(result4))
    text.insert(tk.INSERT, "\n")
    text.insert("end", "NO.5:转向错误:" + str(result5))
    text.insert(tk.INSERT, "\n")
    text.insert("end", "NO.6:ID重复错误:" + str(result6))
    text.insert(tk.INSERT, "\n")
    text.insert("end", "NO.7:车道宽错误:" + str(result7))
    text.insert(tk.INSERT, "\n")
    text.insert("end", "NO.8:单独线错误:" + str(result8))
    text.insert(tk.INSERT, "\n")
    text.insert("end", "NO.9:车道方向错误:" + str(result9))
    text.insert(tk.INSERT, "\n")
    text.insert("end", "NO.10:路段方向错误:" + str(result10))
    text.insert(tk.INSERT, "\n")
    if check:
        text.insert("end", "NO.11:衔接角度过大:" + str(result11))
        text.insert(tk.INSERT, "\n")
    text.insert("end", "-" * 226)
    text.insert(tk.INSERT, "\n")


def check():
    shapefile_check(buffer)


def shapefile_correct(*args):
    global buffer
    global map
    sub_direction_opposite_single_all = []
    sub_direction_opposite_all_all = []
    for sub1 in direction_opposite_single_all:
        if sub1 not in sub_direction_opposite_single_all:
            sub_direction_opposite_single_all.append(sub1)
    for sub in direction_opposite_all_all:
        if sub not in sub_direction_opposite_all_all:
            sub_direction_opposite_all_all.append(sub)
    for lane in buffer:
        # w = 0
        # while w <= len(single_lane_error) - 1:
        # 	print lane
        # 	if lane["geometry"] == single_lane_error[w][-1]:
        # 		del lane
        # 	w += 1
        s = 0
        while s <= len(sub_direction_opposite_single_all) - 1:
            if lane["geometry"] == sub_direction_opposite_single_all[s][-1]:
                coordinates_correct = sub_direction_opposite_single_all[s][-1]['coordinates'][::-1]
                del lane["geometry"]['coordinates']
                lane["geometry"]['coordinates'] = coordinates_correct
            s += 1
        l = 0
        while l <= len(sub_direction_opposite_all_all) - 1:
            y = 0
            while y <= len(sub_direction_opposite_all_all[l]) - 1:
                if lane["geometry"] == sub_direction_opposite_all_all[l][y][-1]:
                    coordinates_correct = sub_direction_opposite_all_all[l][y][-1]['coordinates'][::-1]
                    del lane["geometry"]['coordinates']
                    lane["geometry"]['coordinates'] = coordinates_correct
                y += 1
            l += 1
    # print ID_repeat
    gg = 1
    o = 0
    while o <= len(feature_collection_flip) - 1:
        ID_max = feature_collection_flip[0][0][-5]
        if feature_collection_flip[o][0][-5] in ID_repeat and feature_collection_flip[o][0][-5] not in ID_subrepeat:
            r = 0
            while r <= len(feature_collection_flip[o]) - 1:
                for lane in buffer:
                    for yy in range(0, len(ID_repeat)):
                        if lane['properties']['sectionID'] == ID_repeat[yy] and lane["geometry"] == \
                                feature_collection_flip[o][r][-1]:
                            del lane['properties']['sectionID']
                            step = yy
                            if r < len(feature_collection_flip[o]) - 1:
                                front_middle_x = feature_collection_flip[o][r][4][0]
                                front_middle_y = feature_collection_flip[o][r][4][1]
                                next_middle_x = feature_collection_flip[o][r + 1][4][0]
                                next_middle_y = feature_collection_flip[o][r + 1][4][1]
                                lane['properties']['sectionID'] = ID_max + step + gg
                                if math.sqrt((front_middle_x - next_middle_x) ** 2 + (
                                        front_middle_y - next_middle_y) ** 2) >= distance_threshold_down:
                                    gg += 1
                            # print lane
                            elif r == len(feature_collection_flip[o]) - 1:
                                lane['properties']['sectionID'] = ID_max + step + gg
                            # print lane
                        yy += 1
                r += 1
        o += 1
    map = {"type": "FeatureCollection", "features": buffer}


def correct():
    shapefile_correct(buffer)
    check()


def save_drivejson():
    pass


def select_bagfile():
    global numberOfFiles
    global bag_name
    global output_bagname
    global filename_path_bag
    bag_name = []
    filename_path_bag = filedialog.askopenfilenames(title='请选择bag文件', filetypes=[('bag', '*.bag'), ('All Files', '*')],
                                                    initialdir='/media/sf_desktop')
    numberOfFiles = str(len(filename_path_bag))
    for bagFile in filename_path_bag:
        bag = rosbag.Bag(bagFile)
        bagName = bag.filename
        bag_name.append(bagName.rstrip('.bag').split("/"))
    output_bagname = bag_name[0][-1] + '_' + bag_name[-1][-1]


def merge_bagfile():
    mergebag_output = filedialog.asksaveasfilename(title='请输入保存文件名', initialfile=output_bagname + '.bag',
                                                   filetypes=[('bag', '*.bag'), ('All Files', '*')],
                                                   initialdir='/media/sf_Desktop/')
    progressbar['value'] = 0
    progressbar['maximum'] = len(filename_path_bag) + 1
    count = 1
    total_included_count = 0
    total_skipped_count = 0
    with Bag(mergebag_output, 'w') as o:
        for bagFile in filename_path_bag:
            included_count = 0
            skipped_count = 0
            matchedtopics = []
            bag = rosbag.Bag(bagFile)
            topic_inputname = topic_input.get()
            if topic_inputname:
                bagContents = bag.read_messages(topic_inputname)
            if not topic_inputname:
                bagContents = bag.read_messages()
            listOfTopics = []
            for topic, msg, t in bagContents:
                if topic not in listOfTopics:
                    listOfTopics.append(topic)
            if count == 1:
                text.insert("end", "Path:" + str(bagFile).lstrip("/"))
            elif count != 1:
                text.insert(tk.INSERT, "\n")
                text.insert("end", "Path:" + str(bagFile).lstrip("/"))
            text.insert(tk.INSERT, "\n")
            text.insert("end", "正在合并第" + str(count) + "个bag文件")
            text.insert(tk.INSERT, "\n")
            with Bag(bagFile, 'r') as ib:
                for topic, msg, t in ib:
                    if any(fnmatchcase(topic, pattern) for pattern in listOfTopics):
                        if not topic in matchedtopics:
                            matchedtopics.append(topic)
                        o.write(topic, msg, t)
                        included_count += 1
                    else:
                        skipped_count += 1
            total_included_count += included_count
            total_skipped_count += skipped_count
            text.insert("end", "包括 %d 个消息，跳过 %d 个消息" % (included_count, skipped_count))
            text.insert(tk.INSERT, "\n")
            count += 1
            progressbar['value'] = count
            window.update()
            time.sleep(0.05)
    bag.close()
    text.insert(tk.INSERT, "\n")
    text.insert("end", "总共包括 %d 个消息，跳过 %d 个消息" % (total_included_count, total_skipped_count))
    text.insert(tk.INSERT, "\n")
    text.insert("end", "已处理完成所有" + numberOfFiles + "个bag文件!")
    text.insert(tk.INSERT, "\n")
    text.insert("end", "-" * 226)
    text.insert(tk.INSERT, "\n")


def save_csv():
    global topic_inputname
    global csv_output
    progressbar['value'] = 0
    progressbar['maximum'] = len(filename_path_bag) + 1
    count = 1
    for bagFile in filename_path_bag:
        if count == 1:
            text.insert("end", "Path:" + str(bagFile).lstrip("/"))
        elif count != 1:
            text.insert(tk.INSERT, "\n")
            text.insert("end", "Path:" + str(bagFile).lstrip("/"))
        text.insert(tk.INSERT, "\n")
        text.insert(tk.INSERT, "\n")
        text.insert("end", "正在读取第" + str(count) + "个bag文件")
        text.insert(tk.INSERT, "\n")
        bag = rosbag.Bag(bagFile)
        bagName = bag.filename
        topic_inputname = topic_input.get()
        if topic_inputname:
            bagContents = bag.read_messages(topic_inputname)
        if not topic_inputname:
            bagContents = bag.read_messages()
        listOfTopics = []
        for topic, msg, t in bagContents:
            if topic not in listOfTopics:
                listOfTopics.append(topic)
        for topicName in listOfTopics:
            text.insert("end", "正在提取" + topicName + "话题")
            text.insert(tk.INSERT, "\n")
            filename = bagName[:-4] + topicName.replace('/', '_') + '.csv'
            csv_output = filedialog.asksaveasfilename(title='请输入保存文件名',
                                                      initialfile=(filename.split('/')[-1]).split('.')[:-1],
                                                      filetypes=[('csv', '*.csv'), ('All Files', '*')],
                                                      initialdir='/media/sf_Desktop/')
            with open(csv_output, 'w+') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',')
                firstIteration = True
                for subtopic, msg, t in bag.read_messages(topicName):
                    msgString = str(msg)
                    msgList = string.split(msgString, '\n')
                    instantaneousListOfData = []
                    for nameValuePair in msgList:
                        splitPair = string.split(nameValuePair, ':')
                        for i in range(len(splitPair)):
                            splitPair[i] = string.strip(splitPair[i])
                        instantaneousListOfData.append(splitPair)
                    if firstIteration:
                        headers = ["rosbagTimestamp"]
                        for pair in instantaneousListOfData:
                            headers.append(pair[0])
                        filewriter.writerow(headers)
                        firstIteration = False
                    values = [str(t)]
                    for pair in instantaneousListOfData:
                        if len(pair) > 1:
                            values.append(pair[1])
                    filewriter.writerow(values)
        count += 1
        progressbar['value'] = count
        window.update()
        time.sleep(0.05)
        bag.close()
    text.insert(tk.INSERT, "\n")
    text.insert("end", "已处理完成所有" + numberOfFiles + "个bag文件!")
    text.insert(tk.INSERT, "\n")
    text.insert("end", "-" * 226)
    text.insert(tk.INSERT, "\n")


def generate_trajectorypolyline():
    global topic_inputname, shapefile_output
    if point_entry.get():
        point_threshold = int(point_entry.get())
    else:
        point_threshold = 0
    global topic_inputname
    progressbar['value'] = 0
    progressbar['maximum'] = len(filename_path_bag) + 1
    count = 1
    for bagFile in filename_path_bag:
        line_collect = []
        line_collect_x = []
        line_collect_y = []
        if count == 1:
            text.insert("end", "Path:" + str(bagFile).lstrip("/"))
        elif count != 1:
            text.insert(tk.INSERT, "\n")
            text.insert("end", "Path:" + str(bagFile).lstrip("/"))
        text.insert(tk.INSERT, "\n")
        text.insert(tk.INSERT, "\n")
        text.insert("end", "正在读取第" + str(count) + "个bag文件")
        text.insert(tk.INSERT, "\n")
        bag = rosbag.Bag(bagFile)
        bagName = bag.filename
        topic_inputname = topic_input.get()
        if topic_inputname:
            bagContents = bag.read_messages(topic_inputname)
        if not topic_inputname:
            bagContents = bag.read_messages()
        listOfTopics = []
        for topic, msg, t in bagContents:
            if topic not in listOfTopics:
                listOfTopics.append(topic)
        for topicName in listOfTopics:
            data_east = []
            data_north = []
            text.insert(tk.INSERT, "\n")
            filename = bagName[:-4] + topicName.replace('/', '_') + '.csv'
            shapefile_output = filedialog.asksaveasfilename(title='请输入保存文件名',initialfile=(filename.split('/')[-1]).split('.')[:-1],filetypes=[('shp', '*.shp'), ('All Files', '*')],
                                                            initialdir='/media/sf_Desktop/')
            for subtopic, msg, t in bag.read_messages(topicName):
                msgString = str(msg)
                msgList = string.split(msgString, '\n')
                for nameValuePair in msgList:
                    splitPair = string.split(nameValuePair, ':')
                    if splitPair[0] == "utm_east" or splitPair[0] == "    x":
                        data_east.append(splitPair[1])
                    elif splitPair[0] == "utm_north" or splitPair[0] == "    y":
                        data_north.append(splitPair[1])
        ployLine = shapefile.Writer(target=shapefile_output, shapeType=3, autoBalance=1)
        ployLine.field('count', 'N', decimal=10)
        if len(data_east) == len(data_north) and len(data_east) != 0:
            point_count = 0
            if point_threshold != 0:
                for r in range(len(data_east)):
                    if  point_count == 0 or point_count % point_threshold == 0:
                        line_collect.append([float(data_east[r]),float(data_north[r])])
                        line_collect_x.append(float(data_east[r]))
                        line_collect_y.append(float(data_north[r]))
                    point_count += 1
            else:
                for r in range(len(data_east)):
                    line_collect.append([float(data_east[r]),float(data_north[r])])
                    line_collect_x.append(float(data_east[r]))
                    line_collect_y.append(float(data_north[r]))
                    point_count += 1
        plt.plot(line_collect_x,line_collect_y,'b.-')
        plt.grid()
        plt.show()
        ployLine.line([line_collect])
        ployLine.record(point_count)
        ployLine.close()
        bag.close()
        count += 1
        progressbar['value'] = count
        window.update()
        time.sleep(0.05)
    text.insert(tk.INSERT, "\n")
    text.insert("end", "已处理完成所有" + numberOfFiles + "个bag文件!")
    text.insert(tk.INSERT, "\n")
    text.insert("end", "-" * 226)
    text.insert(tk.INSERT, "\n")


def generate_trajectorypoint():
    global topic_inputname, shapefile_output
    if point_entry.get():
        point_threshold = int(point_entry.get())
    else:
        point_threshold = 0
    progressbar['value'] = 0
    progressbar['maximum'] = len(filename_path_bag) + 1
    count = 1
    for bagFile in filename_path_bag:
        line_collect_x = []
        line_collect_y = []
        if count == 1:
            text.insert("end", "Path:" + str(bagFile).lstrip("/"))
        elif count != 1:
            text.insert(tk.INSERT, "\n")
            text.insert("end", "Path:" + str(bagFile).lstrip("/"))
        text.insert(tk.INSERT, "\n")
        text.insert(tk.INSERT, "\n")
        text.insert("end", "正在读取第" + str(count) + "个bag文件")
        text.insert(tk.INSERT, "\n")
        bag = rosbag.Bag(bagFile)
        bagName = bag.filename
        topic_inputname = topic_input.get()
        if topic_inputname:
            bagContents = bag.read_messages(topic_inputname)
        if not topic_inputname:
            bagContents = bag.read_messages()
        listOfTopics = []
        for topic, msg, t in bagContents:
            if topic not in listOfTopics:
                listOfTopics.append(topic)
        for topicName in listOfTopics:
            data_east = []
            data_north = []
            text.insert(tk.INSERT, "\n")
            filename = bagName[:-4] + topicName.replace('/', '_') + '.csv'
            shapefile_output = filedialog.asksaveasfilename(title='请输入保存文件名',initialfile=(filename.split('/')[-1]).split('.')[:-1],filetypes=[('shp', '*.shp'), ('All Files', '*')],
                                                            initialdir='/media/sf_Desktop/')
            for subtopic, msg, t in bag.read_messages(topicName):
                msgString = str(msg)
                msgList = string.split(msgString, '\n')
                for nameValuePair in msgList:
                    splitPair = string.split(nameValuePair, ':')
                    if splitPair[0] == "utm_east" or splitPair[0] == "    x":
                        data_east.append(splitPair[1])
                    elif splitPair[0] == "utm_north" or splitPair[0] == "    y":
                        data_north.append(splitPair[1])
        ployLine = shapefile.Writer(target=shapefile_output, shapeType=1, autoBalance=1)
        ployLine.field('utm_east', 'F', decimal=10)
        ployLine.field('utm_north', 'F', decimal=10)
        if len(data_east) == len(data_north) and len(data_east) != 0:
            if point_threshold != 0:
                point_count = 0
                for r in range(len(data_east)):
                    if point_count == 0 or point_count % point_threshold == 0:
                        ployLine.point(float(data_east[r]), float(data_north[r]))
                        ployLine.record(float(data_east[r]), float(data_north[r]))
                        line_collect_x.append(float(data_east[r]))
                        line_collect_y.append(float(data_north[r]))
                    point_count += 1
            else:
                for r in range(len(data_east)):
                    ployLine.point(float(data_east[r]), float(data_north[r]))
                    ployLine.record(float(data_east[r]), float(data_north[r]))
                    line_collect_x.append(float(data_east[r]))
                    line_collect_y.append(float(data_north[r]))
        plt.plot(line_collect_x,line_collect_y,'b.-')
        plt.grid()
        plt.show()
        ployLine.close()
        bag.close()
        count += 1
        progressbar['value'] = count
        window.update()
        time.sleep(0.05)
    text.insert(tk.INSERT, "\n")
    text.insert("end", "已处理完成所有" + numberOfFiles + "个bag文件!")
    text.insert(tk.INSERT, "\n")
    text.insert("end", "-" * 226)
    text.insert(tk.INSERT, "\n")


def select_geojson():
    global map
    global file_name
    file_name = filedialog.askopenfilename(title='请选择json文件',filetypes=[('json', '*.json'), ('json', '*.ini'), ('json', '*.tmp'),('json', '*.inj'), ('All Files', '*')],
                                           initialdir='/media/sf_Desktop/')
    json_file = open(file_name)
    map = json.load(json_file)


def select_drivejson():
    global map
    global file_name
    file_name = filedialog.askopenfilename(title='请选择json文件', filetypes=[('json', '*.json'), ('All Files', '*')],
                                           initialdir='/media/sf_Desktop/')
    json_file = open(file_name)
    map = json.load(json_file)


def generate_centerline():
    file = "/media/sf_Desktop/shapefile"
    mkdir(file)
    driver = ogr.GetDriverByName('ESRI Shapefile')
    point_shp = '/media/sf_Desktop/shapefile/centerline_shp.shp'
    if os.path.exists(point_shp):
        driver.DeleteDataSource(point_shp)
    ds = driver.CreateDataSource(point_shp)
    layer = ds.CreateLayer('centerline_shp', geom_type=ogr.wkbLineString)
    if map.has_key('roads'):
        fieldx = ogr.FieldDefn('x', ogr.OFTReal)
        fieldy = ogr.FieldDefn('y', ogr.OFTReal)
        fieldID = ogr.FieldDefn('sectionID', ogr.OFTInteger)
        fieldType = ogr.FieldDefn('laneType', ogr.OFTInteger)
        fieldSpeed = ogr.FieldDefn('laneSpeed', ogr.OFTInteger)
        fieldTurn = ogr.FieldDefn('turnType', ogr.OFTInteger)
        layer.CreateField(fieldx)
        layer.CreateField(fieldy)
        layer.CreateField(fieldID)
        layer.CreateField(fieldType)
        layer.CreateField(fieldSpeed)
        layer.CreateField(fieldTurn)
        featureDefn = layer.GetLayerDefn()
        text.insert(tk.INSERT, '\n')
        text.insert('end', "Path:" + file_name)
        text.insert(tk.INSERT, '\n')
        progressbar['value'] = 0
        progressbar['maximum'] = len(map['roads']) + 1
        count = 1
        for road in map['roads']:
            for laneSection in road['laneSections']:
                for lane in laneSection['lanes']:
                    if lane['type'] == "driving":
                        laneType = 0
                    elif lane['type'] == "seaside":
                        laneType = 1
                    elif lane['type'] == "yard":
                        laneType = 2
                    elif lane['type'] == "cross":
                        laneType = 3
                    elif lane['type'] == "connection":
                        laneType = 4
                    elif lane['type'] == "lockzone":
                        laneType = 5
                    elif lane['type'] == "hatchcover":
                        laneType = 6
                    elif lane['type'] == "latitude":
                        laneType = 7
                    elif lane['type'] == "longitude":
                        laneType = 8
                    elif lane['type'] == "emergency":
                        laneType = 10
                    elif lane['type'] == "tunnel":
                        laneType = 12
                    elif lane['type'] == "underbridge":
                        laneType = 13
                    elif lane['type'] == "ramp":
                        laneType = 14
                    if lane['turnType'] == "noTurn":
                        turnType = 0
                    elif lane['turnType'] == "leftTurn":
                        turnType = 1
                    elif lane['turnType'] == "rightTurn":
                        turnType = 2
                    elif lane['turnType'] == "uTurn":
                        turnType = 3
                    # laneType = 0
                    sectionID = road['id']
                    laneSpeed = lane['speedLimit']
                    feature = ogr.Feature(featureDefn)
                    line = ogr.Geometry(ogr.wkbLineString)
                    for point in lane['centerLine']:
                        line.AddPoint(point['x'], point['y'])
                    feature.SetGeometry(line)
                    feature.SetField('sectionID', sectionID)
                    feature.SetField('laneType', laneType)
                    feature.SetField('laneSpeed', laneSpeed)
                    feature.SetField('turnType', turnType)
                    layer.CreateFeature(feature)
            count += 1
            progressbar['value'] = count
            window.update()
            time.sleep(0.05)
        ds.Destroy()
        text.insert(tk.INSERT, '\n')
        text.insert('end', "已生成点!")
        text.insert(tk.INSERT, '\n')
        text.insert("end", "-" * 226)
        text.insert(tk.INSERT, "\n")
    elif map.has_key('type'):
        fieldx = ogr.FieldDefn('x', ogr.OFTReal)
        fieldy = ogr.FieldDefn('y', ogr.OFTReal)
        layer.CreateField(fieldx)
        layer.CreateField(fieldy)
        featureDefn = layer.GetLayerDefn()
        text.insert(tk.INSERT, '\n')
        text.insert('end', "Path:" + file_name)
        text.insert(tk.INSERT, '\n')
        progressbar['value'] = 0
        progressbar['maximum'] = len(map['features']) + 1
        count = 1
        for subfeature in map['features']:
            x = subfeature['geometry']['coordinates'][0]
            y = subfeature['geometry']['coordinates'][1]
            feature = ogr.Feature(featureDefn)
            line = ogr.Geometry(ogr.wkbLineString)
            line.AddPoint(x, y)
            feature.SetGeometry(line)
            feature.SetField('x', x)
            feature.SetField('y', y)
            layer.CreateFeature(feature)
            count += 1
            progressbar['value'] = count
            window.update()
            time.sleep(0.05)
        ds.Destroy()
        text.insert(tk.INSERT, '\n')
        text.insert('end', "已生成车道中心线!")
        text.insert(tk.INSERT, '\n')
        text.insert("end", "-" * 226)
        text.insert(tk.INSERT, "\n")


def generate_polyline():
    file = "/media/sf_Desktop/shapefile"
    mkdir(file)
    driver = ogr.GetDriverByName('ESRI Shapefile')
    polyline_shp = '/media/sf_Desktop/shapefile/polyline_shp.shp'
    if os.path.exists(polyline_shp):
        driver.DeleteDataSource(polyline_shp)
    ds = driver.CreateDataSource(polyline_shp)
    layer = ds.CreateLayer('polyline_shp', geom_type=ogr.wkbLineString)
    if map.has_key('roads'):
        fieldID = ogr.FieldDefn('sectionID', ogr.OFTInteger)
        fieldType = ogr.FieldDefn('laneType', ogr.OFTInteger)
        fieldSpeed = ogr.FieldDefn('laneSpeed', ogr.OFTInteger)
        fieldTurn = ogr.FieldDefn('turnType', ogr.OFTInteger)
        fieldVir = ogr.FieldDefn('virtual', ogr.OFTInteger)
        fieldCha = ogr.FieldDefn('change', ogr.OFTInteger)
        layer.CreateField(fieldID)
        layer.CreateField(fieldType)
        layer.CreateField(fieldSpeed)
        layer.CreateField(fieldTurn)
        layer.CreateField(fieldVir)
        layer.CreateField(fieldCha)
        text.insert(tk.INSERT, '\n')
        text.insert('end', "Path:" + file_name)
        text.insert(tk.INSERT, '\n')
        progressbar['value'] = 0
        progressbar['maximum'] = len(map['roads']) + 1
        num = 1
        for road in map['roads']:
            for laneSection in road['laneSections']:
                count = 0
                for lane in laneSection['lanes']:
                    if lane['type'] == "driving":
                        laneType = 0
                    elif lane['type'] == "seaside":
                        laneType = 1
                    elif lane['type'] == "yard":
                        laneType = 2
                    elif lane['type'] == "cross":
                        laneType = 3
                    elif lane['type'] == "connection":
                        laneType = 4
                    elif lane['type'] == "lockzone":
                        laneType = 5
                    elif lane['type'] == "hatchcover":
                        laneType = 6
                    elif lane['type'] == "latitude":
                        laneType = 7
                    elif lane['type'] == "longitude":
                        laneType = 8
                    elif lane['type'] == "emergency":
                        laneType = 10
                    elif lane['type'] == "tunnel":
                        laneType = 12
                    elif lane['type'] == "underbridge":
                        laneType = 13
                    elif lane['type'] == "ramp":
                        laneType = 14
                    if lane['turnType'] == "noTurn":
                        turnType = 0
                    elif lane['turnType'] == "leftTurn":
                        turnType = 1
                    elif lane['turnType'] == "rightTurn":
                        turnType = 2
                    elif lane['turnType'] == "uTurn":
                        turnType = 3
                    if count == 0:
                        sectionID = road['id']
                        laneSpeed = lane['speedLimit']
                        virtual = 0
                        change = 0
                        featureDefn = layer.GetLayerDefn()
                        feature = ogr.Feature(featureDefn)
                        line = ogr.Geometry(ogr.wkbLineString)
                        for point in lane['leftBorder']["pointSet"]:
                            line.AddPoint(point['x'], point['y'])
                        feature.SetGeometry(line)
                        feature.SetField('sectionID', sectionID)
                        feature.SetField('laneType', laneType)
                        feature.SetField('laneSpeed', laneSpeed)
                        feature.SetField('turnType', turnType)
                        feature.SetField('virtual', virtual)
                        feature.SetField('change', change)
                        layer.CreateFeature(feature)
                        featureDefn = layer.GetLayerDefn()
                        feature = ogr.Feature(featureDefn)
                        line = ogr.Geometry(ogr.wkbLineString)
                        for point in lane['rightBorder']["pointSet"]:
                            line.AddPoint(point['x'], point['y'])
                        feature.SetGeometry(line)
                        feature.SetField('sectionID', sectionID)
                        feature.SetField('laneType', laneType)
                        feature.SetField('laneSpeed', laneSpeed)
                        feature.SetField('turnType', turnType)
                        feature.SetField('virtual', virtual)
                        feature.SetField('change', change)
                        layer.CreateFeature(feature)
                    if count != 0:
                        sectionID = road['id']
                        laneSpeed = lane['speedLimit']
                        virtual = 0
                        change = 0
                        featureDefn = layer.GetLayerDefn()
                        feature = ogr.Feature(featureDefn)
                        line = ogr.Geometry(ogr.wkbLineString)
                        for point in lane['rightBorder']["pointSet"]:
                            line.AddPoint(point['x'], point['y'])
                        feature.SetGeometry(line)
                        feature.SetField('sectionID', sectionID)
                        feature.SetField('laneType', laneType)
                        feature.SetField('laneSpeed', laneSpeed)
                        feature.SetField('turnType', turnType)
                        feature.SetField('virtual', virtual)
                        feature.SetField('change', change)
                        layer.CreateFeature(feature)
                        if laneType == 1:
                            featureDefn = layer.GetLayerDefn()
                            feature = ogr.Feature(featureDefn)
                            line = ogr.Geometry(ogr.wkbLineString)
                            for point in lane['leftBorder']["pointSet"]:
                                line.AddPoint(point['x'], point['y'])
                            feature.SetGeometry(line)
                            feature.SetField('sectionID', sectionID)
                            feature.SetField('laneType', laneType)
                            feature.SetField('laneSpeed', laneSpeed)
                            feature.SetField('turnType', turnType)
                            feature.SetField('virtual', virtual)
                            feature.SetField('change', change)
                            layer.CreateFeature(feature)
                    count += 1
            num += 1
            progressbar['value'] = num
            window.update()
            time.sleep(0.05)
        ds.Destroy()
        text.insert(tk.INSERT, '\n')
        text.insert('end', "已生成车道线!")
        text.insert(tk.INSERT, '\n')
        text.insert("end", "-" * 226)
        text.insert(tk.INSERT, "\n")
    elif map.has_key('type'):
        fieldsectionID = ogr.FieldDefn('sectionID', ogr.OFTInteger)
        fieldlaneType = ogr.FieldDefn('laneType', ogr.OFTInteger)
        filedlaneSpeed = ogr.FieldDefn('laneSpeed', ogr.OFTInteger)
        filedturnType = ogr.FieldDefn('turnType', ogr.OFTInteger)
        filedroadType = ogr.FieldDefn('roadType', ogr.OFTInteger)
        filedlineType = ogr.FieldDefn('lineType', ogr.OFTInteger)
        filedchange = ogr.FieldDefn('change', ogr.OFTInteger)
        layer.CreateField(fieldsectionID)
        layer.CreateField(fieldlaneType)
        layer.CreateField(filedlaneSpeed)
        layer.CreateField(filedturnType)
        layer.CreateField(filedroadType)
        layer.CreateField(filedlineType)
        layer.CreateField(filedchange)
        text.insert(tk.INSERT, '\n')
        # text.insert('end', "Path:" + file_name)
        # text.insert(tk.INSERT, '\n')
        progressbar['value'] = 0
        progressbar['maximum'] = len(map['features']) + 1
        count = 1
        for subfeature in map['features']:
            sectionID = subfeature['properties']['sectionID']
            laneType = subfeature['properties']['laneType']
            laneSpeed = subfeature['properties']['laneSpeed']
            turnType = subfeature['properties']['turnType']
            roadType = subfeature['properties']['roadType']
            lineType = subfeature['properties']['lineType']
            change = subfeature['properties']['change']
            featureDefn = layer.GetLayerDefn()
            feature = ogr.Feature(featureDefn)
            line = ogr.Geometry(ogr.wkbLineString)
            for point in subfeature['geometry']['coordinates']:
                line.AddPoint(point[0], point[1])
            feature.SetGeometry(line)
            feature.SetField('sectionID', sectionID)
            feature.SetField('laneType', laneType)
            feature.SetField('laneSpeed', laneSpeed)
            feature.SetField('turnType', turnType)
            feature.SetField('roadType', roadType)
            feature.SetField('lineType', lineType)
            feature.SetField('change', change)
            layer.CreateFeature(feature)
            count += 1
            progressbar['value'] = count
            window.update()
            time.sleep(0.05)
        ds.Destroy()
        text.insert(tk.INSERT, '\n')
        text.insert('end', "已生成车道线!")
        text.insert(tk.INSERT, '\n')
        text.insert("end", "-" * 226)
        text.insert(tk.INSERT, "\n")


def generate_polygon():
    file = "/media/sf_Desktop/shapefile"
    mkdir(file)
    driver = ogr.GetDriverByName('ESRI Shapefile')
    polygon_shp = '/media/sf_Desktop/shapefile/polygon_shp.shp'
    if os.path.exists(polygon_shp):
        driver.DeleteDataSource(polygon_shp)
    ds = driver.CreateDataSource(polygon_shp)
    layer = ds.CreateLayer('polygon_shp', geom_type=ogr.wkbPolygon)
    if map.has_key('roads'):
        fieldID = ogr.FieldDefn('junctionID', ogr.OFTInteger)
        layer.CreateField(fieldID)
        text.insert(tk.INSERT, '\n')
        text.insert('end', "Path:" + file_name)
        text.insert(tk.INSERT, '\n')
        progressbar['value'] = 0
        progressbar['maximum'] = len(map['junctions']) + 1
        count = 1
        for junction in map['junctions']:
            junctionID = junction['id']
            featureDefn = layer.GetLayerDefn()
            feature = ogr.Feature(featureDefn)
            polygon = ogr.Geometry(ogr.wkbPolygon)
            outring = ogr.Geometry(ogr.wkbLinearRing)
            for outline_point in junction["outline"]:
                outring.AddPoint(outline_point['x'], outline_point['y'])
            polygon.AddGeometry(outring)
            feature.SetGeometry(polygon)
            feature.SetField('junctionID', junctionID)
            layer.CreateFeature(feature)
            count += 1
            progressbar['value'] = count
            window.update()
            time.sleep(0.05)
        ds.Destroy()
        text.insert(tk.INSERT, '\n')
        text.insert('end', "已生成掩膜!")
        text.insert(tk.INSERT, '\n')
        text.insert("end", "-" * 226)
        text.insert(tk.INSERT, "\n")
    if map.has_key('type'):
        fieldID = ogr.FieldDefn('junctionID', ogr.OFTInteger)
        layer.CreateField(fieldID)
        if map['features'][0]['properties'].has_key('type'):
            fieldtype = ogr.FieldDefn('type', ogr.OFTInteger)
            layer.CreateField(fieldtype)
        text.insert(tk.INSERT, '\n')
        text.insert('end', "Path:" + file_name)
        text.insert(tk.INSERT, '\n')
        progressbar['value'] = 0
        progressbar['maximum'] = len(map['features']) + 1
        count = 1
        for subfeature in map['features']:
            junctionID = subfeature['properties']['junctionID']
            if subfeature['properties'].has_key('type'):
                type = subfeature['properties']['type']
            featureDefn = layer.GetLayerDefn()
            feature = ogr.Feature(featureDefn)
            polygon = ogr.Geometry(ogr.wkbPolygon)
            outring = ogr.Geometry(ogr.wkbLinearRing)
            for outline_point in subfeature['geometry']['coordinates'][0]:
                outring.AddPoint(outline_point[0], outline_point[1])
            polygon.AddGeometry(outring)
            feature.SetGeometry(polygon)
            feature.SetField('junctionID', junctionID)
            if subfeature['properties'].has_key('type'):
                feature.SetField('type', type)
            layer.CreateFeature(feature)
            count += 1
            progressbar['value'] = count
            window.update()
            time.sleep(0.05)
        ds.Destroy()
        text.insert(tk.INSERT, '\n')
        text.insert('end', "已生成掩膜!")
        text.insert(tk.INSERT, '\n')
        text.insert("end", "-" * 226)
        text.insert(tk.INSERT, "\n")


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def cal_road():
    center = {"centerx": centerx, "centery": centery}
    left = {"leftx": leftx, "lefty": lefty}
    right = {"rightx": rightx, "righty": righty}
    leftB = []
    rightB = []
    road_feature = []
    i = 0
    while i <= len(left["leftx"]) - 1:
        j = 0
        leftBorder_pointSets = []
        leftBorder = {}
        rightBorder_pointSets = []
        rightBorder = {}
        while j <= len(left["leftx"][i]) - 1:
            leftBorder_point = {}
            leftBorder_point["x"] = left["leftx"][i][j]
            leftBorder_point["y"] = left["lefty"][i][j]
            leftBorder_point["z"] = 0
            leftBorder_pointSets.append(leftBorder_point)
            rightBorder_point = {}
            rightBorder_point["x"] = right["rightx"][i][j]
            rightBorder_point["y"] = right["righty"][i][j]
            rightBorder_point["z"] = 0
            rightBorder_pointSets.append(rightBorder_point)
            j += 1
        leftBorder["virtual"] = "FALSE"
        leftBorder["type"] = "broken"
        leftBorder["color"] = "white"
        leftBorder["pointSet"] = leftBorder_pointSets
        leftB.append(leftBorder)
        rightBorder["virtual"] = "FALSE"
        rightBorder["type"] = "broken"
        rightBorder["color"] = "white"
        rightBorder["pointSet"] = rightBorder_pointSets
        rightB.append(rightBorder)
        i += 1
    i = 0
    while i <= len(center["centerx"]) - 1:
        lane_feature = {}
        lanes_feature = []
        lanesection_feature = []
        lane_section = {}
        section_feature = {}
        centerLine = []
        n = 0
        while n <= len(center["centerx"][i]) - 1:
            centerLine_points = {}
            centerLine_points["id"] = str(1000 + i) + "_" + str(i) + "_" + str(n)
            centerLine_points["heading"] = heading[i][n]
            centerLine_points["x"] = centerx[i][n]
            centerLine_points["y"] = centery[i][n]
            centerLine_points["z"] = 0
            centerLine_points["lenIntegral"] = sum_length[i][n]
            centerLine.append(centerLine_points)
            n += 1
        lane_feature["id"] = 0
        lane_feature["uid"] = str(1000 + i) + "_" + str(0)
        lane_feature["type"] = "driving"
        lane_feature["turnType"] = "noTurn"
        lane_feature["speedLimit"] = 20
        if len(centerx) == 1:
            lane_feature["link"] = {"predecessors": [], "successors": []}
            lane_feature["laneOverlapGroup"] = []
        elif len(centerx) == 2:
            if i == 0:
                successors = [{"id": str(1001) + "_" + str(0)}]
                lane_feature["link"] = {"predecessors": [], "successors": successors}
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


def bag_drivejson():
    global numberOfFiles
    global bag_name
    global output_bagname
    global filename_path_bag
    global centerx, centery
    global leftx, lefty
    global rightx, righty
    global heading, sum_length
    bag_name = []
    drivejson = {}
    filename_path_bag = filedialog.askopenfilenames(title='请选择bag文件', filetypes=[('bag', '*.bag'), ('All Files', '*')],
                                                    initialdir='/media/sf_desktop')
    numberOfFiles = str(len(filename_path_bag))
    bag_count = 0
    for bagFile in filename_path_bag:
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
        leftLinex = []
        leftLiney = []
        rightLinex = []
        rightLiney = []
        col_heading = []
        col_sum_length = []
        i = 0
        sum_length = 0
        while i <= len(centerLinex) - 1:
            if i == 0:
                x = centerLinex[0]
                y = centerLiney[0]
                # print x,y
                x_next = centerLinex[1]
                y_next = centerLiney[1]
                heading = math.atan2(y_next - y, x_next - x)
                length = 0
                leftLinex.append(x)
                leftLiney.append(y)
                rightLinex.append(x)
                rightLiney.append(y)
            elif 0 < i < len(centerLinex) - 1:
                x = centerLinex[i]
                y = centerLiney[i]
                x_pre = centerLinex[i - 1]
                y_pre = centerLiney[i - 1]
                x_next = centerLinex[i + 1]
                y_next = centerLinex[i + 1]
                heading1 = math.atan2(y - y_pre, x - x_pre)
                heading2 = math.atan2(y_next - y, x_next - x)
                heading = (heading1 + heading2) / 2
                length = math.sqrt((y - y_pre) ** 2 + (x - x_pre) ** 2)
                vector_1 = [x_pre - x, y_pre - y]
                vector_2 = [x_next - x, y_next - y]
                try:
                    leftLinex.append(x + 1.5 / ((vector_1[0] * vector_2[1] + vector_1[1] * vector_2[0]) / math.sqrt(
                        vector_1[0] ** 2 + vector_1[1] ** 2) / math.sqrt
                                                (vector_2[0] ** 2 + vector_2[1] ** 2)) * (
                                                 vector_1[0] / math.sqrt(vector_1[0] ** 2 + vector_1[1] ** 2) +
                                                 vector_2[0] / math.sqrt(vector_2[0] ** 2 + vector_2[1] ** 2)))
                    leftLiney.append(y + 1.5 / ((vector_1[0] * vector_2[1] + vector_1[1] * vector_2[0]) / math.sqrt(
                        vector_1[0] ** 2 + vector_1[1] ** 2) / math.sqrt
                                                (vector_2[0] ** 2 + vector_2[1] ** 2)) * (
                                                 vector_1[1] / math.sqrt(vector_1[0] ** 2 + vector_1[1] ** 2) +
                                                 vector_2[1] / math.sqrt(vector_2[0] ** 2 + vector_2[1] ** 2)))
                    rightLinex.append(x - 1.5 / ((vector_1[0] * vector_2[1] + vector_1[1] * vector_2[0]) / math.sqrt(
                        vector_1[0] ** 2 + vector_1[1] ** 2) / math.sqrt
                                                 (vector_2[0] ** 2 + vector_2[1] ** 2)) * (
                                                  vector_1[0] / math.sqrt(vector_1[0] ** 2 + vector_1[1] ** 2) +
                                                  vector_2[0] / math.sqrt(vector_2[0] ** 2 + vector_2[1] ** 2)))
                    rightLiney.append(y - 1.5 / ((vector_1[0] * vector_2[1] + vector_1[1] * vector_2[0]) / math.sqrt(
                        vector_1[0] ** 2 + vector_1[1] ** 2) / math.sqrt
                                                 (vector_2[0] ** 2 + vector_2[1] ** 2)) * (
                                                  vector_1[1] / math.sqrt(vector_1[0] ** 2 + vector_1[1] ** 2) +
                                                  vector_2[1] / math.sqrt(vector_2[0] ** 2 + vector_2[1] ** 2)))
                except:
                    print "error!!"
                    leftLinex.append(centerLinex[i])
                    leftLiney.append(centerLiney[i])
                    rightLinex.append(centerLinex[i])
                    rightLiney.append(centerLiney[i])
            elif i == len(centerLinex) - 1:
                x = centerLinex[i]
                y = centerLiney[i]
                x_pre = centerLinex[i - 1]
                y_pre = centerLiney[i - 1]
                heading = math.atan2(y - y_pre, x - x_pre)
                length = math.sqrt((y - y_pre) ** 2 + (x - x_pre) ** 2)
                leftLinex.append(x)
                leftLiney.append(y)
                rightLinex.append(x)
                rightLiney.append(y)
            sum_length += length
            col_heading.append(heading)
            col_sum_length.append(sum_length)
            i += 1
        print len(centerLinex), len(centerLiney), len(leftLinex), len(leftLiney), len(rightLinex), \
            len(rightLiney), len(col_heading), len(col_sum_length)
        plt.plot(leftLinex, leftLiney, 'b.-')
        plt.plot(rightLinex, rightLiney, 'g.-')
        plt.plot(centerLinex, centerLiney, 'r.-')
        plt.grid()
        plt.show()
        new_centerLinex = []
        new_centerLiney = []
        new_leftLinex = []
        new_leftLiney = []
        new_rightLinex = []
        new_rightLiney = []
        centerx = []
        centery = []
        leftx = []
        lefty = []
        rightx = []
        righty = []
        new_col_heading = []
        new_col_sum_length = []
        heading = []
        sum_length = []
        k = 0
        while k <= len(centerLinex) - 1:
            if k % 5000 == 0 and k != 0:
                centerx.append(new_centerLinex)
                centery.append(new_centerLiney)
                leftx.append(new_leftLinex)
                lefty.append(new_leftLiney)
                rightx.append(new_rightLinex)
                righty.append(new_rightLiney)
                heading.append(new_col_heading)
                sum_length.append(new_col_sum_length)
                new_centerLinex = [new_centerLinex[-1]]
                new_centerLiney = [new_centerLiney[-1]]
                new_leftLinex = [new_leftLinex[-1]]
                new_leftLiney = [new_leftLiney[-1]]
                new_rightLinex = [new_rightLinex[-1]]
                new_rightLiney = [new_rightLiney[-1]]
                new_col_heading = [new_col_heading[-1]]
                new_col_sum_length = [new_col_sum_length[-1]]
            else:
                new_centerLinex.append(centerLinex[k])
                new_centerLiney.append(centerLiney[k])
                new_leftLinex.append(leftLinex[k])
                new_leftLiney.append(leftLiney[k])
                new_rightLinex.append(rightLinex[k])
                new_rightLiney.append(rightLiney[k])
                new_col_heading.append(col_heading[k])
                new_col_sum_length.append(col_sum_length[k])
            k += 1
        centerx.append(new_centerLinex)
        centery.append(new_centerLiney)
        leftx.append(new_leftLinex)
        lefty.append(new_leftLiney)
        rightx.append(new_rightLinex)
        righty.append(new_rightLiney)
        heading.append(new_col_heading)
        sum_length.append(new_col_sum_length)
        # print len(centerx), centerx, len(centery), centery
        road_feature = cal_road()
        drivejson["header"] = {"revMajor": "", "revMinor": "", "name": "", "version": "", "date": "", "north": 0,
                               "south": 0, "east": 0, "west": 0,
                               "vendor": "Trunk", "geoReference": "+proj=longlat+ellps=WGS84+datum=WGS84+no_defs"}
        drivejson["roads"] = road_feature
        drivejson["junctions"] = []
        # print drivejson
        with open("/media/sf_Desktop/" + str(bag_name[bag_count]) + ".json", "w+") as drivejsonfile:
            json.dump(drivejson, drivejsonfile)
            print str(bag_count + 1) + ":" + str(bag_name[bag_count]) + " transform over!"
        bag_count += 1


def clear_text():
    text.delete('1.0', 'end')


if __name__ == "__main__":
    window = tk.Tk()
    window.title('VectorMap辅助工具')
    window.resizable(width=False, height=False)
    window.geometry('1600x910')
    suffix_input = StringVar()
    topic_input = StringVar()
    check_input = StringVar()

    button1 = tk.Button(window, text='选择bag文件', font=('Arial', 12), width=15, height=2, command=select_bagfile).grid(row=0, column=0, sticky="w")
    button2 = tk.Button(window, text='合并bag文件', font=('Arial', 12), width=15, height=2, command=merge_bagfile).grid(row=0, column=1, sticky="w")
    button3 = tk.Button(window, text='选择shapefile', font=('Arial', 12), width=15, height=2,command=select_shapefile).grid(row=3, column=0, sticky="w")
    button4 = tk.Button(window, text='生成geojson', font=('Arial', 12), width=15, height=2, command=save_geojson).grid(row=3, column=3, sticky="w")
    button5 = tk.Button(window, text='生成drivejson', font=('Arial', 12), width=15, height=2, command=bag_drivejson).grid(row=3, column=4, sticky="w")
    button6 = tk.Button(window, text='shapefile检查', font=('Arial', 12), width=15, height=2, command=check).grid(row=3,column=1,sticky="w")
    button7 = tk.Button(window, text='shapefile改正', font=('Arial', 12), width=15, height=2, command=correct).grid(row=3,column=2,sticky="w")
    button8 = tk.Button(window, text='生成csv', font=('Arial', 12), width=15, height=2, command=save_csv).grid(row=0,column=2,sticky="w")
    button9 = tk.Button(window, text='生成轨迹点', font=('Arial', 12), width=15, height=2,command=generate_trajectorypoint).grid(row=0, column=3, sticky="w")
    button10 = tk.Button(window, text='生成轨迹线', font=('Arial', 12), width=15, height=2,command=generate_trajectorypolyline).grid(row=0, column=4, sticky="w")
    button11 = tk.Button(window, text='清空文本', font=('Arial', 12), width=15, height=2, command=clear_text).grid(row=10,column=5,sticky="w")
    button12 = tk.Button(window, text='选择geojson', font=('Arial', 12), width=15, height=2, command=select_geojson).grid(row=10, column=0, sticky="w")
    button13 = tk.Button(window, text='选择drivejson', font=('Arial', 12), width=15, height=2,command=select_drivejson).grid(row=10, column=1, sticky="w")
    button14 = tk.Button(window, text='生成中心线', font=('Arial', 12), width=15, height=2,command=generate_centerline).grid(row=10, column=2, sticky="w")
    button15 = tk.Button(window, text='生成车道线', font=('Arial', 12), width=15, height=2, command=generate_polyline).grid(row=10, column=3, sticky="w")
    button16 = tk.Button(window, text='生成掩膜', font=('Arial', 12), width=15, height=2, command=generate_polygon).grid(row=10, column=4, sticky="w")

    topic_label = Label(text="话题名称", font=('Arial', 12), width=15, height=2).grid(row=1, column=0, sticky="w")
    distance_lable_down = Label(text="检查阈值下限", font=('Arial', 12), width=15, height=2).grid(row=7, column=0, sticky="w")
    distance_entry_down = Entry(window)
    distance_entry_down.grid(row=7, column=1, columnspan=2, sticky="w")
    distance_lable_up = Label(text="检查阈值上限", font=('Arial', 12), width=15, height=2).grid(row=7, column=2, sticky="w")
    distance_entry_up = Entry(window)
    distance_entry_up.grid(row=7, column=3, columnspan=2, sticky="w")
    direction_lable = Label(text="检查方向", font=('Arial', 12), width=15, height=2).grid(row=7, column=4, sticky="w")
    direction_entry = Entry(window)
    direction_entry.grid(row=7, column=5, columnspan=2, sticky="w")
    angle_lable = Label(text="衔接角阈值", font=('Arial', 12), width=15, height=2).grid(row=8, column=0, sticky="w")
    angle_entry = Entry(window)
    angle_entry.grid(row=8, column=1, columnspan=2, sticky="w")
    point_lable = Label(text="轨迹拟合度", font=('Arial', 12), width=15, height=2).grid(row=0, column=5, sticky="w")
    point_entry = Entry(window)
    point_entry.grid(row=0, column=6, columnspan=2, sticky="w")
    suffix_label = Label(text="文件扩展名", font=('Arial', 12), width=16, height=2).grid(row=9, column=0, sticky="w")
    radiobutton1 = tk.Radiobutton(window, text='gnss', variable=topic_input, value='/trunk_info/gnss',font=('Arial', 12), width=15, height=2).grid(row=1, column=1, sticky="w")
    radiobutton2 = tk.Radiobutton(window, text='ins', variable=topic_input, value='/trunk_info/gnss_ins',font=('Arial', 12), width=15, height=2).grid(row=1, column=2, sticky="w")
    radiobutton3 = tk.Radiobutton(window, text='imu', variable=topic_input, value='/trunk_info/imu', font=('Arial', 12),width=15, height=2).grid(row=1, column=3, sticky="w")
    radiobutton4 = tk.Radiobutton(window, text='state', variable=topic_input, value='/pnc_msgs/vehicle_state',font=('Arial', 12), width=15, height=2).grid(row=1, column=4, sticky="w")
    radiobutton5 = tk.Radiobutton(window, text='info', variable=topic_input, value='/pnc_msgs/vehicle_info',font=('Arial', 12), width=15, height=2).grid(row=1, column=5, sticky="w")
    radiobutton6 = tk.Radiobutton(window, text='locate', variable=topic_input, value='/localization',font=('Arial', 12), width=15, height=2).grid(row=1, column=6, sticky="w")
    radiobutton7 = tk.Radiobutton(window, text='ini', variable=suffix_input, value='ini', font=('Arial', 12), width=15,height=2).grid(row=9, column=1, sticky="w")
    radiobutton8 = tk.Radiobutton(window, text='tmp', variable=suffix_input, value='tmp', font=('Arial', 12), width=15,height=2).grid(row=9, column=2, sticky="w")
    radiobutton9 = tk.Radiobutton(window, text='inj', variable=suffix_input, value='inj', font=('Arial', 12), width=15,height=2).grid(row=9, column=3, sticky="w")
    radiobutton10 = tk.Radiobutton(window, text='json', variable=suffix_input, value='json', font=('Arial', 12),width=15, height=2).grid(row=9, column=4, sticky="w")
    radiobutton11 = tk.Radiobutton(window, text='angle', variable=check_input, value='check_angle', font=('Arial', 12),width=15, height=2).grid(row=8, column=2, sticky="w")

    text = scrolledtext.ScrolledText(window, font=('Arial', 16), width=132, height=25)
    text.grid(row=11, column=0, columnspan=8, sticky="e")

    progressbar = ttk.Progressbar(window, orient='horizontal', length=1590, mode='determinate')
    progressbar.grid(row=12, column=0, columnspan=8, sticky="w")
    window.mainloop()
