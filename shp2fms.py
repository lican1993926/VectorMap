# -*- coding: utf-8 -*-
import json
import math
import shapefile
import tkinter as tk
from tkinter import filedialog
def select_json():
    new_centerLine_y = []
    new_centerLine_x = []
    new_centerLine_heading = ['heading']
    file_name = filedialog.askopenfilename(title='请选择json文件', filetypes=[('json', '*.json'), ('All Files', '*')]
                                           ,initialdir='C:\\Users\\Administrator\\Desktop')
    json_file = open(file_name)
    map = json.load(json_file)
    for point in map:
        new_centerLine_y.append(float(point['pos']['latitude']+4317123))
        new_centerLine_x.append(float(point['pos']['longitude']+565123))
        if point.has_key=='heading':
            new_centerLine_heading.append(int(point['heading']))
    ployLine = shapefile.Writer(target="/media/sf_Desktop/path.shp", shapeType=1, autoBalance=1)
    ployLine.field('utm_east', 'F', decimal=10)
    ployLine.field('utm_north', 'F', decimal=10)
    ployLine.field('heading', 'N', decimal=5)
    # print new_centerLine_x
    if len(new_centerLine_x) == len(new_centerLine_y) and len(new_centerLine_x) != 0:
        for r in range(len(new_centerLine_x)):
            ployLine.point(new_centerLine_x[r], new_centerLine_y[r])
            ployLine.record(new_centerLine_x[r],new_centerLine_y[r])
    ployLine.close()
