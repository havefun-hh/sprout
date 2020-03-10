# -*- coding: utf-8 -*-
"""150°"""
import numpy as np
import time
from Replace import Replace as rep
from Prediction import Prediction as pre


"""========================================================================================================================"""
H1 = 805 - 118
H2 = 328 + 65 - 5

"""============================================================address============================================================"""
ad_part1_runout = 'G:/190708-190712data/MNJ-HPC-002ZP1-20190709.csv'
ad_part2_runout = 'G:/190708-190712data/MNJ-HPT-001ZP1-20190708.csv'
ad_inp_data = "G:/19.12.25whole model (less grids)/Step2----inp_all_node_data.csv"
ad_part1_flat_node_down = "G:/19.12.25whole model (less grids)/Step3----part1_flat_node_data_down.csv"
ad_part1_flat_node_up = "G:/19.12.25whole model (less grids)/Step3----part1_flat_node_data_up.csv"
ad_part2_flat_node_down = "G:/19.12.25whole model (less grids)/Step3----part2_flat_node_data_down.csv"
ad_part2_flat_node_up = "G:/19.12.25whole model (less grids)/Step3----part2_flat_node_data_up.csv"
ad_part1_radial_node_down = "G:/19.12.25whole model (less grids)/Step3----part1_radial_node_data_down.csv"
ad_part1_radial_node_up = "G:/19.12.25whole model (less grids)/Step3----part1_radial_node_data_up.csv"
ad_part2_radial_node_down = "G:/19.12.25whole model (less grids)/Step3----part2_radial_node_data_down.csv"
ad_part2_radial_node_up = "G:/19.12.25whole model (less grids)/Step3----part2_radial_node_data_up.csv"
ad_part2_node_number = "G:/19.12.25whole model (less grids)/Step4----part2_node_number.csv"

"""============================================================flat============================================================"""
part1_flat_runout_down = -pre.idata(ad_part1_runout, [3])
part1_flat_runout_spin_down = pre.spin(part1_flat_runout_down, 0)
part1_flat_runout_coordinate_down = pre.gcfl(80 / 2, part1_flat_runout_spin_down, 0)
part1_normal_vector_down = pre.planefit(part1_flat_runout_coordinate_down)
part1_flat_node_data_down = pre.idata(ad_part1_flat_node_down, [0,1,2,3])
new_part1_flat_node_data_down = rep.frure(80 / 2, part1_normal_vector_down[0], part1_normal_vector_down[1], part1_normal_vector_down[2], part1_normal_vector_down[3], part1_flat_runout_spin_down, part1_flat_node_data_down, -H1)

part1_flat_runout_up = pre.idata(ad_part1_runout, [1])
part1_flat_runout_spin_up = pre.spin(part1_flat_runout_up, 0)
part1_flat_runout_coordinate_up = pre.gcfl(206.5 / 2, part1_flat_runout_spin_up, 0)
part1_normal_vector_up = pre.planefit(part1_flat_runout_coordinate_up)
part1_flat_node_data_up = pre.idata(ad_part1_flat_node_up, [0,1,2,3])
new_part1_flat_node_data_up = rep.frure(206.5 / 2, part1_normal_vector_up[0], part1_normal_vector_up[1], part1_normal_vector_up[2], part1_normal_vector_up[3], part1_flat_runout_spin_up, part1_flat_node_data_up, 0)

part2_flat_runout_down = -pre.idata(ad_part2_runout, [4])
part2_flat_runout_spin_down = pre.spin(part2_flat_runout_down, 150)
part2_flat_runout_coordinate_down = pre.gcfl(206.5 / 2, part2_flat_runout_spin_down, 0)
part2_normal_vector_down = pre.planefit(part2_flat_runout_coordinate_down)
part2_flat_node_data_down = pre.idata(ad_part2_flat_node_down, [0,1,2,3])
new_part2_flat_node_data_down = rep.frure(206.5 / 2, part2_normal_vector_down[0], part2_normal_vector_down[1], part2_normal_vector_down[2], part2_normal_vector_down[3], part2_flat_runout_spin_down, part2_flat_node_data_down, 0)

part2_flat_runout_up = pre.idata(ad_part2_runout, [2])
part2_flat_runout_spin_up = pre.spin(part2_flat_runout_up, 150)
part2_flat_runout_coordinate_up = pre.gcfl(80 / 2, part2_flat_runout_spin_up, 0)
part2_normal_vector_up = pre.planefit(part2_flat_runout_coordinate_up)
part2_flat_node_data_up = pre.idata(ad_part2_flat_node_up, [0,1,2,3])
new_part2_flat_node_data_up = rep.frure(80 / 2, part2_normal_vector_up[0], part2_normal_vector_up[1], part2_normal_vector_up[2], part2_normal_vector_up[3], part2_flat_runout_spin_up, part2_flat_node_data_up, H2)

