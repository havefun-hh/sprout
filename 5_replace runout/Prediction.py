# from dataclasses import dataclass
from numpy import linalg as la
import numpy as np
import pandas as pd


# @dataclass
class Prediction():
    """
    拟合法向量、圆心
    """
    # def __init__(self, runout):
    #     self.runout = runout
    
    # def idata(ad, usecols):                       #(import data)导入第n列跳动数据；ad——地址
    #     data = np.array(pd.read_csv(ad, usecols=usecols))
    #     data = np.squeeze(data)
    #     return data
    
    def idata(ad, usecols):     #(import data)导入第n列数据
        data = np.array(pd.read_csv(ad, usecols=usecols))
        data = np.squeeze(data)
        return data
    
    def gcfl(r, runout, H):                #(generate coordinates--flat)生成端面的直角坐标
        theta = np.linspace((2 * np.pi) / len(runout), 2 * np.pi, len(runout))
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = H + runout
        data = np.stack((x, y, z), axis=1)
        return data
    
    def planefit(data):                          #(plane fit)拟合平面法向量
        U,sigma,VT = la.svd(data)
        a = VT[2, 0]
        b = VT[2, 1]
        c = VT[2, 2]
        d = -a * data[0, 0] - b * data[0, 1] - c * data[0, 2]
        result = np.array([a, b, c, d])
        return result
    
    def gcra(r, runout, H):                #(generate coordinates--radial)生成止口的直角坐标
        theta = np.linspace((2 * np.pi) / len(runout), 2 * np.pi, len(runout))
        x, y = [], []
        for i in range(len(theta)):
            x.append((r + runout[i]) * np.cos(theta[i]))
            y.append((r + runout[i]) * np.sin(theta[i]))
        x = np.array(x).reshape(-1, 1)
        x = np.squeeze(x)
        y = np.array(y).reshape(-1, 1)
        y = np.squeeze(y)
        z = np.array([H] * len(runout))
        data = np.dstack((x, y, z))
        data = np.squeeze(data)
        return data
    
    def circ(data):
        x = data[:, 0]
        y = data[:, 1]
        x1, x2, x3, y1, y2, y3, x1y1, x1y2, x2y1 = 0, 0, 0, 0, 0, 0, 0, 0, 0
        N = len(data[:, 0])
        for i in range(N):
            x1 = x1 + x[i]
            x2 = x2 + x[i] * x[i]
            x3 = x3 + x[i] * x[i] * x[i]
            y1 = y1 + y[i]
            y2 = y2 + y[i] * y[i]
            y3 = y3 + y[i] * y[i] * y[i]
            x1y1 = x1y1 + x[i] * y[i]
            x1y2 = x1y2 + x[i] * y[i] * y[i]
            x2y1 = x2y1 + x[i] * x[i] * y[i]
        C = N * x2 - x1 * x1
        D = N * x1y1 - x1 * y1
        E = N * x3 + N * x1y2 - (x2 + y2) * x1
        G = N * y2 - y1 * y1
        H = N * x2y1 + N * y3 - (x2 + y2) * y1
        a = (H * D - E * G) / (C * G - D * D)
        b = (H * C - E * D) / (D * D - G * C)
        c = -(a * x1 + b * y1 + x2 + y2) / N
        A = a/(-2)
        B = b/(-2)
        R = np.sqrt(a * a + b * b - 4 * c) / 2
        result = [R, A, B]
        return result

    def spin(runout, theta):
        H = len(runout)
        Hr = np.round(theta / 360 * H)
        Hr = int(Hr)
        a = list(runout[Hr:H])
        b = list(runout[:Hr])
        a.extend(b)
        new_runout = np.array(a)
        return new_runout

    def eccentric(A1, B1, A2, B2, a1, b1, c1, a2, b2, c2, L):
        a = a2 / c2 - a1 / c1
        b = b2 / c2 - b1 / c1
        A = A2 - A1 + L * np.sin(-a1 / c1)
        B = B2 - B1 + L * np.sin(-b1 / c1)
        result = [A, B, a, b]
        return result

