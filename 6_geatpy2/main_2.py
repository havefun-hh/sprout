# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 18:23:19 2020

@author: admin
"""
import numpy as np
import geatpy as ea # import geatpy
from MyProblem_2 import MyProblem # 导入自定义问题接口
from Prediction import Prediction as pre
from Stack_rigidity import Stack_rigidity


if __name__ == '__main__':
    """===============================实例化问题对象==========================="""
    ad_part1 = 'G:/190708-190712data/MNJ-HPC-002ZP1-20190709.csv'
    ad_part2 = 'G:/190708-190712data/MNJ-HPT-001ZP1-20190708.csv'
    ad_part3 = 'G:/190708-190712data/MNJ-HPC-001ZP2-20190708.csv'
    runout = np.stack((-pre.idata(ad_part1, [3]), pre.idata(ad_part1, [1]), pre.idata(ad_part1, [4]), 
                       -pre.idata(ad_part1, [2]), -pre.idata(ad_part2, [4]), pre.idata(ad_part2, [2]), 
                       pre.idata(ad_part2, [3]), pre.idata(ad_part2, [1]), -pre.idata(ad_part3, [3]), 
                       pre.idata(ad_part3, [1]), pre.idata(ad_part3, [4]), pre.idata(ad_part3, [2])), axis=0)
    r = [84/2, 206.5/2, 80/2, 200/2, 206.5/2, 84/2, 200/2, 80/2, 
         84/2, 206.5/2, 80/2, 200/2]
    h = [192, 120, 192]
    aim = Stack_rigidity(runout, r, h)
    Dim = 2
    n = 0
    phase = None
    problem = MyProblem(aim, n, Dim, phase) # 生成问题对象
    """=================================种群设置==============================="""
    Encoding = 'RI'       # 编码方式
    NIND = 15            # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders) # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND) # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """===============================算法参数设置============================="""
    myAlgorithm = ea.soea_studGA_templet(problem, population) # 实例化一个算法模板对象
    myAlgorithm.MAXGEN = 15 # 最大进化代数
    myAlgorithm.drawing = 2 # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）
    """==========================调用算法模板进行种群进化======================="""
    [population, obj_trace, var_trace] = myAlgorithm.run() # 执行算法模板
    population.save() # 把最后一代种群的信息保存到文件中
    # 输出结果
    best_gen = np.argmin(problem.maxormins * obj_trace[:, 1]) # 记录最优种群个体是在哪一代
    best_ObjV = obj_trace[best_gen, 1]
    print('最优的目标函数值为：%.8smm'%(best_ObjV))
    phase = [0] + [i*10 for i in var_trace[best_gen, :]]
    res = aim.bias_n_li(phase)
    find_index = np.where(max(res[1:, 0]) == res[1:, 0])[0][0] + 1
    print('所在位置及相位偏斜角为：第%s级与第%s级连接处; %.8s°' % (find_index + 1, find_index + 2, res[find_index, 1]))
    for i in range(len(phase)):
        print('第%s级相位、偏心值及相位偏斜角为：%s°; %.8smm; %.8s°' % (i+1, phase[i], res[i, 0], res[i, 1]))
    print('有效进化代数：%s' % (obj_trace.shape[0]))
    print('最优的一代是第 %s 代' % (best_gen + 1))
    print('评价次数：%s' % (myAlgorithm.evalsNum))
    print('时间已过 %.8s 秒' % (myAlgorithm.passTime))

