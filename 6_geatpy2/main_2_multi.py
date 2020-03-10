# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 21:17:35 2020

@author: admin
"""
import numpy as np
import geatpy as ea # import geatpy
import time
from MyProblem_2 import MyProblem_multiprocess # 导入自定义问题接口
from Prediction import Prediction as pre
from Stack_rigidity import Stack_rigidity


def main(aim, n, Dim, phase):
    """===============================实例化问题对象==========================="""
    PoolType = 'Process' # 设置采用多进程，若修改为: PoolType = 'Thread'，则表示用多线程
    problem = MyProblem_multiprocess(aim, n, Dim, phase, PoolType) # 生成问题对象
    """=================================种群设置==============================="""
    Encoding = 'RI'       # 编码方式
    NIND = 10            # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders) # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND) # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """===============================算法参数设置============================="""
    myAlgorithm = ea.soea_SGA_templet(problem, population) # 实例化一个算法模板对象
    # myAlgorithm.mutOper.Pm = 1 # 修改变异算子的变异概率(原模板中breeder GA变异算子的Pm定义为1 / Dim)
    # myAlgorithm.recOper.XOVR = 0.9 # 修改交叉算子的交叉概率
    myAlgorithm.MAXGEN = 15 # 最大进化代数
    myAlgorithm.trappedValue = 1e-6 # “进化停滞”判断阈值
    myAlgorithm.maxTrappedCount = 10 # 进化停滞计数器最大上限值，如果连续maxTrappedCount代被判定进化陷入停滞，则终止进化
    myAlgorithm.drawing = 2 # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）
    """==========================调用算法模板进行种群进化======================="""
    [population, obj_trace, var_trace] = myAlgorithm.run() # 执行算法模板
    population.save() # 把最后一代种群的信息保存到文件中
    # 输出结果
    best_gen = np.argmin(problem.maxormins * obj_trace[:, 1]) # 记录最优种群个体是在哪一代
    best_ObjV = obj_trace[best_gen, 1]
    print('最优的目标函数值为：%.8smm'%(best_ObjV))
    if phase == None:
        phase = [0] + [i*10 for i in var_trace[best_gen, :]]      # 第一次算出的所有相位值
        res = aim.bias_n_li(phase)
        find_index = np.where(max(res[n + 1:, 0]) == res[n + 1:, 0])[0][0] + 1    # 第一次最大偏心值的索引位置（此处res内的n+1和最后面的+1表示：不考虑第一级，整体向后偏移一位）
    else:
        phase = phase + [i*10 for i in var_trace[best_gen, :]]    # 所有相位值(后续几级相位值有更新)
        res = aim.bias_n_li(phase)
        find_index = np.where(max(res[n:, 0]) == res[n:, 0])[0][0]    # 每次的最大偏心值的索引位置
    print('所在位置及相位偏斜角为：第%s级零件末端; %.8s°' % (find_index + 1 + n, res[find_index + n, 1]))
    if n == 0:
        for i in range(len(phase)):
            print('第%s级相位、偏心值及相位偏斜角为：%s°; %.8smm; %.8s°' % (i + 1, phase[i], res[i, 0], res[i, 1]))
    else:
        for i in range(var_trace.shape[1]):
            print('第%s级相位、偏心值及相位偏斜角为：%s°; %.8smm; %.8s°' % (i + (n + 1), phase[i + n], res[i + n, 0], res[i + n, 1]))
    print('有效进化代数：%s' % (obj_trace.shape[0]))
    print('最优的一代是第 %s 代' % (best_gen + 1))
    print('评价次数：%s' % (myAlgorithm.evalsNum))
    print('时间已过 %s 分 %.8s 秒' % (int(myAlgorithm.passTime // 60), myAlgorithm.passTime % 60))
    n = n + int((find_index + 1))         # 计算累计固定好的级数(此处find_index类型为int64,改为int类型防止后面报错！)
    return myAlgorithm, obj_trace, var_trace, best_gen, best_ObjV, phase, res, n


if __name__ == '__main__':
    ad_part1 = 'G:/190708-190712data/MNJ-HPC-002ZP1-20190709.csv'
    ad_part2 = 'G:/190708-190712data/MNJ-HPT-001ZP1-20190708.csv'
    ad_part3 = 'G:/190708-190712data/MNJ-HPC-001ZP2-20190708.csv'
    # new_part1--part2--part1
    runout = np.stack((-pre.idata(ad_part1, [3]), pre.idata(ad_part1, [1]), pre.idata(ad_part1, [4]), 
                       -pre.idata(ad_part1, [2]), -pre.idata(ad_part2, [4]), pre.idata(ad_part2, [2]), 
                       pre.idata(ad_part2, [3]), pre.idata(ad_part2, [1]), -pre.idata(ad_part3, [3]), 
                       pre.idata(ad_part3, [1]), pre.idata(ad_part3, [4]), pre.idata(ad_part3, [2])), axis=0)
    r = [84/2, 206.5/2, 80/2, 200/2, 206.5/2, 84/2, 200/2, 80/2, 
         84/2, 206.5/2, 80/2, 200/2]
    h = [192, 120, 192]
    Dim = 2          # 初始决策变量维数(=总的级数-1)
    n = 0            # 累计的已固定好的级数
    aim = Stack_rigidity(runout, r, h)
    myAlgorithm, obj_trace, var_trace, best_gen, best_ObjV, phase, res, n = main(aim, n, Dim, phase=None)
    """==========================判断是否再次使用算法======================="""
    while len(res[:, 0]) - n > 0:     # 如果未固定好的级数(=总的级数-已固定好的级数)大于0，则还需继续搜索，直到一级也不剩时终止。
        print('---------------------------------------------------------------')
        print('后续最优相位寻找中...')
        Dim = len(res[:, 0]) - n  # 更新后的决策变量维数
        if Dim == 1:                  # 如果只剩最后一级零件，则遍历找出最优
            start = time.perf_counter()
            traversal = np.zeros((36, 2))
            for i in range(36):
                traversal[i, :] = aim.bias_n_li(phase[:n] + [i * 10])[n:, :]
            s = np.where(traversal[:, 0] == traversal[:, 0].min())[0][0]
            n += 1
            end = time.perf_counter()
            print('遍历结束。')
            print('第%s级相位、偏心值及相位偏斜角为：%s°; %.8smm; %.8s°' % (n, s * 10, traversal[s, 0], traversal[s, 1]))
            print(f'时间已过 {int((end - start) // 60)} 分 {(end - start) % 60:.8f} 秒')  # f-Strings方式更快速
            # print('时间已过 {} 分 {:.8f} 秒'.format(int((end - start) // 60), (end - start) % 60))
        else:                         # 否则继续遗传算法找最优
            myAlgorithm, obj_trace, var_trace, best_gen, best_ObjV, phase, res, n = main(aim, n, Dim, phase[:n])
        # 改成以上格式，当只剩一级时，遍历更省时
        # myAlgorithm, obj_trace, var_trace, best_gen, best_ObjV, phase, res, n = main(aim, n, Dim, phase[:n])
    print('搜索完毕！')


