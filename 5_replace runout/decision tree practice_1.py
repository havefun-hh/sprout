# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 12:47:31 2020

@author: admin
"""
"""1:1特征1标签"""
import os
import sys
root_path = os.path.abspath("D:/Anaconda files/calculate assemble deformation/")
if root_path not in sys.path:
    sys.path.append(root_path)

# 导入python操作mysql的模块
import pymysql
import pandas as pd
import numpy as np
from Prediction import Prediction as pre
from Replace import Replace as rep
from sklearn import tree
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt


def predata_r(data, Y_pred_r):    #predict data radial
    x = []
    y = []
    for i in range(len(data[:, 0])):
        theta = np.arctan(data[:, 2] / data[:, 1])
        x.append(data[i, 1] + Y_pred_r[i] * np.cos(theta))
        y.append(data[i, 2] + Y_pred_r[i] * np.sin(theta))
    x = np.array(x).reshape(-1, 1)
    x = np.squeeze(x)
    y = np.array(y).reshape(-1, 1)
    y = np.squeeze(y)
    data = np.dstack((x, y))
    data = np.squeeze(data)
    return data

"""==============================================================train=========================================================="""
H1 = 805 - 118
H2 = 328 + 65 - 5
ad_part1_runout = 'G:/190708-190712data/MNJ-HPC-001ZP2-20190708.csv'
ad_part2_runout = 'G:/190708-190712data/MNJ-HPT-001ZP1-20190708.csv'
ad_part1_flat_node_up = "G:/19.12.25whole model (less grids)/Step3----part1_flat_node_data_up.csv"
ad_part2_flat_node_down = "G:/19.12.25whole model (less grids)/Step3----part2_flat_node_data_down.csv"
ad_part1_radial_node_up = "G:/19.12.25whole model (less grids)/Step3----part1_radial_node_data_up.csv"
ad_part2_radial_node_down = "G:/19.12.25whole model (less grids)/Step3----part2_radial_node_data_down.csv"


part1_flat_runout_up = pre.idata(ad_part1_runout, [1])
part1_flat_runout_coordinate_up = pre.gcfl(206.5 / 2, part1_flat_runout_up, 0)
part1_normal_vector_up = pre.planefit(part1_flat_runout_coordinate_up)
part1_flat_node_data_up = pre.idata(ad_part1_flat_node_up, [0,1,2,3])
new_part1_flat_node_data_up = rep.frure(206.5 / 2, part1_normal_vector_up[0], part1_normal_vector_up[1], part1_normal_vector_up[2], part1_normal_vector_up[3], part1_flat_runout_up, part1_flat_node_data_up, 0)
new_part1_flat_runout_up = new_part1_flat_node_data_up[:, 3]
part2_flat_runout_down = -pre.idata(ad_part2_runout, [4])
part2_flat_runout_coordinate_down = pre.gcfl(206.5 / 2, part2_flat_runout_down, 0)
part2_normal_vector_down = pre.planefit(part2_flat_runout_coordinate_down)
part2_flat_node_data_down = pre.idata(ad_part2_flat_node_down, [0,1,2,3])
new_part2_flat_node_data_down = rep.frure(206.5 / 2, part2_normal_vector_down[0], part2_normal_vector_down[1], part2_normal_vector_down[2], part2_normal_vector_down[3], part2_flat_runout_down, part2_flat_node_data_down, 0)
new_part2_flat_runout_down = new_part2_flat_node_data_down[:, 3]

part1_radial_runout_up = -pre.idata(ad_part1_runout, [2])
part1_radial_runout_coordinate_up = pre.gcra(200 / 2, part1_radial_runout_up, 0)
part1_circle_center_up = pre.circ(part1_radial_runout_coordinate_up)
part1_radial_node_data_up = pre.idata(ad_part1_radial_node_up, [0,1,2,3])
new_part1_radial_runout_up = rep.rrure3(part1_radial_runout_up, part1_radial_node_data_up)
part2_radial_runout_down = pre.idata(ad_part2_runout, [3])
part2_radial_runout_coordinate_down = pre.gcra(200 / 2, part2_radial_runout_down, 0)
part2_circle_center_down = pre.circ(part2_radial_runout_coordinate_down[:, 0:3])
part2_radial_node_data_down = pre.idata(ad_part2_radial_node_down, [0,1,2,3])
new_part2_radial_runout_down = rep.rrure3(part2_radial_runout_down, part2_radial_node_data_down)

dif_f = np.stack((new_part1_flat_runout_up, new_part2_flat_runout_down, new_part1_flat_runout_up - new_part2_flat_runout_down), axis=1)
dif_r = np.stack((new_part1_radial_runout_up, new_part2_radial_runout_down, new_part1_radial_runout_up - new_part2_radial_runout_down), axis=1)

#joint
#端面
part1_flat_data_up = np.array(pd.read_csv("G:/19.12.25whole model (less grids)/Step5----replaced(0)/Step8——仿真结果/1.8_inp4圆心对准，有跳动，过盈0，大变形，加重力， 弱弹簧3300N(frictional)/part1端面.txt", sep='\t'))
part2_flat_data_down = np.array(pd.read_csv("G:/19.12.25whole model (less grids)/Step5----replaced(0)/Step8——仿真结果/1.8_inp4圆心对准，有跳动，过盈0，大变形，加重力， 弱弹簧3300N(frictional)/part2端面.txt", sep='\t'))
part1_flat_data_up = np.squeeze(part1_flat_data_up)
part2_flat_data_down =np.squeeze(part2_flat_data_down)
disp_f = np.stack((part1_flat_data_up[:, 4], part2_flat_data_down[:, 4]), axis=1)
#止口
part1_radial_data_x_up = np.array(pd.read_csv("G:/19.12.25whole model (less grids)/Step5----replaced(0)/Step8——仿真结果/1.8_inp4圆心对准，有跳动，过盈0，大变形，加重力， 弱弹簧3300N(frictional)/part1止口x.txt", sep='\t', usecols=[0,1,2,4]))
part1_radial_data_y_up = np.array(pd.read_csv("G:/19.12.25whole model (less grids)/Step5----replaced(0)/Step8——仿真结果/1.8_inp4圆心对准，有跳动，过盈0，大变形，加重力， 弱弹簧3300N(frictional)/part1止口y.txt", sep='\t', usecols=[0,1,2,4]))
part2_radial_data_x_down = np.array(pd.read_csv("G:/19.12.25whole model (less grids)/Step5----replaced(0)/Step8——仿真结果/1.8_inp4圆心对准，有跳动，过盈0，大变形，加重力， 弱弹簧3300N(frictional)/part2止口x.txt", sep='\t', usecols=[0,1,2,4]))
part2_radial_data_y_down = np.array(pd.read_csv("G:/19.12.25whole model (less grids)/Step5----replaced(0)/Step8——仿真结果/1.8_inp4圆心对准，有跳动，过盈0，大变形，加重力， 弱弹簧3300N(frictional)/part2止口y.txt", sep='\t', usecols=[0,1,2,4]))
part1_radial_data_x_up = np.squeeze(part1_radial_data_x_up)
part1_radial_data_y_up = np.squeeze(part1_radial_data_y_up)
part2_radial_data_x_down = np.squeeze(part2_radial_data_x_down)
part2_radial_data_y_down = np.squeeze(part2_radial_data_y_down)
part1_radial_disp_up = np.sqrt((part1_radial_data_x_up[:, 3] ** 2 + part1_radial_data_y_up[:, 3] ** 2))
part2_radial_disp_down = np.sqrt((part2_radial_data_x_down[:, 3] ** 2 + part2_radial_data_y_down[:, 3] ** 2))
disp_r = np.stack((part1_radial_disp_up, part2_radial_disp_down), axis=1)


features_f = pd.DataFrame(columns=['p1_runout_f', 'p2_runout_f', 'dif_runout_f'])   #p1_f:part1 flat runout;待加入差分形貌的分步特征！！！
features_r = pd.DataFrame(columns=['p1_runout_r', 'p2_runout_r', 'dif_runout_r'])
target_f = pd.DataFrame(columns=['p1_disp_f', 'p2_disp_f'])
target_r = pd.DataFrame(columns=['p1_disp_r', 'p2_disp_r'])

for i in range(len(dif_f)):
    features_f.loc[i] = dif_f[i]
for i in range(len(dif_r)):
    features_r.loc[i] = dif_r[i]
for i in range(len(disp_f)):
    target_f.loc[i] = disp_f[i]
for i in range(len(disp_r)):
    target_r.loc[i] = disp_r[i]


X_train_f = dif_f.tolist()
Y_train_f = disp_f.tolist()
X_train_r = dif_r.tolist()
Y_train_r = disp_r.tolist()

"""==============================================================test=========================================================="""
part1_flat_runout_up = pre.idata(ad_part1_runout, [1])
part1_flat_runout_coordinate_up = pre.gcfl(206.5 / 2, part1_flat_runout_up, 0)
part1_normal_vector_up = pre.planefit(part1_flat_runout_coordinate_up)
part1_flat_node_data_up = pre.idata(ad_part1_flat_node_up, [0,1,2,3])
new_part1_flat_node_data_up = rep.frure(206.5 / 2, part1_normal_vector_up[0], part1_normal_vector_up[1], part1_normal_vector_up[2], part1_normal_vector_up[3], part1_flat_runout_up, part1_flat_node_data_up, 0)
new_part1_flat_runout_up = new_part1_flat_node_data_up[:, 3]
part2_flat_runout_down = -pre.idata(ad_part2_runout, [4])
part2_flat_runout_coordinate_down = pre.gcfl(206.5 / 2, part2_flat_runout_down, 0)
part2_normal_vector_down = pre.planefit(part2_flat_runout_coordinate_down)
part2_flat_node_data_down = pre.idata(ad_part2_flat_node_down, [0,1,2,3])
new_part2_flat_node_data_down = rep.frure(206.5 / 2, part2_normal_vector_down[0], part2_normal_vector_down[1], part2_normal_vector_down[2], part2_normal_vector_down[3], part2_flat_runout_down, part2_flat_node_data_down, 0)
new_part2_flat_runout_down = new_part2_flat_node_data_down[:, 3]

part1_radial_runout_up = -pre.idata(ad_part1_runout, [2])
part1_radial_runout_coordinate_up = pre.gcra(200 / 2, part1_radial_runout_up, 0)
part1_circle_center_up = pre.circ(part1_radial_runout_coordinate_up)
part1_radial_node_data_up = pre.idata(ad_part1_radial_node_up, [0,1,2,3])
new_part1_radial_runout_up = rep.rrure3(part1_radial_runout_up, part1_radial_node_data_up)
part2_radial_runout_down = pre.idata(ad_part2_runout, [3])
part2_radial_runout_coordinate_down = pre.gcra(200 / 2, part2_radial_runout_down, 0)
part2_circle_center_down = pre.circ(part2_radial_runout_coordinate_down[:, 0:3])
part2_radial_node_data_down = pre.idata(ad_part2_radial_node_down, [0,1,2,3])
new_part2_radial_runout_down = rep.rrure3(part2_radial_runout_down, part2_radial_node_data_down)

dif_f = np.stack((new_part1_flat_runout_up, new_part2_flat_runout_down, new_part1_flat_runout_up - new_part2_flat_runout_down), axis=1)
dif_r = np.stack((new_part1_radial_runout_up, new_part2_radial_runout_down, new_part1_radial_runout_up - new_part2_radial_runout_down), axis=1)

#joint
#端面
part1_flat_data_up = np.array(pd.read_csv("G:/19.12.25whole model (less grids)/Step5----replaced(90)/Step8——仿真结果/1.8_inp4圆心对准，有跳动，过盈0，大变形，加重力， 弱弹簧3300N(frictional)/part1端面.txt", sep='\t'))
part2_flat_data_down = np.array(pd.read_csv("G:/19.12.25whole model (less grids)/Step5----replaced(90)/Step8——仿真结果/1.8_inp4圆心对准，有跳动，过盈0，大变形，加重力， 弱弹簧3300N(frictional)/part2端面.txt", sep='\t'))
part1_flat_data_up = np.squeeze(part1_flat_data_up)
part2_flat_data_down =np.squeeze(part2_flat_data_down)
disp_f = np.stack((part1_flat_data_up[:, 4], part2_flat_data_down[:, 4]), axis=1)
#止口
part1_radial_data_x_up = np.array(pd.read_csv("G:/19.12.25whole model (less grids)/Step5----replaced(90)/Step8——仿真结果/1.8_inp4圆心对准，有跳动，过盈0，大变形，加重力， 弱弹簧3300N(frictional)/part1止口x.txt", sep='\t', usecols=[0,1,2,4]))
part1_radial_data_y_up = np.array(pd.read_csv("G:/19.12.25whole model (less grids)/Step5----replaced(90)/Step8——仿真结果/1.8_inp4圆心对准，有跳动，过盈0，大变形，加重力， 弱弹簧3300N(frictional)/part1止口y.txt", sep='\t', usecols=[0,1,2,4]))
part2_radial_data_x_down = np.array(pd.read_csv("G:/19.12.25whole model (less grids)/Step5----replaced(90)/Step8——仿真结果/1.8_inp4圆心对准，有跳动，过盈0，大变形，加重力， 弱弹簧3300N(frictional)/part2止口x.txt", sep='\t', usecols=[0,1,2,4]))
part2_radial_data_y_down = np.array(pd.read_csv("G:/19.12.25whole model (less grids)/Step5----replaced(90)/Step8——仿真结果/1.8_inp4圆心对准，有跳动，过盈0，大变形，加重力， 弱弹簧3300N(frictional)/part2止口y.txt", sep='\t', usecols=[0,1,2,4]))
part1_radial_data_x_up = np.squeeze(part1_radial_data_x_up)
part1_radial_data_y_up = np.squeeze(part1_radial_data_y_up)
part2_radial_data_x_down = np.squeeze(part2_radial_data_x_down)
part2_radial_data_y_down = np.squeeze(part2_radial_data_y_down)
part1_radial_disp_up = np.sqrt((part1_radial_data_x_up[:, 3] ** 2 + part1_radial_data_y_up[:, 3] ** 2))
part2_radial_disp_down = np.sqrt((part2_radial_data_x_down[:, 3] ** 2 + part2_radial_data_y_down[:, 3] ** 2))
disp_r = np.stack((part1_radial_disp_up, part2_radial_disp_down), axis=1)


X_test_f = dif_f.tolist()
Y_test_f = disp_f.tolist()
X_test_r = dif_r.tolist()
Y_test_r = disp_r.tolist()

"""==============================================================predict=========================================================="""
clf_f = tree.DecisionTreeRegressor()
clf_f = clf_f.fit(X_train_f, Y_train_f)
Y_pred_f = clf_f.predict(X_test_f)
Y_test_1_f = np.array(Y_test_f)
mean_squared_error(Y_test_f, Y_pred_f)

clf_r = tree.DecisionTreeRegressor()
clf_r = clf_r.fit(X_train_r, Y_train_r)
Y_pred_r = clf_r.predict(X_test_r)
Y_test_1_r = np.array(Y_test_r)
mean_squared_error(Y_test_r, Y_pred_r)


# plt.figure(1)
# plt.scatter(X_test_f, Y_test_f, s=1)
# plt.scatter(X_test_f, Y_pred_f, s=1)
# plt.figure(2)
# plt.scatter(X_test_f, Y_test_f, s=1)
# plt.figure(3)
# plt.scatter(X_test_f, Y_pred_f, s=1, c='red')
# plt.figure(4)
# plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
# plt.rcParams['axes.unicode_minus'] = False
# plt.subplot(1, 2, 1)
# plt.scatter(X_test_f, Y_test_f, s=1)
# plt.xlabel('端跳形貌差分值/mm', size=15)
# plt.ylabel('端面变形实际差分值/mm', size=15, rotation=90)
# plt.title('真实结果（150°相位）', size=20, loc = 'center')
# plt.subplot(1, 2, 2)
# plt.scatter(X_test_f, Y_pred_f, s=1, c='red')
# plt.xlabel('端跳形貌差分值/mm', size=15)
# plt.ylabel('端面变形预测差分值/mm', size=15, rotation=90)
# plt.title('预测结果（150°相位）', size=20, loc = 'center')
# plt.figure(5)
# plt.subplot(1, 2, 1)
# plt.scatter(X_test_r, Y_test_r, s=1)
# plt.xlabel('径跳形貌差分值/mm', size=15)
# plt.ylabel('止口变形实际差分值/mm', size=15, rotation=90)
# plt.title('真实结果（90°相位）', size=20, loc = 'center')
# plt.subplot(1, 2, 2)
# plt.scatter(X_test_r, Y_pred_r, s=1, c='red')
# plt.xlabel('径跳形貌差分值/mm', size=15)
# plt.ylabel('止口变形预测差分值/mm', size=15, rotation=90)
# plt.title('预测结果（90°相位）', size=20, loc = 'center')


# plt.figure(5)
plt.figure(figsize=(10,6))
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams['axes.unicode_minus'] = False
n_f = np.linspace(1, len(X_train_f), len(X_train_f))
plt.scatter(n_f, Y_test_1_f[:, 0], s=1)
plt.scatter(n_f, Y_pred_f[:, 0], s=1)
plt.xlabel('数据点个数', size=15)
plt.ylabel('part1端面变形量/mm', size=15, rotation=90)
plt.legend(['仿真变形量', '预测变形量'], loc="upper right")
plt.title('相位90°', size=20, loc = 'center')
# plt.figure(6)
plt.figure(figsize=(10,6))
plt.scatter(n_f, Y_test_1_f[:, 1], s=1)
plt.scatter(n_f, Y_pred_f[:, 1], s=1)
plt.xlabel('数据点个数', size=15)
plt.ylabel('part2端面变形量/mm', size=15, rotation=90)
plt.legend(['仿真变形量', '预测变形量'], loc="upper right")
plt.title('相位90°', size=20, loc = 'center')

# plt.figure(7)
plt.figure(figsize=(10,6))
n_r = np.linspace(1, len(X_train_r), len(X_train_r))
plt.scatter(n_r, Y_test_1_r[:, 0], s=1)
plt.scatter(n_r, Y_pred_r[:, 0], s=1)
plt.xlabel('数据点个数', size=15)
plt.ylabel('part1止口变形量/mm', size=15, rotation=90)
plt.legend(['仿真变形量', '预测变形量'], loc="upper right")
plt.title('相位90°', size=20, loc = 'center')
# plt.figure(8)
plt.figure(figsize=(10,6))
plt.scatter(n_r, Y_test_1_r[:, 1], s=1)
plt.scatter(n_r, Y_pred_r[:, 1], s=1)
plt.xlabel('数据点个数', size=15)
plt.ylabel('part2止口变形量/mm', size=15, rotation=90)
plt.legend(['仿真变形量', '预测变形量'], loc="upper right")
plt.title('相位90°', size=20, loc = 'center')



"""==============================================================compared=========================================================="""
#偏心误差
#raw results——radial
new_part1_radial_data_raw_up = np.vstack((part1_radial_data_x_up[:, 1] + part1_radial_data_x_up[:, 3], part1_radial_data_y_up[:, 2] + part1_radial_data_y_up[:, 3])).T
new_part2_radial_data_raw_down = np.vstack((part2_radial_data_x_down[:, 1] + part2_radial_data_x_down[:, 3], part2_radial_data_y_down[:, 2] + part2_radial_data_y_down[:, 3])).T
part1_circle_center_raw_up = pre.circ(new_part1_radial_data_raw_up)
part2_circle_center_raw_down = pre.circ(new_part2_radial_data_raw_down)
#precict results——radial
new_part1_radial_data_predict_up = predata_r(part1_radial_data_x_up, Y_pred_r[:, 0])
new_part2_radial_data_predict_down = predata_r(part2_radial_data_x_down, Y_pred_r[:, 1])
part1_circle_center_predict_up = pre.circ(new_part1_radial_data_predict_up)
part2_circle_center_predict_down = pre.circ(new_part2_radial_data_predict_down)

part1_dert_x = part1_circle_center_raw_up[1] - part1_circle_center_predict_up[1]
part1_dert_y = part1_circle_center_raw_up[2] - part1_circle_center_predict_up[2]
part2_dert_x = part2_circle_center_raw_down[1] - part2_circle_center_predict_down[1]
part2_dert_y = part2_circle_center_raw_down[2] - part2_circle_center_predict_down[2]

#偏心相位误差




#偏斜误差
#raw results——flat
new_part1_flat_data_raw_up = np.vstack((part1_flat_data_up[:, 1], part1_flat_data_up[:, 2], part1_flat_data_up[:, 3] + part1_flat_data_up[:, 4])).T
new_part2_flat_data_raw_down = np.vstack((part2_flat_data_down[:, 1], part2_flat_data_down[:, 2], part2_flat_data_down[:, 3] + part2_flat_data_down[:, 4])).T
part1_normal_vector_raw_up = pre.planefit(new_part1_flat_data_raw_up)
part2_normal_vector_raw_down = pre.planefit(new_part2_flat_data_raw_down)
#precict results——flat
new_part1_flat_data_predict_up = np.vstack((part1_flat_data_up[:, 1], part1_flat_data_up[:, 2], part1_flat_data_up[:, 3] + Y_pred_f[:, 0])).T
new_part2_flat_data_predict_down = np.vstack((part2_flat_data_down[:, 1], part2_flat_data_down[:, 2], part2_flat_data_down[:, 3] + Y_pred_f[:, 1])).T
part1_normal_vector_predict_up = pre.planefit(new_part1_flat_data_predict_up)
part2_normal_vector_predict_down = pre.planefit(new_part2_flat_data_predict_down)

part1_dert_rox = (np.arctan(part1_normal_vector_raw_up[1] / part1_normal_vector_raw_up[3]) - np.arctan(part1_normal_vector_predict_up[1] / part1_normal_vector_predict_up[3])) * 180 / np.pi
part1_dert_roy = (np.arctan(part1_normal_vector_raw_up[2] / part1_normal_vector_raw_up[3]) - np.arctan(part1_normal_vector_predict_up[2] / part1_normal_vector_predict_up[3])) * 180 / np.pi
part2_dert_rox = (np.arctan(part2_normal_vector_raw_down[1] / part2_normal_vector_raw_down[3]) - np.arctan(part2_normal_vector_predict_down[1] / part2_normal_vector_predict_down[3])) * 180 / np.pi
part2_dert_roy = (np.arctan(part2_normal_vector_raw_down[2] / part2_normal_vector_raw_down[3]) - np.arctan(part2_normal_vector_predict_down[2] / part2_normal_vector_predict_down[3])) * 180 / np.pi







# features1 = pd.DataFrame(columns=['preload', 'ments', 'ness', 'nesses'])
# target1 = pd.DataFrame