new_flat_node_data = np.vstack((new_part1_flat_node_data_down, new_part1_flat_node_data_up, new_part2_flat_node_data_down, new_part2_flat_node_data_up))

def pene_f(part1_runout, part2_runout):
    penetration = []
    for i in range(len(part1_runout)):
        penetration.append(part1_runout[i] - part2_runout[i])
    return max(penetration)
penetration_f = pene_f(part1_flat_runout_spin_up, part2_flat_runout_spin_down)
penetration_ff = pene_f(new_part1_flat_node_data_up[:, 3], new_part2_flat_node_data_down[:, 3])
"""np.savetxt("G:/19.12.25whole model (less grids)/check_new_flat_data.csv", new_part2_flat_node_data, delimiter=',')"""
"""============================================================shut up============================================================"""
part1_radial_runout_down = pre.idata(ad_part1_runout, [4])
part1_radial_runout_spin_down = pre.spin(part1_radial_runout_down, 0)
part1_radial_runout_coordinate_down = pre.gcra(80 / 2, part1_radial_runout_spin_down, 0)
part1_circle_center_down = pre.circ(part1_radial_runout_coordinate_down)
part1_radial_node_data_down = pre.idata(ad_part1_radial_node_down, [0,1,2,3])
new_part1_radial_node_data_down = rep.rrure2(part1_radial_runout_spin_down, part1_radial_node_data_down)

part1_radial_runout_up = -pre.idata(ad_part1_runout, [2])
part1_radial_runout_spin_up = pre.spin(part1_radial_runout_up, 0)
part1_radial_runout_coordinate_up = pre.gcra(200 / 2, part1_radial_runout_spin_up, 0)
part1_circle_center_up = pre.circ(part1_radial_runout_coordinate_up)
part1_radial_node_data_up = pre.idata(ad_part1_radial_node_up, [0,1,2,3])
new_part1_radial_node_data_up = rep.rrure2(part1_radial_runout_spin_up, part1_radial_node_data_up)

part2_radial_runout_down = pre.idata(ad_part2_runout, [3])
part2_radial_runout_spin_down = pre.spin(part2_radial_runout_down, 150)
part2_radial_runout_coordinate_down = pre.gcra(200 / 2, part2_radial_runout_spin_down, 0)
part2_circle_center_down = pre.circ(part2_radial_runout_coordinate_down[:, 0:3])
part2_radial_node_data_down = pre.idata(ad_part2_radial_node_down, [0,1,2,3])
new_part2_radial_node_data_down = rep.rrure2(part2_radial_runout_spin_down, part2_radial_node_data_down)

part2_radial_runout_up = pre.idata(ad_part2_runout, [1])
part2_radial_runout_spin_up = pre.spin(part2_radial_runout_up, 150)
part2_radial_runout_coordinate_up = pre.gcra(80 / 2, part2_radial_runout_spin_up, 0)
part2_circle_center_up = pre.circ(part2_radial_runout_coordinate_up[:, 0:3])
part2_radial_node_data_up = pre.idata(ad_part2_radial_node_up, [0,1,2,3])
new_part2_radial_node_data_up = rep.rrure2(part2_radial_runout_spin_up, part2_radial_node_data_up)

new_radial_node_data = np.vstack((new_part1_radial_node_data_down, new_part1_radial_node_data_up, new_part2_radial_node_data_down, new_part2_radial_node_data_up))

def pene_r(part1_runout, part2_runout):
    penetration = []
    for i in range(len(part1_runout)):
        penetration.append(part2_runout[i] - part1_runout[i])
    return max(penetration)

penetration_r = pene_r(part1_radial_runout_spin_up, part2_radial_runout_spin_down)

def interf(part1_runout, part2_runout):
    interference = []
    for i in range(len(part1_runout)):
        interference.append(part1_runout[i] - part2_runout[i])
    return max(interference)

interference = interf(part1_radial_runout_spin_up, part2_radial_runout_spin_down)  #max gap
"""np.savetxt("G:/19.12.25whole model (less grids)/check_new_radial_data.csv", new_part2_radial_node_data, delimiter=',')"""
"""============================================================part2 translate============================================================"""
part2_node_number = pre.idata(ad_part2_node_number, [0])

#translation distance
X = part2_circle_center_down[1] - part1_circle_center_up[1]
Y = part2_circle_center_down[2] - part1_circle_center_up[2]
Z = np.abs(max(new_part1_flat_node_data_up[:, 3]) - min(new_part2_flat_node_data_down[:, 3]))
"""============================================================inp replace============================================================"""
start = time.perf_counter()
inp_data = pre.idata(ad_inp_data, [0,1,2,3])
end = time.perf_counter()
print(f"inp input time consuming:{end - start}s")

