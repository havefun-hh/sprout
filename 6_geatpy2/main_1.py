# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 18:49:07 2020

@author: Lenovo
"""
import numpy as np
import geatpy as ea # import geatpy
from MyProblem_1 import MyProblem_1 # 导入自定义问题接口
from Prediction import Prediction as pre
from Stack_rigidity import Stack_rigidity


if __name__ == '__main__':
    """===============================实例化问题对象==========================="""
    ad_part1 = 'G:/190708-190712data/MNJ-HPC-002ZP1-20190709.csv'
    ad_part2 = 'G:/190708-190712data/MNJ-HPT-001ZP1-20190708.csv'
    part1_flat_runout_down = -pre.idata(ad_part1, [3])# 单件1第4列————基准面端跳
    part1_flat_runout_up = pre.idata(ad_part1, [1])# 单件1第2列————位置面端跳
    part1_radial_runout_down = pre.idata(ad_part1, [4])# 单件1第5列————基准面端跳
    part1_radial_runout_up = -pre.idata(ad_part1, [2])# 单件1第3列————位置面端跳
    part2_flat_runout_down = -pre.idata(ad_part2, [4])# 单件1第5列————基准面端跳
    part2_flat_runout_up = pre.idata(ad_part2, [2])# 单件1第3列————位置面端跳
    part2_radial_runout_down = pre.idata(ad_part2, [3])# 单件1第4列————基准面端跳
    part2_radial_runout_up = pre.idata(ad_part2, [1])# 单件1第2列————位置面端跳
    runout = np.stack((part1_flat_runout_down, part1_flat_runout_up, part1_radial_runout_down, part1_radial_runout_up, part2_flat_runout_down, part2_flat_runout_up, part2_radial_runout_down, part2_radial_runout_up), axis=0)
    part1_r_flat_down = 84 / 2
    part1_r_flat_up = 206.5 / 2
    part1_r_radial_down = 80 / 2
    part1_r_radial_up = 200 / 2
    part2_r_flat_down = 206.5 / 2
    part2_r_flat_up = 84 / 2
    part2_r_radial_down = 200 / 2
    part2_r_radial_up = 80 / 2
    r = [part1_r_flat_down, part1_r_flat_up, part1_r_radial_down, part1_r_radial_up, part2_r_flat_down, part2_r_flat_up, part2_r_radial_down, part2_r_radial_up]
    aim = Stack_rigidity(runout, r, [687, 388])
    problem = MyProblem_1(aim) # 生成问题对象
    """=================================种群设置==============================="""
    Encoding = 'RI'       # 编码方式
    NIND = 10            # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders) # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND) # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """===============================算法参数设置============================="""
    myAlgorithm = ea.soea_SEGA_templet(problem, population) # 实例化一个算法模板对象
    # myAlgorithm.mutOper.Pm = 0.2 # 修改变异算子的变异概率
    # myAlgorithm.recOper.XOVR = 0.9 # 修改交叉算子的交叉概率
    myAlgorithm.MAXGEN = 20 # 最大进化代数
    myAlgorithm.drawing = 2 # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）
    """==========================调用算法模板进行种群进化======================="""
    [population, obj_trace, var_trace] = myAlgorithm.run() # 执行算法模板
    population.save() # 把最后一代种群的信息保存到文件中
    # 输出结果
    best_gen = np.argmin(problem.maxormins * obj_trace[:, 1]) # 记录最优种群个体是在哪一代
    best_ObjV = obj_trace[best_gen, 1]
    print('最优的目标函数值为：%s'%(best_ObjV))
    print('相位为：%s'%(aim.bias_2(0, var_trace[best_gen] * 10)[1]))
    for i in range(var_trace.shape[1]):
        print('最优的控制变量值为：%s'%(var_trace[best_gen, i] * 10))
    print('有效进化代数：%s'%(obj_trace.shape[0]))
    print('最优的一代是第 %s 代'%(best_gen + 1))
    print('评价次数：%s'%(myAlgorithm.evalsNum))
    print('时间已过 %.8s 秒'%(myAlgorithm.passTime))
