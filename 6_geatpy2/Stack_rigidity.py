"""根据装配后测试数据，反求偏心偏斜量"""
import numpy as np
from Prediction import Prediction as pre
# from numba import jit
# from multiprocessing.dummy import Pool
from scipy.optimize import root, fsolve
import numpy as np


class Para():
    def __init__(self, runout, r):
        self.runout = runout
        self.r = r
        
    def vec(self, args):
        runout = args[0]
        r = args[1]
        theta = args[2]
        res = pre.pfit(pre.gcfl(r, pre.spin(runout, theta), 0))
        return res
    
    def cen(self, args):
        runout = args[0]
        r = args[1]
        theta = args[2]
        res = pre.circ(pre.gcra(r, pre.spin(runout, theta), 0))
        return res
    
    def getPara(self):
        runout = self.runout
        r = self.r
        para = [[]] * len(runout)
        for i in range(int(len(runout) / 4)):
            args_1 = list(zip([runout[i * 4]] * 36, [r[i * 4]] * 36, [i * 10 for i in range(36)]))
            args_2 = list(zip([runout[i * 4 + 1]] * 36, [r[i * 4 + 1]] * 36, [i * 10 for i in range(36)]))
            args_3 = list(zip([runout[i * 4 + 2]] * 36, [r[i * 4 + 2]] * 36, [i * 10 for i in range(36)]))
            args_4 = list(zip([runout[i * 4 + 3]] * 36, [r[i * 4 + 3]] * 36, [i * 10 for i in range(36)]))
            para[i * 4] = [i for i in map(self.vec, args_1)]
            para[i * 4 + 1] = [i for i in map(self.vec, args_2)]
            para[i * 4 + 2] = [i for i in map(self.cen, args_3)]
            para[i * 4 + 3] = [i for i in map(self.cen, args_4)]
        return para
    