inp_data_1 = rep.ifrure(inp_data, new_flat_node_data)
inp_data_2 = rep.irrure(inp_data_1, new_radial_node_data)
# inp_data_3 = rep.ip2tr(inp_data_2, part2_node_number, -X, -Y, Z)
# inp_data_33 = rep.ip2tr(inp_data_2, part2_node_number, 0, 0, Z)
inp_data_4 = rep.ip2tr(inp_data_2, part2_node_number, -X, -Y, 0)



# n1 = 0
# for i in range(len(inp_data_1[:, 0])):
#     if inp_data_2[i, 1] != inp_data_1[i, 1]:
#         n1 += 1
# print(n1)

# a = pre.circ(new_part1_radial_node_data_down[:, 1:3])
# b = pre.circ(new_part1_radial_node_data_up[:, 1:3])
# c = pre.circ(new_part2_radial_node_data_down[:, 1:3])
# d = pre.circ(new_part2_radial_node_data_up[:, 1:3])
# L1 = pre.planefit(new_part1_flat_node_data_down[:, 1:])
# L2 = pre.planefit(new_part1_flat_node_data_up[:, 1:])
# L3 = pre.planefit(new_part2_flat_node_data_down[:, 1:])
# L4 = pre.planefit(new_part2_flat_node_data_up[:, 1:])

# o1 = np.arctan(part2_normal_vector_down[0] / part2_normal_vector_down[2]) * 180 / np.pi
# o2 = np.arctan(L3[0] / L3[2]) * 180 / np.pi

# o3 = np.arctan(part2_normal_vector_up[0] / part2_normal_vector_up[2]) * 180 / np.pi
# o4 = np.arctan(L4[0] / L4[2]) * 180 / np.pi


"""
np.savetxt("G:/19.12.25whole model (less grids)/Step5----replaced(150)/Step5----replaced1.csv", inp_data_1, delimiter=',')
np.savetxt("G:/19.12.25whole model (less grids)/Step5----replaced(150)/Step5----replaced2.csv", inp_data_2, delimiter=',')
np.savetxt("G:/19.12.25whole model (less grids)/Step5----replaced(150)/Step5----replaced3.csv", inp_data_3, delimiter=',')
np.savetxt("G:/19.12.25whole model (less grids)/Step5----replaced(150)/Step5----replaced3_1.csv", inp_data_33, delimiter=',')
np.savetxt("G:/19.12.25whole model (less grids)/Step5----replaced(150)/Step5----replaced4.csv", inp_data_4, delimiter=',')
"""

"""============================================================visualization============================================================"""
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#shut up
ax = plt.figure().add_subplot(111, projection = '3d')
ax.scatter(part1_radial_node_data[:, 1], part1_radial_node_data[:, 2], part1_radial_node_data[:, 3], c = 'r')
#flat
ax = plt.figure().add_subplot(111, projection = '3d')
ax.scatter(part1_flat_node_data_up[:, 1], part1_flat_node_data_up[:, 2], part1_flat_node_data_up[:, 3], c = 'r', s = 0.5)

#shut up
ax = plt.figure().add_subplot(111, projection = '3d')
ax.scatter(new_radial_node_data[:, 1], new_radial_node_data[:, 2], new_radial_node_data[:, 3], c = 'r', s = 0.5)
#flat
ax = plt.figure().add_subplot(111, projection = '3d')
ax.scatter(new_part1_flat_node_data_up[:, 1], new_part1_flat_node_data_up[:, 2], new_part1_flat_node_data_up[:, 3], c = 'r', s = 0.5)

#shut up
ax = plt.figure().add_subplot(111, projection = '3d')
ax.scatter(new_radial_node_data[:, 1], new_radial_node_data[:, 2], new_radial_node_data[:, 3], c = 'r', s = 0.5)
#flat
ax = plt.figure().add_subplot(111, projection = '3d')
ax.scatter(new_flat_node_data[:, 1], new_flat_node_data[:, 2], new_flat_node_data[:, 3], c = 'r', s = 0.5)

#check spin runout
n = np.linspace(1, 3600, 3600)
plt.figure(1)
plt.scatter(n, part1_flat_runout_up, s = 1)
plt.scatter(n, part2_flat_runout_down, s = 1)
plt.figure(2)
plt.scatter(n, part1_flat_runout_spin_up, s = 1)
plt.scatter(n, part2_flat_runout_spin_down, s = 1)
"""""

