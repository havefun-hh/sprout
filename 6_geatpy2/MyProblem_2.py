# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 18:22:41 2020

@author: admin
"""
import numpy as np
import pandas as pd
import geatpy as ea   # import geatpy
from Stack_rigidity import Stack_rigidity
import multiprocessing as mp
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool


class MyProblem(ea.Problem): # 继承Problem父类
    def __init__(self, aim, n, Dim, phase):
        self.aim = aim
        self.n = n
        self.phase = phase
        name = 'MyProblem' # 初始化name（函数名称，可以随意设置）
        M = 1 # 初始化M（目标维数）
        maxormins = [1] # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        #Dim = 2 # 初始化Dim（决策变量维数）——只考虑两级装配，只有一个自变量（端跳差分值）
        Dim = Dim
        varTypes = [1] * Dim # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0] * Dim # 决策变量下界
        ub = [35] * Dim # 决策变量上界
        lbin = [1] * Dim # 决策变量下边界
        ubin = [1] * Dim # 决策变量上边界
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
    
    def aimFunc(self, pop): # 目标函数
        aim = self.aim
        n = self.n
        phase = self.phase
        Vars = pop.Phen # 得到决策变量矩阵
        # x1 = Vars[:, [0]] * 10
        # x2 = Vars[:, [1]] * 10
        f = np.zeros((len(Vars[:, 0]), 1))
        for i in range(len(Vars[:, 0])):
            if phase == None:
                x = [0] + [j * 10 for j in Vars[i, :]]  # 注意Vars的切片要×10
                a = aim.bias_n_li_fast(x)
                f[i] = max(a[n + 1:, 0])
            else:
                x = phase + [j * 10 for j in Vars[i, :]]
                a = aim.bias_n_li_fast(x)
                f[i] = max(a[n:, 0])
        pop.ObjV = f # 计算目标函数值，赋值给pop种群对象的ObjV属性


class MyProblem_aim2(ea.Problem): # 继承Problem父类
    def __init__(self, aim, n, Dim, phase):
        self.aim = aim
        self.n = n
        self.phase = phase
        name = 'MyProblem' # 初始化name（函数名称，可以随意设置）
        M = 1 # 初始化M（目标维数）
        maxormins = [1] # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        #Dim = 2 # 初始化Dim（决策变量维数）——只考虑两级装配，只有一个自变量（端跳差分值）
        Dim = Dim
        varTypes = [1] * Dim # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0] * Dim # 决策变量下界
        ub = [35] * Dim # 决策变量上界
        lbin = [1] * Dim # 决策变量下边界
        ubin = [1] * Dim # 决策变量上边界
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
    
    def aimFunc(self, pop): # 目标函数
        aim = self.aim
        n = self.n
        phase = self.phase
        Vars = pop.Phen # 得到决策变量矩阵
        # x1 = Vars[:, [0]] * 10
        # x2 = Vars[:, [1]] * 10
        f = np.zeros((len(Vars[:, 0]), 1))
        for i in range(len(Vars[:, 0])):
            if phase == None:
                x = [0] + [j * 10 for j in Vars[i, :]]  # 注意Vars的切片要×10
                f[i] = sum(aim.bias_n_li_fast_dert_e(x))
            else:
                x = phase + [j * 10 for j in Vars[i, :]]
                f[i] = sum(aim.bias_n_li_fast_dert_e(x))
        pop.ObjV = f # 计算目标函数值，赋值给pop种群对象的ObjV属性


class MyProblem_aim3(ea.Problem): # 继承Problem父类
    def __init__(self, aim, n, Dim, phase):
        self.aim = aim
        self.n = n
        self.phase = phase
        name = 'MyProblem' # 初始化name（函数名称，可以随意设置）
        M = 1 # 初始化M（目标维数）
        maxormins = [1] # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        #Dim = 2 # 初始化Dim（决策变量维数）——只考虑两级装配，只有一个自变量（端跳差分值）
        Dim = Dim
        varTypes = [1] * Dim # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0] * Dim # 决策变量下界
        ub = [35] * Dim # 决策变量上界
        lbin = [1] * Dim # 决策变量下边界
        ubin = [1] * Dim # 决策变量上边界
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
    
    def aimFunc(self, pop): # 目标函数
        aim = self.aim
        n = self.n
        phase = self.phase
        Vars = pop.Phen # 得到决策变量矩阵
        # x1 = Vars[:, [0]] * 10
        # x2 = Vars[:, [1]] * 10
        f = np.zeros((len(Vars[:, 0]), 1))
        for i in range(len(Vars[:, 0])):
            if phase == None:
                x = [0] + [j * 10 for j in Vars[i, :]]  # 注意Vars的切片要×10
                f[i] = sum(aim.bias_n_li_fast_e_projection(x))
            else:
                x = phase + [j * 10 for j in Vars[i, :]]
                f[i] = sum(aim.bias_n_li_fast_e_projection(x))
        pop.ObjV = f # 计算目标函数值，赋值给pop种群对象的ObjV属性

class MyProblem_aim4(ea.Problem): # 继承Problem父类
    def __init__(self, aim, n, Dim, phase):
        self.aim = aim
        self.n = n
        self.phase = phase
        name = 'MyProblem' # 初始化name（函数名称，可以随意设置）
        M = 1 # 初始化M（目标维数）
        maxormins = [1] # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        #Dim = 2 # 初始化Dim（决策变量维数）——只考虑两级装配，只有一个自变量（端跳差分值）
        Dim = Dim
        varTypes = [1] * Dim # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0] * Dim # 决策变量下界
        ub = [35] * Dim # 决策变量上界
        lbin = [1] * Dim # 决策变量下边界
        ubin = [1] * Dim # 决策变量上边界
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
    
    def aimFunc(self, pop): # 目标函数
        aim = self.aim
        n = self.n
        phase = self.phase
        Vars = pop.Phen # 得到决策变量矩阵
        # x1 = Vars[:, [0]] * 10
        # x2 = Vars[:, [1]] * 10
        f = np.zeros((len(Vars[:, 0]), 1))
        for i in range(len(Vars[:, 0])):
            if phase == None:
                x = [0] + [j * 10 for j in Vars[i, :]]  # 注意Vars的切片要×10
                f[i] = sum(aim.bias_n_li_fast_dert_phase(x))
            else:
                x = phase + [j * 10 for j in Vars[i, :]]
                f[i] = sum(aim.bias_n_li_fast_dert_phase(x))
        pop.ObjV = f # 计算目标函数值，赋值给pop种群对象的ObjV属性
    
    
class MyProblem_multiprocess(ea.Problem): # 继承Problem父类（多进程多线程）
    def __init__(self, aim, n, Dim, phase, PoolType): # PoolType是取值为'Process'或'Thread'的字符串
        self.aim = aim
        self.n = n
        self.phase = phase
        self.PoolType = PoolType
        name = 'MyProblem' # 初始化name（函数名称，可以随意设置）
        M = 1 # 初始化M（目标维数）
        maxormins = [1] # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        #Dim = 2 # 初始化Dim（决策变量维数）——只考虑两级装配，只有一个自变量（端跳差分值）
        Dim = Dim
        varTypes = [1] * Dim # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0] * Dim # 决策变量下界
        ub = [35] * Dim # 决策变量上界
        lbin = [1] * Dim # 决策变量下边界
        ubin = [1] * Dim # 决策变量上边界
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
        if self.PoolType == 'Thread':
            self.pool = ThreadPool(12) # 设置线程池的大小
        elif self.PoolType == 'Process':
            num_cores = int(mp.cpu_count()) # 获得计算机的核心数
            self.pool = ProcessPool(num_cores) # 设置池的大小
    
    def aimFunc(self, pop): # 目标函数
        aim = self.aim
        n = self.n
        phase = self.phase
        Vars = pop.Phen # 得到决策变量矩阵
        args = list(zip(Vars, [aim] * len(Vars[:, 0]), [n] * len(Vars[:, 0]), [phase] * len(Vars[:, 0])))  #list(zip(list()))
        if self.PoolType == 'Thread':
            pop.ObjV = np.array(list(self.pool.map(subAimFunc, args))).reshape(-1, 1)  #geatpy规定种群的目标函数值(ObjV)矩阵必须是n行1列的numpy array类型矩阵,原返回类型为（10,），使用reshape将其增加一维
        elif self.PoolType == 'Process':
            result = self.pool.map_async(subAimFunc, args)
            result.wait()
            pop.ObjV = np.array(result.get()).reshape(-1, 1)


def subAimFunc(args):
    Vars = args[0]     # 每次传入一行Vars值
    aim = args[1]
    n = args[2]
    phase = args[3]
    if phase == None:
        x = [0] + [i * 10 for i in Vars]  # 注意Vars的切片要×10
        a = aim.bias_n_li_fast(x)
        f = max(a[n + 1:, 0])
    else:
        x = phase + [i * 10 for i in Vars]
        a = aim.bias_n_li_fast(x)
        f = max(a[n:, 0])
    return f




