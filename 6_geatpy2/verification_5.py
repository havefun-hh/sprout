# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 16:12:17 2020

@author: admin
"""
import numpy as np
from Prediction import Prediction as pre
from Stack_rigidity import Stack_rigidity, Para
import time
import multiprocessing as mp
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool


"""=================================遍历得到第4,5级装配处的36*36个偏心值================================="""
"""==================================前三级相位为:0,180,280，第6级为190===================================="""
def aimFunc3(args):  # 每次传入一行args
    phase = args[0]
    aim = args[1]
    n = args[2]
    a = max(aim.bias_n_li_fast(phase)[n - 1:,0])
    a = np.squeeze(a) # shape由(1,2)改为(2,),以便后续处理
    return a

if __name__ == '__main__':
    ad_part1 = 'G:/190708-190712data/MNJ-HPC-002ZP1-20190709.csv'
    ad_part2 = 'G:/190708-190712data/MNJ-HPT-001ZP1-20190708.csv'
    ad_part3 = 'G:/190708-190712data/MNJ-HPC-001ZP2-20190708.csv'
    # new_part1--part2--part1--part2--new_part1
    # new_part1--part2--part1--part2--new_part1--part1
    runout = np.stack((-pre.idata(ad_part1, [3]), pre.idata(ad_part1, [1]), pre.idata(ad_part1, [4]), 
                       -pre.idata(ad_part1, [2]), -pre.idata(ad_part2, [4]), pre.idata(ad_part2, [2]), 
                       pre.idata(ad_part2, [3]), pre.idata(ad_part2, [1]), -pre.idata(ad_part3, [3]), 
                       pre.idata(ad_part3, [1]), pre.idata(ad_part3, [4]), pre.idata(ad_part3, [2]), 
                       -pre.idata(ad_part2, [4]), pre.idata(ad_part2, [2]), pre.idata(ad_part2, [3]), 
                       pre.idata(ad_part2, [1]), -pre.idata(ad_part1, [3]), pre.idata(ad_part1, [1]), 
                       pre.idata(ad_part1, [4]), -pre.idata(ad_part1, [2]), -pre.idata(ad_part3, [3]), 
                       pre.idata(ad_part3, [1]), pre.idata(ad_part3, [4]), pre.idata(ad_part3, [2])), axis=0)
    r = [84/2, 206.5/2, 80/2, 200/2, 206.5/2, 84/2, 200/2, 80/2, 
         84/2, 206.5/2, 80/2, 200/2, 206.5/2, 84/2, 200/2, 80/2, 
         84/2, 206.5/2, 80/2, 200/2, 84/2, 206.5/2, 80/2, 200/2]
    h = [192, 120, 192, 120, 192, 192]
    find_index = 0
    Para = Para(runout, r)
    para = Para.getPara()
    aim = Stack_rigidity(runout, r, h, para)
    n = 6
    x = [[0, 180, 280] + [i * 10, j * 10] + [190] for i in range(36) for j in range(36)]
    PoolType = 'Thread'
    start = time.perf_counter()
    """========================================分割线============================================="""
    args = list(zip(x, [aim] * len(x), [n] * len(x)))   # 返回一个迭代器，每次返回一行数据
    if PoolType == 'Thread':
        pool = ThreadPool(12) # 设置线程池的大小
    elif PoolType == 'Process':
        num_cores = int(mp.cpu_count()) # 获得计算机的核心数
        pool = ProcessPool(num_cores) # 设置池的大小
    a0 = pool.map(aimFunc3, args)  # 使用pool.map函数
    a = np.zeros((36, 36))
    for i in range(36):
        a[i, :] = a0[i * 36:(i + 1) * 36]
    # res = pool.map_async(aimFunc2, args)  # 使用pool.map_async函数（需用get函数得到返回值）
    # res.wait()
    # a = np.array(res.get())
    """========================================分割线============================================="""
    end = time.perf_counter()
    s = np.where(a.min() == a[:, :])  # s = [[19], [22]]
    print('最小目标值为：%s' % (a[s[0], s[1]]))   # a[s[0], s[1]] = 0.014390570229967216
    print('位置为：%s; %s' % (s[0] * 10, s[1] * 10))
    print(f'时间已过 {int((end - start) // 60)} 分 {(end - start) % 60:.4f} 秒')


