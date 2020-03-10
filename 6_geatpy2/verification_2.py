# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 14:36:47 2020

@author: Lenovo
"""
import numpy as np
from Prediction import Prediction as pre
from Stack_rigidity import Stack_rigidity
import time
from multiprocessing import Pool

# if __name__ == '__main__':
#     ad_part1 = 'G:/190708-190712data/MNJ-HPC-002ZP1-20190709.csv'
#     ad_part2 = 'G:/190708-190712data/MNJ-HPT-001ZP1-20190708.csv'
#     ad_part3 = 'G:/190708-190712data/MNJ-HPC-001ZP2-20190708.csv'
#     runout = np.stack((-pre.idata(ad_part1, [3]), pre.idata(ad_part1, [1]), pre.idata(ad_part1, [4]), 
#                        -pre.idata(ad_part1, [2]), -pre.idata(ad_part2, [4]), pre.idata(ad_part2, [2]), 
#                        pre.idata(ad_part2, [3]), pre.idata(ad_part2, [1]), -pre.idata(ad_part3, [3]), 
#                        pre.idata(ad_part3, [1]), pre.idata(ad_part3, [4]), pre.idata(ad_part3, [2])), axis=0)
#     r = [84/2, 206.5/2, 80/2, 200/2, 206.5/2, 84/2, 200/2, 80/2, 
#          84/2, 206.5/2, 80/2, 200/2]
#     start = time.perf_counter()
#     aim = Stack_rigidity(runout, r, [192, 120, 192])
#     a = np.zeros((36, 36))
#     for i in range(36):
#         for j in range(36):
#             a[i, j] = max(aim.bias_n_li([0, i * 10, j * 10])[1:, 0])
#     # pool = Pool(4)
#     # res = pool.map()
#     s = np.where(a.min() == a[:, :])
#     end = time.perf_counter()
#     print('最小目标值为：%s' % (a[s[0], s[1]]))
#     print('相位为：%s' % (a[s, 1]))
#     print(f'耗时：{end - start}s')


"""=================================遍历得到第2,3级装配的36个偏心值================================="""
"""=======================================前两级相位为:0,180======================================="""
if __name__ == '__main__':
    ad_part1 = 'G:/190708-190712data/MNJ-HPC-002ZP1-20190709.csv'
    ad_part2 = 'G:/190708-190712data/MNJ-HPT-001ZP1-20190708.csv'
    ad_part3 = 'G:/190708-190712data/MNJ-HPC-001ZP2-20190708.csv'
    runout = np.stack((-pre.idata(ad_part1, [3]), pre.idata(ad_part1, [1]), pre.idata(ad_part1, [4]), 
                        -pre.idata(ad_part1, [2]), -pre.idata(ad_part2, [4]), pre.idata(ad_part2, [2]), 
                        pre.idata(ad_part2, [3]), pre.idata(ad_part2, [1]), -pre.idata(ad_part3, [3]), 
                        pre.idata(ad_part3, [1]), pre.idata(ad_part3, [4]), pre.idata(ad_part3, [2])), axis=0)
    r = [84/2, 206.5/2, 80/2, 200/2, 206.5/2, 84/2, 200/2, 80/2, 
          84/2, 206.5/2, 80/2, 200/2]
    start = time.perf_counter()
    aim = Stack_rigidity(runout, r, [192, 120, 192])
    a = np.zeros((36, 2))
    for i in range(36):
        a[i, :] = aim.bias_n_li([0, 180, i * 10])[2:, :]
    # pool = Pool(4)
    # res = pool.map()
    s = np.where(a[:, 0] == a[:, 0].min())[0][0]   # 's = 30'
    end = time.perf_counter()
    print('最小目标值为：%s' % (a[s, 0]))     # a[s, 0] = 0.007983456406788495
    print('相位为：%s' % (a[s, 1]))           # a[s, 1] = 77.76590501269096
    print(f'耗时：{end - start}s')

