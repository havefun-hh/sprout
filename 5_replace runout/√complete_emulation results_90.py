"""所有形貌0°"""

import pandas as pd
import numpy as np
from numpy import linalg as la
import time
from Prediction import Prediction as pre


start2 = time.perf_counter()
#两零件高度
H1 = 805 - 118
H2 = 328 + 65 - 5
"""==================================================================测量位置===================================================================="""
"""==================================================================(1)止口====================================================================="""
part1_radial_data_x_down = np.array(pd.read_csv("G:/19.12.25whole model (less grids)/Step5----replaced(90)/Step8——仿真结果/1.13_server_inp4圆心对准，有跳动，过盈0，大变形，加重力， 弱弹簧3300N(frictional)/基准止口x.txt", sep='\t', usecols=[0,1,2,4]))
part1_radial_data_y_down = np.array(pd.read_csv("G:/19.12.25whole model (less grids)/Step5----replaced(90)/Step8——仿真结果/1.13_server_inp4圆心对准，有跳动，过盈0，大变形，加重力， 弱弹簧3300N(frictional)/基准止口y.txt", sep='\t', usecols=[0,1,2,4]))
part2_radial_data_x_up = np.array(pd.read_csv("G:/19.12.25whole model (less grids)/Step5----replaced(90)/Step8——仿真结果/1.13_server_inp4圆心对准，有跳动，过盈0，大变形，加重力， 弱弹簧3300N(frictional)/位置止口x.txt", sep='\t', usecols=[0,1,2,4]))
part2_radial_data_y_up = np.array(pd.read_csv("G:/19.12.25whole model (less grids)/Step5----replaced(90)/Step8——仿真结果/1.13_server_inp4圆心对准，有跳动，过盈0，大变形，加重力， 弱弹簧3300N(frictional)/位置止口y.txt", sep='\t', usecols=[0,1,2,4]))

new_part1_radial_data_down = np.vstack((part1_radial_data_x_down[:, 1] + part1_radial_data_x_down[:, 3], part1_radial_data_y_down[:, 2] + part1_radial_data_y_down[:, 3])).T
new_part2_radial_data_up = np.vstack((part2_radial_data_x_up[:, 1] + part2_radial_data_x_up[:, 3], part2_radial_data_y_up[:, 2] + part2_radial_data_y_up[:, 3])).T

part1_circle_center_down = pre.circ(new_part1_radial_data_down)
part2_circle_center_up = pre.circ(new_part2_radial_data_up)

"""==================================================================(2)端面===================================================================="""
part1_flat_data_down = np.array(pd.read_csv("G:/19.12.25whole model (less grids)/Step5----replaced(90)/Step8——仿真结果/1.13_server_inp4圆心对准，有跳动，过盈0，大变形，加重力， 弱弹簧3300N(frictional)/基准端面.txt", sep='\t'))
part2_flat_data_up = np.array(pd.read_csv("G:/19.12.25whole model (less grids)/Step5----replaced(90)/Step8——仿真结果/1.13_server_inp4圆心对准，有跳动，过盈0，大变形，加重力， 弱弹簧3300N(frictional)/位置端面.txt", sep='\t'))

new_part1_flat_data_down = np.vstack((part1_flat_data_down[:, 1], part1_flat_data_down[:, 2], part1_flat_data_down[:, 3] + part1_flat_data_down[:, 4] + H1)).T
new_part2_flat_data_up = np.vstack((part2_flat_data_up[:, 1], part2_flat_data_up[:, 2], part2_flat_data_up[:, 3] + part2_flat_data_up[:, 4] - H2)).T

part1_normal_vector_down = pre.planefit(new_part1_flat_data_down)
part2_normal_vector_up = pre.planefit(new_part2_flat_data_up)

"""==================================================================拟合矩阵===================================================================="""

results = pre.eccentric(part1_circle_center_down[1], part1_circle_center_down[2], part2_circle_center_up[1], part2_circle_center_up[2], part1_normal_vector_down[0], part1_normal_vector_down[1], part1_normal_vector_down[2], part2_normal_vector_up[0], part2_normal_vector_up[1], part2_normal_vector_up[2], H1 + H2)
results_1 = pre.eccentric(0, 0, part2_circle_center_up[1], part2_circle_center_up[2], part1_normal_vector_down[0], part1_normal_vector_down[1], part1_normal_vector_down[2], part2_normal_vector_up[0], part2_normal_vector_up[1], part2_normal_vector_up[2], H1 + H2)
m = np.array([[1, 0, results[2], results[0]], [0, 1, results[3], results[1]], [-results[2] ,-results[3], 1, H1 + H2], [0, 0, 0, 1]])

end2 = time.perf_counter()
print(f'耗时：{end2 - start2}s')

