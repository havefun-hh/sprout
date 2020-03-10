import numpy as np
import time
from Homogeneous_Transformation import Homogeneous_Transformation as ht


class Replace(object):
    """
    替换端面、止口形貌
    """
#    def __init__():
#    
    def frure(r, a, b, c, d, flat_runout, flat_node_data, H):    #flat runout replace;r——端跳测量位置半径（沿法向量方向生成端面形貌）
        theta1 = np.linspace(0.1, 360, 3600)
        theta2 = []
        for i in range(len(flat_node_data[:, 0])):
            if flat_node_data[i, 1] >= 0 and flat_node_data[i, 2] >= 0:
                theta = np.arctan(flat_node_data[i, 2] / flat_node_data[i, 1]) * 180 / np.pi
                theta2.append(theta)
            if flat_node_data[i, 1] < 0 and flat_node_data[i, 2] > 0:
                theta = np.arctan(flat_node_data[i, 2] / flat_node_data[i, 1]) * 180 / np.pi + 180
                theta2.append(theta)
            if flat_node_data[i, 1] < 0 and flat_node_data[i, 2] < 0:
                theta = np.arctan(flat_node_data[i, 2] / flat_node_data[i, 1]) * 180 / np.pi + 180
                theta2.append(theta)
            if flat_node_data[i, 1] > 0 and flat_node_data[i, 2] < 0:
                theta = np.arctan(flat_node_data[i, 2] / flat_node_data[i, 1]) * 180 / np.pi + 360
                theta2.append(theta)
        theta2 = np.array(theta2).reshape(-1, 1)
        theta2 = np.squeeze(theta2)
        #提取微观端跳
        theta = np.linspace((2 * np.pi) / len(flat_runout), 2 * np.pi, len(flat_runout))
        xx = r * np.cos(theta)
        yy = r * np.sin(theta)
        new_flat_runout = flat_runout + (a * xx + b * yy + d) / c
        #用距离最近的点的形貌代替
        replace_runout = []
        start = time.perf_counter()
        for i in range(len(theta2)):
            theta_discrepancy = abs(theta2[i] - theta1)
            S = np.where(min(theta_discrepancy) == theta_discrepancy)[0][0]
            z = (-a * flat_node_data[i, 1] - b * flat_node_data[i, 2] - d) / c
            replace_runout.append(z + new_flat_runout[S] + H)
        end = time.perf_counter()
        print("替换形貌耗时：{}s".format(end - start))
        replace_runout = np.array(replace_runout).reshape(-1, 1)
        replace_runout = np.squeeze(replace_runout)
        
        new_data = np.array([flat_node_data[:, 0], flat_node_data[:, 1], flat_node_data[:, 2], replace_runout]).T
        return new_data

    def frure2(r, a, b, c, d, flat_runout, flat_node_data, H):        #只生成斜面，无微观跳动
        theta1 = np.linspace(0.1, 360, 3600)
        theta2 = []
        for i in range(len(flat_node_data[:, 0])):
            if flat_node_data[i, 1] >= 0 and flat_node_data[i, 2] >= 0:
                theta = np.arctan(flat_node_data[i, 2] / flat_node_data[i, 1]) * 180 / np.pi
                theta2.append(theta)
            if flat_node_data[i, 1] < 0 and flat_node_data[i, 2] > 0:
                theta = np.arctan(flat_node_data[i, 2] / flat_node_data[i, 1]) * 180 / np.pi + 180
                theta2.append(theta)
            if flat_node_data[i, 1] < 0 and flat_node_data[i, 2] < 0:
                theta = np.arctan(flat_node_data[i, 2] / flat_node_data[i, 1]) * 180 / np.pi + 180
                theta2.append(theta)
            if flat_node_data[i, 1] > 0 and flat_node_data[i, 2] < 0:
                theta = np.arctan(flat_node_data[i, 2] / flat_node_data[i, 1]) * 180 / np.pi + 360
                theta2.append(theta)
        theta2 = np.array(theta2).reshape(-1, 1)
        theta2 = np.squeeze(theta2)
        #提取微观端跳
        theta = np.linspace((2 * np.pi) / len(flat_runout), 2 * np.pi, len(flat_runout))
        xx = r * np.cos(theta)
        yy = r * np.sin(theta)
        new_flat_runout = flat_runout - (a * xx + b * yy + d) / c
        #用距离最近的点的形貌代替
        replace_runout = []
        start = time.perf_counter()
        for i in range(len(theta2)):
            theta_discrepancy = abs(theta2[i] - theta1)
            S = np.where(min(theta_discrepancy) == theta_discrepancy)[0][0]
            z = (-a * flat_node_data[i, 1] - b * flat_node_data[i, 2] - d) / c
            replace_runout.append(z + H)        #此处不加微观跳动
        end = time.perf_counter()
        print("替换形貌耗时：{}s".format(end - start))
        replace_runout = np.array(replace_runout).reshape(-1, 1)
        replace_runout = np.squeeze(replace_runout)
        
        new_data = np.array([flat_node_data[:, 0], flat_node_data[:, 1], flat_node_data[:, 2], replace_runout]).T
        return new_data
    
    def frure3(r, a, b, c, d, flat_runout, flat_node_data, H):        #只生成微观跳动，无斜面
        theta1 = np.linspace(0.1, 360, 3600)
        theta2 = []
        for i in range(len(flat_node_data[:, 0])):
            if flat_node_data[i, 1] >= 0 and flat_node_data[i, 2] >= 0:
                theta = np.arctan(flat_node_data[i, 2] / flat_node_data[i, 1]) * 180 / np.pi
                theta2.append(theta)
            if flat_node_data[i, 1] < 0 and flat_node_data[i, 2] > 0:
                theta = np.arctan(flat_node_data[i, 2] / flat_node_data[i, 1]) * 180 / np.pi + 180
                theta2.append(theta)
            if flat_node_data[i, 1] < 0 and flat_node_data[i, 2] < 0:
                theta = np.arctan(flat_node_data[i, 2] / flat_node_data[i, 1]) * 180 / np.pi + 180
                theta2.append(theta)
            if flat_node_data[i, 1] > 0 and flat_node_data[i, 2] < 0:
                theta = np.arctan(flat_node_data[i, 2] / flat_node_data[i, 1]) * 180 / np.pi + 360
                theta2.append(theta)
        theta2 = np.array(theta2).reshape(-1, 1)
        theta2 = np.squeeze(theta2)
        #提取微观端跳
        theta = np.linspace((2 * np.pi) / len(flat_runout), 2 * np.pi, len(flat_runout))
        xx = r * np.cos(theta)
        yy = r * np.sin(theta)
        new_flat_runout = flat_runout - (a * xx + b * yy + d) / c
        #用距离最近的点的形貌代替
        replace_runout = []
        start = time.perf_counter()
        for i in range(len(theta2)):
            theta_discrepancy = abs(theta2[i] - theta1)
            S = np.where(min(theta_discrepancy) == theta_discrepancy)[0][0]
            z = new_flat_runout[S]
            replace_runout.append(z + H)        #此处不加微观跳动
        end = time.perf_counter()
        print("替换形貌耗时：{}s".format(end - start))
        replace_runout = np.array(replace_runout).reshape(-1, 1)
        replace_runout = np.squeeze(replace_runout)
        
        new_data = np.array([flat_node_data[:, 0], flat_node_data[:, 1], flat_node_data[:, 2], replace_runout]).T
        return new_data
    
    def rrure2(radial_runout, radial_node_data):    #radial runout replace
        theta1 = np.linspace(0.1, 360, 3600)
        theta2 = []
        for i in range(len(radial_node_data[:, 0])):
            if radial_node_data[i, 1] >= 0 and radial_node_data[i, 2] >= 0:
                theta = np.arctan(radial_node_data[i, 2] / radial_node_data[i, 1]) * 180 / np.pi
                theta2.append(theta)
            if radial_node_data[i, 1] < 0 and radial_node_data[i, 2] > 0:
                theta = np.arctan(radial_node_data[i, 2] / radial_node_data[i, 1]) * 180 / np.pi + 180
                theta2.append(theta)
            if radial_node_data[i, 1] < 0 and radial_node_data[i, 2] < 0:
                theta = np.arctan(radial_node_data[i, 2] / radial_node_data[i, 1]) * 180 / np.pi + 180
                theta2.append(theta)
            if radial_node_data[i, 1] > 0 and radial_node_data[i, 2] < 0:
                theta = np.arctan(radial_node_data[i, 2] / radial_node_data[i, 1]) * 180 / np.pi + 360
                theta2.append(theta)
        theta2 = np.array(theta2).reshape(-1, 1)
        theta2 = np.squeeze(theta2)
        replace_runout = []
        new_x = []
        new_y = []
        start = time.perf_counter()
        for i in range(len(theta2)):
            theta_discrepancy = abs(theta2[i] - theta1)
            S = np.where(min(theta_discrepancy) == theta_discrepancy)[0][0]
            replace_runout.append(radial_runout[S])
        replace_runout = np.array(replace_runout).reshape(-1, 1)
        replace_runout = np.squeeze(replace_runout)
        for j in range(len(radial_node_data[:, 0])):
            new_x.append(radial_node_data[j, 1] + replace_runout[j] * np.cos(theta2[j] * np.pi / 180))
            new_y.append(radial_node_data[j, 2] + replace_runout[j] * np.sin(theta2[j] * np.pi / 180))
        end = time.perf_counter()
        print("替换形貌耗时：{}s".format(end - start))
        new_x = np.array(new_x).reshape(-1, 1)
        new_x = np.squeeze(new_x)
        new_y = np.array(new_y).reshape(-1, 1)
        new_y = np.squeeze(new_y)
        new_data = np.array([radial_node_data[:, 0], new_x, new_y, radial_node_data[:, 3]]).T
        return new_data

    def rrure3(radial_runout, radial_node_data):    #同rure2,return runout
        theta1 = np.linspace(0.1, 360, 3600)
        theta2 = []
        for i in range(len(radial_node_data[:, 0])):
            if radial_node_data[i, 1] >= 0 and radial_node_data[i, 2] >= 0:
                theta = np.arctan(radial_node_data[i, 2] / radial_node_data[i, 1]) * 180 / np.pi
                theta2.append(theta)
            if radial_node_data[i, 1] < 0 and radial_node_data[i, 2] > 0:
                theta = np.arctan(radial_node_data[i, 2] / radial_node_data[i, 1]) * 180 / np.pi + 180
                theta2.append(theta)
            if radial_node_data[i, 1] < 0 and radial_node_data[i, 2] < 0:
                theta = np.arctan(radial_node_data[i, 2] / radial_node_data[i, 1]) * 180 / np.pi + 180
                theta2.append(theta)
            if radial_node_data[i, 1] > 0 and radial_node_data[i, 2] < 0:
                theta = np.arctan(radial_node_data[i, 2] / radial_node_data[i, 1]) * 180 / np.pi + 360
                theta2.append(theta)
        theta2 = np.array(theta2).reshape(-1, 1)
        theta2 = np.squeeze(theta2)
        replace_runout = []
        new_x = []
        new_y = []
        start = time.perf_counter()
        for i in range(len(theta2)):
            theta_discrepancy = abs(theta2[i] - theta1)
            S = np.where(min(theta_discrepancy) == theta_discrepancy)[0][0]
            replace_runout.append(radial_runout[S])
        replace_runout = np.array(replace_runout).reshape(-1, 1)
        replace_runout = np.squeeze(replace_runout)
        return replace_runout
        
    def ifrure(inp_data, new_flat_node_data):    #inp flat runout replace
        start = time.perf_counter()
        inp_data_1 = inp_data.copy()
        S1 = []
        for i in range(len(new_flat_node_data[:, 0])):
            s1 = np.where(new_flat_node_data[i, 0] == inp_data_1[:, 0])[0][0]
            S1.append(s1)
            inp_data_1[s1, 3] = new_flat_node_data[i, 3]
        end = time.perf_counter()
        print(f"替换端面节点耗时：{end - start}s")
        return inp_data_1
    
    def irrure(inp_data_1, new_radial_node_data):   #inp radial runout replace
        start = time.perf_counter()
        inp_data_2 = inp_data_1.copy()
        S2 = []
        for i in range(len(new_radial_node_data[:, 0])):
            s2 = np.where(new_radial_node_data[i, 0] == inp_data_2[:, 0])[0][0]
            S2.append(s2)
            inp_data_2[s2, 1] = new_radial_node_data[i, 1]
            inp_data_2[s2, 2] = new_radial_node_data[i, 2]
        end = time.perf_counter()
        print(f"替换止口节点耗时：{end - start}s")
        return inp_data_2
    
    def ip2tr(inp_data_2, part2_node_number, X, Y, Z):   #inp part2 translate
        start = time.perf_counter()
        inp_data_3 = inp_data_2.copy()
        S3 = []
        for i in range(len(part2_node_number)):
            s3 = np.where(part2_node_number[i] == inp_data_3[:, 0])[0][0]
            S3.append(s3)
            temp = ht.translate(inp_data_3[s3, 1:], X, Y, Z)
            inp_data_3[s3, 1] = temp[0]
            inp_data_3[s3, 2] = temp[1]
            inp_data_3[s3, 3] = temp[2]
        end = time.perf_counter()
        print(f"translate part2 time consuming:{end - start}s")
        return inp_data_3
        
    def correction(r, runout, a, b, d):                      #tilt correction
        theta = np.linspace(0, 3599, 3600)
        x_data = r * np.cos(2*np.pi*theta/3600)
        y_data = r * np.sin(2*np.pi*theta/3600)
        new_runout = runout - (a * x_data + b * y_data + d)
        return new_runout