def generate_bufferflip():
    global buffer
    global buffer_flip
    filename_path_shapefile = filedialog.askopenfilename(title='请选择shp文件',filetypes=[('shp', '*.shp'), ('All Files', '*')],initialdir='/project')
    inputfilename_path = filename_path_shapefile.replace('\\','\\\\')
    # arcpy.env.workspace = os.path.realpath(__file__)
    # climateBackup = "backups/jt_j7_0918.shp"
    # arcpy.Densify_edit('jt_test_1.shp', "DISTANCE", "1.64041994751 feet")
    reader = shapefile.Reader(inputfilename_path)
    field_names = []
    fields = reader.fields[1:]
    for field in fields:
        field_names.append(field[0])
    shape_records = reader.shapeRecords()
    buffer = []
    for sr in shape_records:
        record = sr.record
        record_first = []
        for value in record:
            if value == None:
                new_value = 0
                record_first.append(new_value)
            else:
                record_first.append(value)
        atr = dict(zip(field_names, record_first))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))
    sub_buffer= []
    buffer_flip = []
    buffer.sort(key=lambda buffer:buffer['properties']['pathID'],reverse=False)
    # print buffer
    k = 0
    while k < len(buffer)-1:
        if buffer[k]['properties']['pathID'] == buffer[k + 1]['properties']['pathID']:
            sub_buffer.append(buffer[k])
            if k == len(buffer) - 2:
                sub_buffer.append(buffer[k+1])
                sub_buffer.sort(key=lambda sub_buffer: sub_buffer['properties']['taskID'], reverse=False)
                m = 0
                new_sub_buffer = []
                sub_buffer_flip = []
                while m <= len(sub_buffer) - 1:
                    if m < len(sub_buffer) - 1:
                        if sub_buffer[m]['properties']['taskID'] == sub_buffer[m + 1]['properties']['taskID']:
                            sub_buffer_flip.append(sub_buffer[m])
                        elif sub_buffer[m]['properties']['taskID'] != sub_buffer[m + 1]['properties']['taskID']:
                            sub_buffer_flip.append(sub_buffer[m])
                            sub_buffer_flip.sort(key=lambda sub_buffer_flip: sub_buffer_flip['properties']['taskTag'], reverse=False)
                            new_sub_buffer.extend(sub_buffer_flip)
                            # m += len(sub_buffer_flip)
                            sub_buffer_flip = []
                    else:
                        sub_buffer_flip.append(sub_buffer[m])
                        sub_buffer_flip.sort(key=lambda sub_buffer_flip: sub_buffer_flip['properties']['taskTag'],reverse=False)
                        new_sub_buffer.extend(sub_buffer_flip)
                    m += 1
                # print new_sub_buffer
                buffer_flip.append(new_sub_buffer)
        elif buffer[k]['properties']['pathID'] != buffer[k+1]['properties']['pathID']:
            sub_buffer.append(buffer[k])
            sub_buffer.sort(key=lambda sub_buffer:sub_buffer['properties']['taskID'], reverse=False)
            m = 0
            new_sub_buffer = []
            sub_buffer_flip = []
            while m <= len(sub_buffer)-1:
                if m < len(sub_buffer)-1:
                    if sub_buffer[m]['properties']['taskID'] == sub_buffer[m+1]['properties']['taskID']:
                        sub_buffer_flip.append(sub_buffer[m])
                    elif sub_buffer[m]['properties']['taskID'] != sub_buffer[m+1]['properties']['taskID']:
                        sub_buffer_flip.append(sub_buffer[m])
                        sub_buffer_flip.sort(key=lambda sub_buffer_flip: sub_buffer_flip['properties']['taskTag'],reverse=False)
                        new_sub_buffer.extend(sub_buffer_flip)
                        # m += len(sub_buffer_flip)
                        sub_buffer_flip = []
                else:
                    sub_buffer_flip.append(sub_buffer[m])
                    sub_buffer_flip.sort(key=lambda sub_buffer_flip: sub_buffer_flip['properties']['taskTag'],reverse=False)
                    new_sub_buffer.extend(sub_buffer_flip)
                m += 1
            # print new_sub_buffer
            buffer_flip.append(new_sub_buffer)
            sub_buffer = []
            if k == len(buffer) - 2:
                sub_buffer.append(buffer[k+1])
                sub_buffer.sort(key=lambda sub_buffer: sub_buffer['properties']['taskID'], reverse=False)
                m = 0
                new_sub_buffer = []
                sub_buffer_flip = []
                while m <= len(sub_buffer) - 1:
                    if m < len(sub_buffer) - 1:
                        if sub_buffer[m]['properties']['taskID'] == sub_buffer[m + 1]['properties']['taskID']:
                            sub_buffer_flip.append(sub_buffer[m])
                        elif sub_buffer[m]['properties']['taskID'] != sub_buffer[m + 1]['properties']['taskID']:
                            sub_buffer_flip.append(sub_buffer[m])
                            sub_buffer_flip.sort(
                                key=lambda sub_buffer_flip: sub_buffer_flip['properties']['taskTag'], reverse=False)
                            new_sub_buffer.extend(sub_buffer_flip)
                            # m += len(sub_buffer_flip)
                            sub_buffer_flip = []
                    else:
                        sub_buffer_flip.append(sub_buffer[m])
                        sub_buffer_flip.sort(key=lambda sub_buffer_flip: sub_buffer_flip['properties']['taskTag'],
                                             reverse=False)
                        new_sub_buffer.extend(sub_buffer_flip)
                    m += 1
                # print new_sub_buffer
                buffer_flip.append(new_sub_buffer)
        # print buffer_flip
        k += 1