class Stack_rigidity():
    def __init__(self, runout, r, H, para):
        self.runout = runout
        self.r = r
        self.H = H
        self.para = para
        
    def gcra(self, r, runout, h, theta):                #(generate coordinates--radial)生成止口的直角坐标；theta顺时针为正
        H = len(runout)
        Hr = np.round(theta / 360 * H)
        Hr = int(Hr)
        a = list(runout[Hr:H])
        b = list(runout[:Hr])
        a.extend(b)
        new_runout = np.array(a)
        t = np.linspace(np.pi / 1800, 2 * np.pi, 3600)
        # x, y = [], []
        # for i in range(len(t)):
        #     x.append((r + new_runout[i]) * np.cos(t[i]))
        #     y.append((r + new_runout[i]) * np.sin(t[i]))
        # x = np.array(x)
        # y = np.array(y)
        x = (r + new_runout) * np.cos(t)
        y = (r + new_runout) * np.sin(t)
        z = np.array([h] * 3600)
        data = np.dstack((x, y, z))
        data = np.squeeze(data)
        return data
    
    def gcfl(self, r, runout, h, theta):                #(generate coordinates--flat)生成端面的直角坐标
        H = len(runout)
        Hr = np.round(theta / 360 * H)
        Hr = int(Hr)
        a = list(runout[Hr:H])
        b = list(runout[:Hr])
        a.extend(b)
        new_runout = np.array(a)
        t = np.linspace(0, 3599, 3600)
        x = r * np.cos(2 * np.pi * t / 3600)
        y = r * np.sin(2 * np.pi * t / 3600)
        z = h + new_runout
        data = np.dstack((x, y, z))
        data = np.squeeze(data)
        return data
    
    def get_phase(self, x, y):
        if x > 0:
            phase = np.arctan(y / x) * 180 / np.pi
        else:
            phase = np.arctan(y / x) * 180 / np.pi + 180
        return phase
    
    def bias_2(self, part1_theta, part2_theta):
        runout = self.runout
        r = self.r
        H = self.H
        #生成坐标
        part1_flat_coordinate_down = self.gcfl(r[0], runout[0], 0, part1_theta)
        part1_flat_coordinate_up = self.gcfl(r[1], runout[1], 0, part1_theta)
        part1_radial_coordinate_down = self.gcra(r[2], runout[2], 0, part1_theta)
        part1_radial_coordinate_up = self.gcra(r[3], runout[3], 0, part1_theta)
        #part1两端圆心及法向量
        part1_center_down = pre.circ(part1_radial_coordinate_down)
        part1_center_up = pre.circ(part1_radial_coordinate_up)
        part1_vector_down = pre.pfit(part1_flat_coordinate_down)
        part1_vector_up = pre.pfit(part1_flat_coordinate_up)
        #生成坐标
        part2_flat_coordinate_down = self.gcfl(r[4], runout[4], 0, part2_theta)
        part2_flat_coordinate_up = self.gcfl(r[5], runout[5], 0, part2_theta)
        part2_radial_coordinate_down = self.gcra(r[6], runout[6], 0, part2_theta)
        part2_radial_coordinate_up = self.gcra(r[7], runout[7], 0, part2_theta)
        #part2两端圆心及法向量
        part2_center_down = pre.circ(part2_radial_coordinate_down)
        part2_center_up = pre.circ(part2_radial_coordinate_up)
        part2_vector_down = pre.pfit(part2_flat_coordinate_down)
        part2_vector_up = pre.pfit(part2_flat_coordinate_up)
        #求出装配后偏心偏斜量
        part1_results = pre.eccentric(part1_center_down[1], part1_center_down[2], part1_center_up[1], part1_center_up[2], part1_vector_down[0], part1_vector_down[1], part1_vector_down[2], part1_vector_up[0], part1_vector_up[1], part1_vector_up[2], H[0])
        part2_results = pre.eccentric(part2_center_down[1], part2_center_down[2], part2_center_up[1], part2_center_up[2], part2_vector_down[0], part2_vector_down[1], part2_vector_down[2], part2_vector_up[0], part2_vector_up[1], part2_vector_up[2], H[1])
        part1_x_center = part1_results[0]
        part1_y_center = part1_results[1]
        part1_theta_y = part1_results[2]
        part1_theta_x = part1_results[3]
        part2_x_center = part2_results[0]
        part2_y_center = part2_results[1]
        part2_theta_y = part2_results[2]
        part2_theta_x = part2_results[3]
        p1 = np.array([[1, 0, part1_theta_y, part1_x_center], [0, 1, part1_theta_x, part1_y_center], [-part1_theta_y, -part1_theta_x, 1, H[0]], [0, 0, 0, 1]])
        p2 = np.array([[1, 0, part2_theta_y, part2_x_center], [0, 1, part2_theta_x, part2_y_center], [-part2_theta_y, -part2_theta_x, 1, H[1]], [0, 0, 0, 1]])
        m = np.matmul(p1, p2)
        #偏心量
        e = np.sqrt(m[0, 3] ** 2 + m[1, 3] ** 2)
        #偏心相位
        phase = self.get_phase(m[0, 3], m[1, 3])
        return [e, phase]
    
    def bias_n(self, *theta):  #可接收任意个theta；返回【所有级】的结果
        runout = self.runout
        r = self.r
        H = self.H
        theta = list(theta)  #将收到的theta写入一个list
        p = [0] * (len(theta))
        for i in range(len(theta)):
            vector_down = pre.pfit(self.gcfl(r[i*4], runout[i*4], 0, theta[i]))
            vector_up = pre.pfit(self.gcfl(r[i*4+1], runout[i*4+1], 0, theta[i]))
            center_down = pre.circ(self.gcra(r[i*4+2], runout[i*4+2], 0, theta[i]))
            center_up = pre.circ(self.gcra(r[i*4+3], runout[i*4+3], 0, theta[i]))
            results = pre.eccentric(center_down[1], center_down[2], center_up[1], center_up[2], vector_down[0], vector_down[1], vector_down[2], vector_up[0], vector_up[1], vector_up[2], H[i])
            p[i] = np.array([[1, 0, results[2], results[0]], [0, 1, results[3], results[1]], [-results[2], -results[3], 1, H[i]], [0, 0, 0, 1]])
        e, phase = [0] * (len(p)), [0] * (len(p))
        m = 1
        for i in range(len(p)):
            m = np.dot(m, p[i])
            #偏心量
            e[i] = np.sqrt(m[0, 3] ** 2 + m[1, 3] ** 2)
            #偏心相位
            phase[i] = self.get_phase(m[0, 3], m[1, 3])
        return np.stack((e, phase), axis=1)
    
    def bias_n_li(self, theta):  #接收一个list类型的theta参数；返回【所有级】的结果
        runout = self.runout
        r = self.r
        H = self.H
        p = [0] * (len(theta))
        for i in range(len(theta)):
            vector_down = pre.pfit(self.gcfl(r[i * 4], runout[i * 4], 0, theta[i]))
            vector_up = pre.pfit(self.gcfl(r[i * 4 + 1], runout[i * 4 + 1], 0, theta[i]))
            center_down = pre.circ(self.gcra(r[i * 4 + 2], runout[i * 4 + 2], 0, theta[i]))
            center_up = pre.circ(self.gcra(r[i * 4 + 3], runout[i * 4 + 3], 0, theta[i]))
            results = pre.eccentric(center_down[1], center_down[2], center_up[1], center_up[2], vector_down[0], vector_down[1], vector_down[2], vector_up[0], vector_up[1], vector_up[2], H[i])
            p[i] = np.array([[1, 0, results[2], results[0]], [0, 1, results[3], results[1]], [-results[2], -results[3], 1, H[i]], [0, 0, 0, 1]])
        e, phase = [0] * (len(p)), [0] * (len(p))
        m = 1
        for i in range(len(p)):
            m = np.dot(m, p[i])
            #偏心量
            e[i] = np.sqrt(m[0, 3] ** 2 + m[1, 3] ** 2)
            #偏心相位
            phase[i] = self.get_phase(m[0, 3], m[1, 3])
        return np.stack((e, phase), axis=1)
    
    def bias_n_li_fast(self, theta):  #接收一个list类型的theta参数；返回【所有级】的结果
        # runout = self.runout
        # r = self.r
        H = self.H
        para = self.para
        p = [0] * (len(theta))
        for i in range(len(theta)):
            vector_down = para[i * 4][int(theta[i] / 10)]
            vector_up = para[i * 4 + 1][int(theta[i] / 10)]
            center_down = para[i * 4 + 2][int(theta[i] / 10)]
            center_up = para[i * 4 + 3][int(theta[i] / 10)]
            results = pre.eccentric(center_down[1], center_down[2], center_up[1], center_up[2], vector_down[0], vector_down[1], vector_down[2], vector_up[0], vector_up[1], vector_up[2], H[i])
            p[i] = np.array([[1, 0, results[2], results[0]], [0, 1, results[3], results[1]], [-results[2], -results[3], 1, H[i]], [0, 0, 0, 1]])
        e, phase = [0] * (len(p)), [0] * (len(p))
        m = 1
        for i in range(len(p)):
            m = np.dot(m, p[i])
            #偏心量
            e[i] = np.sqrt(m[0, 3] ** 2 + m[1, 3] ** 2)
            #偏心相位
            phase[i] = self.get_phase(m[0, 3], m[1, 3])
        return np.stack((e, phase), axis=1)
    
    def bias_n_li_fast_sum(self, theta):  #接收一个list类型的theta参数；分别返回【所有级】的偏心值和偏心相位结果【之和】
        # runout = self.runout
        # r = self.r
        H = self.H
        para = self.para
        p = [0] * (len(theta))
        for i in range(len(theta)):
            vector_down = para[i * 4][int(theta[i] / 10)]
            vector_up = para[i * 4 + 1][int(theta[i] / 10)]
            center_down = para[i * 4 + 2][int(theta[i] / 10)]
            center_up = para[i * 4 + 3][int(theta[i] / 10)]
            results = pre.eccentric(center_down[1], center_down[2], center_up[1], center_up[2], vector_down[0], vector_down[1], vector_down[2], vector_up[0], vector_up[1], vector_up[2], H[i])
            p[i] = np.array([[1, 0, results[2], results[0]], [0, 1, results[3], results[1]], [-results[2], -results[3], 1, H[i]], [0, 0, 0, 1]])
        e, phase = [0] * (len(p)), [0] * (len(p))
        m = 1
        for i in range(len(p)):
            m = np.dot(m, p[i])
            #偏心量
            e[i] = np.sqrt(m[0, 3] ** 2 + m[1, 3] ** 2)
            #偏心相位
            phase[i] = self.get_phase(m[0, 3], m[1, 3])
        sum_e, sum_phase = 0, 0
        for i in range(len(e) - 1):
            sum_e += abs(e[i + 1] - e[i])
        for i in range(len(phase) - 1):
            sum_phase += abs(phase[i + 1] - phase[i])
        return [sum_e, sum_phase]
    
    def bias_n_li_fast_dert_e(self, theta):  #接收一个list类型的theta参数；分别返回【所有级】的dert_e【之和】
        # runout = self.runout
        # r = self.r
        H = self.H
        para = self.para
        p = [0] * (len(theta))
        for i in range(len(theta)):
            vector_down = para[i * 4][int(theta[i] / 10)]
            vector_up = para[i * 4 + 1][int(theta[i] / 10)]
            center_down = para[i * 4 + 2][int(theta[i] / 10)]
            center_up = para[i * 4 + 3][int(theta[i] / 10)]
            results = pre.eccentric(center_down[1], center_down[2], center_up[1], center_up[2], vector_down[0], vector_down[1], vector_down[2], vector_up[0], vector_up[1], vector_up[2], H[i])
            p[i] = np.array([[1, 0, results[2], results[0]], [0, 1, results[3], results[1]], [-results[2], -results[3], 1, H[i]], [0, 0, 0, 1]])
        e, phase = [0] * (len(p)), [0] * (len(p))
        m = 1
        M = []
        M.append(np.zeros((4, 4)))
        for i in range(len(p)):
            m = np.dot(m, p[i])
            e[i] = np.sqrt(m[0, 3] ** 2 + m[1, 3] ** 2)
            phase[i] = self.get_phase(m[0, 3], m[1, 3])
            M.append(m)
        dert_e = np.zeros((len(M) - 1, 1))
        for i in range(len(M) - 1):
            dert_e[i] = np.sqrt((M[i + 1][0, 3] - M[i][0, 3]) ** 2 + (M[i + 1][1, 3] - M[i][1, 3]) ** 2) + np.sqrt(M[i + 1][0, 3] ** 2 + M[i + 1][1, 3] ** 2)
        return dert_e
    
    def bias_n_li_fast_e_projection(self, theta):  #接收一个list类型的theta参数；分别返回【所有级】的e_projection【之和】
        # runout = self.runout
        # r = self.r
        H = self.H
        para = self.para
        p = [0] * (len(theta))
        for i in range(len(theta)):
            vector_down = para[i * 4][int(theta[i] / 10)]
            vector_up = para[i * 4 + 1][int(theta[i] / 10)]
            center_down = para[i * 4 + 2][int(theta[i] / 10)]
            center_up = para[i * 4 + 3][int(theta[i] / 10)]
            results = pre.eccentric(center_down[1], center_down[2], center_up[1], center_up[2], vector_down[0], vector_down[1], vector_down[2], vector_up[0], vector_up[1], vector_up[2], H[i])
            p[i] = np.array([[1, 0, results[2], results[0]], [0, 1, results[3], results[1]], [-results[2], -results[3], 1, H[i]], [0, 0, 0, 1]])
        # 保存各级零件偏心坐标
        center = np.zeros((len(p) + 1, 3))
        m = 1
        e, phase = [0] * (len(p)), [0] * (len(p))
        M = []
        M.append(np.zeros((4, 4)))
        for i in range(len(p)):
            m = np.dot(m, p[i])
            center[i + 1, :] = m[0:3, 3]
            e[i] = np.sqrt(m[0, 3] ** 2 + m[1, 3] ** 2)
            phase[i] = self.get_phase(m[0, 3], m[1, 3])
            M.append(m)
        # alpha = np.arctan(np.sqrt(m[0, 3] ** 2 + m[1, 3] ** 2) / m[2, 3])  # 轴线偏斜角
        # rot_x = 
        # rot_y = 
        # rot_z = 
        rot_axis_vector = np.array([m[0, 3], m[1, 3], m[2, 3]])  # 实际回转轴线法向量
        a, b, c = rot_axis_vector
        e_projection = np.zeros((len(p), 1))
        for i in range(len(p)):
            le = np.sqrt((center[i + 1, 0] - center[0, 0]) ** 2 + (center[i + 1, 1] - center[0, 1]) ** 2 + (center[i + 1, 2] - center[0, 2]) **2)
            d = abs(a * center[i + 1, 0] + b * center[i + 1, 1] + c *  center[i + 1, 2]) / np.sqrt(a ** 2 + b ** 2 + c ** 2)  # 点到平面距离
            e_projection[i] = np.sqrt(abs(le ** 2 - d ** 2))
        return e_projection
    
    def bias_n_li_fast_dert_e_projection(self, theta):  #接收一个list类型的theta参数；分别返回【所有级】的e和dert_e【之和】
        # runout = self.runout
        # r = self.r
        H = self.H
        para = self.para
        p = [0] * (len(theta))
        for i in range(len(theta)):
            vector_down = para[i * 4][int(theta[i] / 10)]
            vector_up = para[i * 4 + 1][int(theta[i] / 10)]
            center_down = para[i * 4 + 2][int(theta[i] / 10)]
            center_up = para[i * 4 + 3][int(theta[i] / 10)]
            results = pre.eccentric(center_down[1], center_down[2], center_up[1], center_up[2], vector_down[0], vector_down[1], vector_down[2], vector_up[0], vector_up[1], vector_up[2], H[i])
            p[i] = np.array([[1, 0, results[2], results[0]], [0, 1, results[3], results[1]], [-results[2], -results[3], 1, H[i]], [0, 0, 0, 1]])
        # 保存各级零件偏心坐标
        center = np.zeros((len(p) + 1, 3))
        m = 1
        e, phase = [0] * (len(p)), [0] * (len(p))
        M = []
        M.append(np.zeros((4, 4)))
        for i in range(len(p)):
            m = np.dot(m, p[i])
            center[i + 1, :] = m[0:3, 3]
            e[i] = np.sqrt(m[0, 3] ** 2 + m[1, 3] ** 2)
            phase[i] = self.get_phase(m[0, 3], m[1, 3])
            M.append(m)
        # alpha = np.arctan(np.sqrt(m[0, 3] ** 2 + m[1, 3] ** 2) / m[2, 3])  # 轴线偏斜角
        # rot_x = 
        # rot_y = 
        # rot_z = 
        rot_axis_vector = np.array([m[0, 3], m[1, 3], m[2, 3]])  # 实际回转轴线法向量
        a, b, c = rot_axis_vector
        e_projection = np.zeros((len(p), 1))
        for i in range(len(p)):
            le = np.sqrt((center[i + 1, 0] - center[0, 0]) ** 2 + (center[i + 1, 1] - center[0, 1]) ** 2 + (center[i + 1, 2] - center[0, 2]) **2)
            d = abs(a * center[i + 1, 0] + b * center[i + 1, 1] + c *  center[i + 1, 2]) / np.sqrt(a ** 2 + b ** 2 + c ** 2)  # 点到平面距离
            e_projection[i] = np.sqrt(le ** 2 - d ** 2)
        dert_e_projection = np.zeros((len(p), 1))
        for i in range(len(e_projection) - 1):
            dert_e_projection[i] = (e_projection[i + 1] - e_projection[i])
        return dert_e_projection
    
    def bias_n_li_fast_dert_phase(self, theta):  #接收一个list类型的theta参数；分别返回【所有级】的dert_phase【之和】
        # runout = self.runout
        # r = self.r
        H = self.H
        para = self.para
        p = [0] * (len(theta))
        for i in range(len(theta)):
            vector_down = para[i * 4][int(theta[i] / 10)]
            vector_up = para[i * 4 + 1][int(theta[i] / 10)]
            center_down = para[i * 4 + 2][int(theta[i] / 10)]
            center_up = para[i * 4 + 3][int(theta[i] / 10)]
            results = pre.eccentric(center_down[1], center_down[2], center_up[1], center_up[2], vector_down[0], vector_down[1], vector_down[2], vector_up[0], vector_up[1], vector_up[2], H[i])
            p[i] = np.array([[1, 0, results[2], results[0]], [0, 1, results[3], results[1]], [-results[2], -results[3], 1, H[i]], [0, 0, 0, 1]])
        e, phase = [0] * (len(p)), [0] * (len(p))
        m = 1
        for i in range(len(p)):
            m = np.dot(m, p[i])
            e[i] = np.sqrt(m[0, 3] ** 2 + m[1, 3] ** 2)
            phase[i] = self.get_phase(m[0, 3], m[1, 3])
        dert_phase = np.zeros((len(phase) - 1, 1))
        for i in range(len(phase) - 1):
            dert_phase[i] = np.arctan(abs(phase[i + 1] - phase[i])) * 180 / np.pi
        return dert_phase
    
    def plot_center(self, theta):  #接收一个list类型的theta参数；返回各级偏心坐标及相位
        H = self.H
        para = self.para
        p = [0] * (len(theta))
        for i in range(len(theta)):
            vector_down = para[i * 4][int(theta[i] / 10)]
            vector_up = para[i * 4 + 1][int(theta[i] / 10)]
            center_down = para[i * 4 + 2][int(theta[i] / 10)]
            center_up = para[i * 4 + 3][int(theta[i] / 10)]
            results = pre.eccentric(center_down[1], center_down[2], center_up[1], center_up[2], vector_down[0], vector_down[1], vector_down[2], vector_up[0], vector_up[1], vector_up[2], H[i])
            p[i] = np.array([[1, 0, results[2], results[0]], [0, 1, results[3], results[1]], [-results[2], -results[3], 1, H[i]], [0, 0, 0, 1]])
        center = np.zeros((len(p) + 1, 3))
        m = 1
        for i in range(len(p)):
            m = np.dot(m, p[i])
            center[i + 1, :] = m[0:3, 3]
        return center

