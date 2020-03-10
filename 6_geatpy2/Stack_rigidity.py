"""根据装配后测试数据，反求偏心偏斜量"""
import numpy as np
from Prediction import Prediction as pre


class Stack_rigidity():
    def __init__(self, runout, r, H):
        self.runout = runout
        self.r = r
        self.H = H
        
    def gcra(self, r, runout, h, theta):                #(generate coordinates--radial)生成止口的直角坐标；theta顺时针为正
        H = len(runout)
        Hr = np.round(theta / 360 * H)
        Hr = int(Hr)
        a = list(runout[Hr:H])
        b = list(runout[:Hr])
        a.extend(b)
        new_runout = np.array(a)
        t = np.linspace(np.pi / 1800, 2 * np.pi, 3600)
        x, y = [], []
        for i in range(len(t)):
            x.append((r + new_runout[i]) * np.cos(t[i]))
            y.append((r + new_runout[i]) * np.sin(t[i]))
        x = np.array(x)
        y = np.array(y)
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
        phase = np.arctan(m[1, 3] / m[0, 3]) * 180 / np.pi
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
            phase[i] = np.arctan(m[1, 3] / m[0, 3]) * 180 / np.pi
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
            phase[i] = np.arctan(m[1, 3] / m[0, 3]) * 180 / np.pi
        return np.stack((e, phase), axis=1)









