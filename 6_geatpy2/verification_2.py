# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 14:36:47 2020

@author: Lenovo
"""
import numpy as np
from Prediction import Prediction as pre
from Stack_rigidity import Stack_rigidity, Para
import time
import multiprocessing as mp
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool


# """=================================遍历得到36*36个偏心值================================="""
# if __name__ == '__main__':
#     ad_part1 = 'G:/190708-190712data/MNJ-HPC-002ZP1-20190709.csv'
#     ad_part2 = 'G:/190708-190712data/MNJ-HPT-001ZP1-20190708.csv'
#     ad_part3 = 'G:/190708-190712data/MNJ-HPC-001ZP2-20190708.csv'
#     runout = np.stack((-pre.idata(ad_part1, [3]), pre.idata(ad_part1, [1]), pre.idata(ad_part1, [4]), 
#                         -pre.idata(ad_part1, [2]), -pre.idata(ad_part2, [4]), pre.idata(ad_part2, [2]), 
#                         pre.idata(ad_part2, [3]), pre.idata(ad_part2, [1]), -pre.idata(ad_part3, [3]), 
#                         pre.idata(ad_part3, [1]), pre.idata(ad_part3, [4]), pre.idata(ad_part3, [2])), axis=0)
#     r = [84/2, 206.5/2, 80/2, 200/2, 206.5/2, 84/2, 200/2, 80/2, 
#           84/2, 206.5/2, 80/2, 200/2]
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


# """=================================遍历得到第2,3级装配的36个偏心值================================="""
# """=======================================前两级相位为:0,180======================================="""
# if __name__ == '__main__':
#     ad_part1 = 'G:/190708-190712data/MNJ-HPC-002ZP1-20190709.csv'
#     ad_part2 = 'G:/190708-190712data/MNJ-HPT-001ZP1-20190708.csv'
#     ad_part3 = 'G:/190708-190712data/MNJ-HPC-001ZP2-20190708.csv'
#     runout = np.stack((-pre.idata(ad_part1, [3]), pre.idata(ad_part1, [1]), pre.idata(ad_part1, [4]), 
#                         -pre.idata(ad_part1, [2]), -pre.idata(ad_part2, [4]), pre.idata(ad_part2, [2]), 
#                         pre.idata(ad_part2, [3]), pre.idata(ad_part2, [1]), -pre.idata(ad_part3, [3]), 
#                         pre.idata(ad_part3, [1]), pre.idata(ad_part3, [4]), pre.idata(ad_part3, [2])), axis=0)
#     r = [84/2, 206.5/2, 80/2, 200/2, 206.5/2, 84/2, 200/2, 80/2, 
#           84/2, 206.5/2, 80/2, 200/2]
#     start = time.perf_counter()
#     Para = Para(runout, r)
#     para = Para.getPara()
#     aim = Stack_rigidity(runout, r, [192, 120, 192], para)
#     a = np.zeros((36, 2))
#     for i in range(36):
#         a[i, :] = aim.bias_n_li_fast([0, 180, i * 10])[2:, :]
#     s = np.where(a[:, 0] == a[:, 0].min())[0][0]   # 's = 30'
#     end = time.perf_counter()
#     print('最小目标值为：%s' % (a[s, 0]))     # a[s, 0] = 0.007983456406788495
#     print('相位为：%s' % (a[s, 1]))           # a[s, 1] = 77.76590501269096
#     print(f'耗时：{end - start}s')

"""=================================================================多进程(2)============================================================="""
# def aimFunc(args):  # 一次传入所有的参数（36行）
#     x = args[0]
#     aim = args[1]
#     a = []
#     for i in range(36):
#         a.append(aim.bias_2(0, x[i] * 10))
#     a = np.array(a)
#     return a


def aimFunc2(args):  # 每次传入一行args
    phase = args[0]
    aim = args[1]
    n = args[2]
    a = max(aim.bias_n_li_fast(phase)[n - 1:, :])
    a = np.squeeze(a) # shape由(1,2)改为(2,),以便后续处理
    return a


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
    h = [192, 120, 192]
    n = 3
    start = time.perf_counter()
    Para = Para(runout, r)
    para = Para.getPara()
    aim = Stack_rigidity(runout, r, h, para)
    phase = [[0, 180] + [i * 10] for i in range(36)]
    PoolType = 'Thread'
    """========================================分割线============================================="""
    args = list(zip(phase, [aim] * len(phase), [n] * len(phase)))   # 返回一个迭代器，每次返回一行数据
    if PoolType == 'Thread':
        pool = ThreadPool(12) # 设置线程池的大小
    elif PoolType == 'Process':
        num_cores = int(mp.cpu_count()) # 获得计算机的核心数
        pool = ProcessPool(num_cores) # 设置池的大小
    # pool = Pool(processes=8)
    a = pool.map(aimFunc2, args)  # 使用pool.map函数
    a = np.array(a)
    # res = pool.map_async(aimFunc2, args)  # 使用pool.map_async函数（需用get函数得到返回值）
    # res.wait()
    # a = np.array(res.get())
    """========================================分割线============================================="""
    # args = list((x, aim))                 # 返回一个list，一次返回所有数据
    # a = aimFunc(args)
    """========================================分割线============================================="""
    end = time.perf_counter()
    s = np.where(a[:, 0] == min(a[:, 0]))[0][0]
    print('最小目标值为：%s' % (a[s, 0]))
    print('相位为：%s' % (a[s, 1]))
    print(f'耗时：{end - start}s')

















