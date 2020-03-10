# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 20:39:04 2020

@author: admin
"""
import numpy as np
from Prediction import Prediction as pre
from Stack_rigidity import Stack_rigidity
import time
from multiprocessing.pool import Pool



def subAimFunc(args):
    Vars = args[0]     # 每次传入一行Vars值
    aim = args[1]
    n = args[2]
    phase = args[3]
    if phase == None:
        x = [0] + [i * 10 for i in Vars]  # 注意Vars的切片要×10
        a = aim.bias_n_li(x)
        f = max(a[n + 1:, 0])
    else:
        x = phase + [i * 10 for i in Vars]
        a = aim.bias_n_li(x)
        f = max(a[n:, 0])
    return f


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
    n = 0
    phase = None
    aim = Stack_rigidity(runout, r, h)
    Vars = np.random.randint(0, 35, (10, 2))
    # args = list(zip(Vars, [aim] * len(Vars[:, 0]), [n] * len(Vars[:, 0]), [phase] * len(Vars[:, 0])))
    # a = subAimFunc(args[0])
    start = time.perf_counter()
    """========================================分割线============================================="""
    args = list(zip(Vars, [aim] * len(Vars[:, 0]), [n] * len(Vars[:, 0]), [phase] * len(Vars[:, 0])))
    pool = Pool(processes=6)
    res = pool.map(subAimFunc, args)
    """========================================分割线============================================="""
    end = time.perf_counter()
    print(f'耗时：{end - start}s')