#偏心量
e = np.sqrt(results[0] ** 2 + results[1] ** 2)
e1 = np.sqrt((part2_circle_center_up[1] - part1_circle_center_down[1]) ** 2 + (part2_circle_center_up[2] - part1_circle_center_down[2]) ** 2)
e2 = np.sqrt(results_1[0] ** 2 + results_1[1] ** 2)
#偏心相位
phase = np.arctan(results[1] / results[0]) * 180 / np.pi
phase1 = np.arctan((part2_circle_center_up[2] - part1_circle_center_down[2]) / (part2_circle_center_up[1] - part1_circle_center_down[2])) * 180 / np.pi
phase2 = np.arctan(results_1[1] / results_1[0]) * 180 / np.pi


"""==================================================================ecc拟合=================================================================="""
"""
***frictional(12.30，减少细化网格，有跳动，圆心不对准，加过盈，大变形): e = 0.08717687911730311; phase = 21.709361137244432
***frictional(12.30，减少细化网格，有跳动，圆心不对准，加过盈，大变形，平移H1): e = 0.08722018874833357; phase = 21.71810552540024
***frictional(12.30，减少细化网格，有跳动，圆心不对准，加过盈，大变形，平移H1，8000N): e = 0.08474589433566354; phase = 20.720994961231167
***frictional(12.31，减少细化网格，有跳动，圆心不对准，过盈0.1264，大变形，平移H1，8000N): e = 0.08013356570007324; phase = 18.538304433808186
***90°frictional(1.6，减少细化网格，有跳动，圆心不对准，过盈0.0562，大变形，弱弹簧，3300N): e2 = 0.0937653521463908; phase2 = 12.729773142758898
***90°frictional(1.6，减少细化网格，有跳动，圆心对准，过盈0，大变形，弱弹簧，3300N): e = 0.12265826041948759; phase = 26.765815817254794
***90°frictional(1.6，减少细化网格，有跳动，圆心对准，过盈0，大变形，弱弹簧，3300N): e2 = 0.13763158726867383; phase2 = 26.80637568039528
***90°frictional(test_1.6，曾广，减少细化网格，有跳动，圆心对准，过盈0，大变形，弱弹簧，3300N): e2 = 0.12265826041948759; phase2 =26.765815817254794

***0°frictional(1.8，减少细化网格，有跳动，圆心对准，过盈0，大变形，加重力，弱弹簧，3300N): e = 0.13166508814627012; phase = 32.28132909493118
***90°frictional(1.8，减少细化网格，有跳动，圆心对准，过盈0，大变形，加重力，弱弹簧，3300N): e = 0.12282721304853834; phase = 26.817259167834326
***90°frictional(1.13server，同上): e = 0.12278062056854265; phase = 26.76638459624804
***90°frictional(1.13local，同上): e = 0.12274453974556881; phase = 26.777124993347158

"""




"""==================================================================常规拟合(舍)=================================================================="""

"""
测试值:e = 0.13014; phase = 42.0
frictional(细化网格，仅part2有跳动，圆心不对准，不加过盈，大变形): e1 = 0.11472774530255918; phase1 = 52.75283331830626
frictional(减少细化网格，仅part2有跳动，圆心不对准，不加过盈，大变形): e1 = 0.11455908377495096; phase1 = 52.740239999456804
"""





# import matplotlib.pyplot as plt
# plt.figure(1)
# plt.scatter(new_part1_radial_data_down[:, 0], new_part1_radial_data_down[:, 1], s = 0.5)
# plt.figure(2)
# plt.scatter(new_part2_radial_data_up[:, 0], new_part2_radial_data_up[:, 1], s = 0.5)

# """=============================================================transform to runout==============================================================="""
# part1_radial_data_x_down = np.array(pd.read_csv("G:/19.12.9whole model (inp replace runout)/Step8——仿真结果/基准止口x.txt", sep='\t', usecols=[4]))
# part1_radial_data_y_down = np.array(pd.read_csv("G:/19.12.9whole model (inp replace runout)/Step8——仿真结果/基准止口y.txt", sep='\t', usecols=[4]))
# part2_radial_data_x_up = np.array(pd.read_csv("G:/19.12.9whole model (inp replace runout)/Step8——仿真结果/位置止口x.txt", sep='\t', usecols=[4]))
# part2_radial_data_y_up = np.array(pd.read_csv("G:/19.12.9whole model (inp replace runout)/Step8——仿真结果/位置止口y.txt", sep='\t', usecols=[4]))


# base_deformation = []
# for i in range(len(part1_radial_data_x_down)):
#     base_deformation.append(np.sqrt(part1_radial_data_x_down[i] ** 2 + part1_radial_data_y_down[i] ** 2))
# base_deformation = np.array(base_deformation)
# base_deformation = np.squeeze(base_deformation)

# position_deformation = []
# for i in range(len(part2_radial_data_x_up)):
#     position_deformation.append(np.sqrt(part2_radial_data_x_up[i] ** 2 + part2_radial_data_y_up[i] ** 2))
# position_deformation = np.array(position_deformation)
# position_deformation = np.squeeze(position_deformation)
# """
# np.savetxt("G:/19.12.9whole model (inp replace runout)/base_deformation.csv", base_deformation, delimiter=',')
# np.savetxt("G:/19.12.9whole model (inp replace runout)/position_deformation.csv", position_deformation, delimiter=',')
# """