def generate_huaweijson():
    i = 0
    while i <= len(buffer_flip)-1:
        tag = 0
        path = []
        col_heading = []
        p = 0
        while p <= len(buffer_flip[i]) - 1:
            pathID = buffer_flip[i][p]['properties']['pathID']
            taskID = buffer_flip[i][p]['properties']['taskID']
            if buffer_flip[i][p]['properties']['achType'] == 0:
                achieve_type = "STRAIGHT"
            elif buffer_flip[i][p]['properties']['achType'] == 1:
                achieve_type = "LANECHANGE"
            elif buffer_flip[i][p]['properties']['achType'] == 2:
                achieve_type = "TURN"
            if buffer_flip[i][p]['properties']['direction'] == 0:
                direction = 1
            elif buffer_flip[i][p]['properties']['direction'] == 1:
                direction = 2
            # print str(pathID) + '_' + str(taskID)+ '_' + str(tag) + '_' + str(direction) + '_' + achieve_type
            h= 0
            while h<= len(buffer_flip[i][p]['geometry']['coordinates']) - 1:
                x = round(buffer_flip[i][p]['geometry']['coordinates'][h][0] - 565123, 3)
                y = round(buffer_flip[i][p]['geometry']['coordinates'][h][1] - 4317123, 3)
                if h <= len(buffer_flip[i][p]['geometry']['coordinates'])-1:
                    if tag == 0 or tag == 1 or tag == 3 or tag == 4:
                        if h == 0:
                            x_diff = buffer_flip[i][p]['geometry']['coordinates'][h + 1][0] - buffer_flip[i][p]['geometry']['coordinates'][h][0]
                            y_diff = buffer_flip[i][p]['geometry']['coordinates'][h + 1][1] - buffer_flip[i][p]['geometry']['coordinates'][h][1]
                            angle = math.acos(y_diff/math.sqrt(x_diff**2+y_diff**2))
                            angle_ = math.acos(x_diff/math.sqrt(x_diff**2+y_diff**2))
                        elif 0 < h < len(buffer_flip[i][p]['geometry']['coordinates']) - 1:
                            x_diff_pro = buffer_flip[i][p]['geometry']['coordinates'][h][0] - buffer_flip[i][p]['geometry']['coordinates'][h - 1][0]
                            y_diff_pro = buffer_flip[i][p]['geometry']['coordinates'][h][1] - buffer_flip[i][p]['geometry']['coordinates'][h - 1][1]
                            x_diff_next = buffer_flip[i][p]['geometry']['coordinates'][h + 1][0] - buffer_flip[i][p]['geometry']['coordinates'][h][0]
                            y_diff_next = buffer_flip[i][p]['geometry']['coordinates'][h + 1][1] - buffer_flip[i][p]['geometry']['coordinates'][h][1]
                            angle1 = math.acos(y_diff_pro/math.sqrt(x_diff_pro**2+y_diff_pro**2))
                            angle2 = math.acos(y_diff_next/math.sqrt(x_diff_next**2+y_diff_next**2))
                            angle3 = math.acos(x_diff_pro/math.sqrt(x_diff_pro**2+y_diff_pro**2))
                            angle4 = math.acos(x_diff_next/math.sqrt(x_diff_next**2+y_diff_next**2))
                            angle = (angle1+angle2)/2
                            angle_ = (angle3+angle4)/2
                        else:
                            x_diff = buffer_flip[i][p]['geometry']['coordinates'][h][0] - buffer_flip[i][p]['geometry']['coordinates'][h-1][0]
                            y_diff = buffer_flip[i][p]['geometry']['coordinates'][h][1] - buffer_flip[i][p]['geometry']['coordinates'][h-1][1]
                            angle = math.acos(y_diff / math.sqrt(x_diff ** 2 + y_diff ** 2))
                            angle_ = math.acos(x_diff / math.sqrt(x_diff ** 2 + y_diff ** 2))
                        if direction == 1:
                            if angle_ > math.pi/2:
                                new_angle = 2*math.pi - angle
                                heading = int(new_angle * 14400 / math.pi)
                                print new_angle * 180 / math.pi, str(pathID) + '_' + str(taskID)+ '_' + str(tag) + '_' + str(direction) + '_' + achieve_type
                            else:
                                heading = int(angle * 14400 / math.pi)
                                print new_angle * 180 / math.pi, str(pathID) + '_' + str(taskID) + '_' + str(tag) + '_' + str(direction) + '_' + achieve_type
                        elif direction == 2:
                            if angle_ > math.pi/2:
                                new_angle = 2 * math.pi - angle
                                if new_angle > math.pi:
                                    new_angle -= math.pi
                                else:
                                    new_angle += math.pi
                                print new_angle * 180 / math.pi, str(pathID) + '_' + str(taskID)+ '_' + str(tag) + '_' + str(direction) + '_' + achieve_type
                                heading = int(new_angle * 14400 / math.pi)
                            else:
                                if angle > math.pi:
                                    angle -= math.pi
                                else:
                                    angle += math.pi
                                print angle * 180 / math.pi, str(pathID) + '_' + str(taskID)+ '_' + str(tag) + '_' + str(direction) + '_' + achieve_type
                                heading = int(angle * 14400 / math.pi)
                    elif tag == 2 or tag == 5:
                        # print col_heading
                        heading = col_heading[-1]
                if tag == 0:
                    if h == 0:
                        key_point = {"direction":direction,"pos": {"longitude": x, "latitude": y, "elevation": 0}, "heading": heading,
                                     "type": achieve_type, "laneId": pathID}
                    elif 0 < h < len(buffer_flip[i][p]['geometry']['coordinates']) - 1:
                        key_point = {}
                    else:
                        key_point = {"pos": {"longitude": x, "latitude": y, "elevation": 0}, "heading": heading,"laneId": pathID}
                elif tag == 1 or tag == 2:
                    if h == 0:
                        key_point = {"direction":direction,"pos": {"longitude": x, "latitude": y, "elevation": 0},"heading":heading, "type": achieve_type,"laneId": pathID}
                    elif 0 < h < len(buffer_flip[i][p]['geometry']['coordinates'])-1:
                        key_point = {"pos": {"longitude": x, "latitude": y, "elevation": 0},"heading": heading,"laneId": pathID}
                    else:
                        key_point = {"pos": {"longitude": x, "latitude": y, "elevation": 0},"heading": heading,"laneId": pathID}
                elif tag == 4 or tag == 5:
                    if h == 0:
                        key_point = {}
                    elif h == 1:
                        key_point = {"direction":direction,"pos": {"longitude": x, "latitude": y, "elevation": 0}, "heading": heading,
                                     "type": achieve_type, "laneId": pathID}
                    elif 0 < h < len(buffer_flip[i][p]['geometry']['coordinates']) - 1:
                        key_point = {"pos": {"longitude": x, "latitude": y, "elevation": 0}, "heading": heading,
                                     "laneId": pathID}
                    else:
                        key_point = {"pos": {"longitude": x, "latitude": y, "elevation": 0}, "heading": heading,"laneId": pathID}
                elif tag == 3:
                    if h == 0:
                        key_point = {}
                    elif h == 1:
                        key_point = {"direction":direction,"pos": {"longitude": x, "latitude": y, "elevation": 0}, "heading": heading,
                                     "type": achieve_type, "laneId": pathID}
                    elif 0 < h < len(buffer_flip[i][p]['geometry']['coordinates']) - 1:
                        key_point = {}
                    else:
                        key_point = {"pos": {"longitude": x, "latitude": y, "elevation": 0}, "heading": heading,"laneId": pathID}
                if key_point!= {}:
                    path.append(key_point)
                    col_heading.append(heading)
                h += 1
            with open('FMS' + '_' + str(pathID) + '_' + str(taskID) + '.json', 'w') as f:
                f.write(json.dumps(path, indent=1))
            if p < len(buffer_flip[i]) - 1:
                if buffer_flip[i][p]['properties']['taskID'] != buffer_flip[i][p + 1]['properties']['taskID'] and buffer_flip[i][p + 1]['properties']['achType'] == 0:
                    tag = 0
                    path = []
                elif buffer_flip[i][p]['properties']['taskID'] != buffer_flip[i][p + 1]['properties']['taskID'] and buffer_flip[i][p + 1]['properties']['achType'] == 2:
                    tag = 1
                    path = []
                elif buffer_flip[i][p]['properties']['taskID'] != buffer_flip[i][p + 1]['properties']['taskID'] and buffer_flip[i][p + 1]['properties']['achType'] == 1:
                    tag = 2
                    path = []
                elif buffer_flip[i][p]['properties']['taskID'] == buffer_flip[i][p + 1]['properties']['taskID'] and buffer_flip[i][p + 1]['properties']['achType'] == 0:
                    tag = 3
                elif buffer_flip[i][p]['properties']['taskID'] == buffer_flip[i][p + 1]['properties']['taskID'] and buffer_flip[i][p + 1]['properties']['achType'] == 2:
                    tag = 4
                elif buffer_flip[i][p]['properties']['taskID'] == buffer_flip[i][p + 1]['properties']['taskID'] and buffer_flip[i][p + 1]['properties']['achType'] == 1:
                    tag = 5
            p += 1
        i+=1

if __name__ == "__main__":
    window = tk.Tk()
    window.title('shp2fms Tool')
    window.geometry('500x300')
    button1 = tk.Button(window, text='选择path', font=('Arial', 12), width=10, height=1, command=select_json)
    button2 = tk.Button(window, text='选择shp', font=('Arial', 12), width=10, height=1, command=generate_bufferflip)
    button3 = tk.Button(window, text='生成huaweijson', font=('Arial', 12), width=10, height=1, command=generate_huaweijson)
    button1.pack()
    button2.pack()
    button3.pack()
    window.mainloop()