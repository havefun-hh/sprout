# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 13:03:18 2020

@author: admin
"""
import numpy as np
from Prediction import Prediction as pre
from Stack_rigidity import Stack_rigidity
import time
from multiprocessing import Pool


"""=================================遍历得到第3,4级装配的36*36个偏心值================================="""
"""=======================================前两级相位为:0,180======================================="""
if __name__ == '__main__':
    ad_part1 = 'G:/190708-190712data/MNJ-HPC-002ZP1-20190709.csv'
    ad_part2 = 'G:/190708-190712data/MNJ-HPT-001ZP1-20190708.csv'
    ad_part3 = 'G:/190708-190712data/MNJ-HPC-001ZP2-20190708.csv'
    # new_part1--part2--part1--part2
    runout = np.stack((-pre.idata(ad_part1, [3]), pre.idata(ad_part1, [1]), pre.idata(ad_part1, [4]), 
                       -pre.idata(ad_part1, [2]), -pre.idata(ad_part2, [4]), pre.idata(ad_part2, [2]), 
                       pre.idata(ad_part2, [3]), pre.idata(ad_part2, [1]), -pre.idata(ad_part3, [3]), 
                       pre.idata(ad_part3, [1]), pre.idata(ad_part3, [4]), pre.idata(ad_part3, [2]), 
                       -pre.idata(ad_part2, [4]), pre.idata(ad_part2, [2]), pre.idata(ad_part2, [3]), 
                       pre.idata(ad_part2, [1])), axis=0)
    r = [84/2, 206.5/2, 80/2, 200/2, 206.5/2, 84/2, 200/2, 80/2, 
         84/2, 206.5/2, 80/2, 200/2, 206.5/2, 84/2, 200/2, 80/2]
    h = [192, 120, 192, 120]
    find_index = 0
    start = time.perf_counter()
    aim = Stack_rigidity(runout, r, h, find_index)
    a = np.zeros((36, 36))
    for i in range(36):
        for j in range(36):
            a[i, j] = max(aim.bias_n(0, 180, i * 10, j * 10)[2:, 0])
    # pool = Pool(4)
    # res = pool.map()
    s = np.where(a.min() == a[:, :])  # s = [[29], [19]]
    end = time.perf_counter()
    print('最小目标值为：%s' % (a[s[0], s[1]]))   # a[s[0], s[1]] = 0.01606076
    print('位置为：%s; %s' % (s[0] * 10, s[1] * 10))
    print(f'耗时：{end - start}s')

