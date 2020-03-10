# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 12:10:53 2020

@author: admin
"""
import numpy as np
from Prediction import Prediction as pre
from Stack_rigidity import Stack_rigidity
import time
from multiprocessing.pool import Pool


"""===================================================================遍历==============================================================="""
# if __name__ == '__main__':
#     ad_part1 = 'G:/190708-190712data/MNJ-HPC-002ZP1-20190709.csv'
#     ad_part2 = 'G:/190708-190712data/MNJ-HPT-001ZP1-20190708.csv'
#     runout = np.stack((-pre.idata(ad_part1, [3]), pre.idata(ad_part1, [1]), pre.idata(ad_part1, [4]), 
#                         -pre.idata(ad_part1, [2]), -pre.idata(ad_part2, [4]), pre.idata(ad_part2, [2]), 
#                         pre.idata(ad_part2, [3]), pre.idata(ad_part2, [1])), axis=0)
#     r = [84 / 2, 206.5 / 2, 80 / 2, 200 / 2, 206.5 / 2, 84 / 2, 200 / 2, 80 / 2]
#     h = [687, 388]
#     aim = Stack_rigidity(runout, r, h)
#     start = time.perf_counter()
#     a = []
#     for i in range(36):
#         a.append(aim.bias_2(0, i * 10))
#     a = np.array(a)
#     end = time.perf_counter()
#     s = np.where(a[:, 0] == min(a[:, 0]))[0][0]
#     print('最小目标值为：%s' % (a[s, 0]))
#     print('相位为：%s' % (a[s, 1]))
#     print(f'耗时：{end - start}s')

"""=================================================================多进程(1)============================================================="""
# def aimFunc(args):
#     ad_part1 = 'G:/190708-190712data/MNJ-HPC-002ZP1-20190709.csv'
#     ad_part2 = 'G:/190708-190712data/MNJ-HPT-001ZP1-20190708.csv'
#     runout = np.stack((-pre.idata(ad_part1, [3]), pre.idata(ad_part1, [1]), pre.idata(ad_part1, [4]), 
#                         -pre.idata(ad_part1, [2]), -pre.idata(ad_part2, [4]), pre.idata(ad_part2, [2]), 
#                         pre.idata(ad_part2, [3]), pre.idata(ad_part2, [1])), axis=0)
#     r = [84 / 2, 206.5 / 2, 80 / 2, 200 / 2, 206.5 / 2, 84 / 2, 200 / 2, 80 / 2]
#     h = [687, 388]
#     aim = Stack_rigidity(runout, r, h)
#     a = []
#     for i in range(36):
#         a.append(aim.bias_2(0, args[i] * 10))
#     a = np.array(a)
#     return a

# def aimFunc2(args):
#     ad_part1 = 'G:/190708-190712data/MNJ-HPC-002ZP1-20190709.csv'
#     ad_part2 = 'G:/190708-190712data/MNJ-HPT-001ZP1-20190708.csv'
#     runout = np.stack((-pre.idata(ad_part1, [3]), pre.idata(ad_part1, [1]), pre.idata(ad_part1, [4]), 
#                         -pre.idata(ad_part1, [2]), -pre.idata(ad_part2, [4]), pre.idata(ad_part2, [2]), 
#                         pre.idata(ad_part2, [3]), pre.idata(ad_part2, [1])), axis=0)
#     r = [84 / 2, 206.5 / 2, 80 / 2, 200 / 2, 206.5 / 2, 84 / 2, 200 / 2, 80 / 2]
#     h = [687, 388]
#     aim = Stack_rigidity(runout, r, h)
#     a = aim.bias_2(0, args * 10)
#     return a


# if __name__ == '__main__':
#     args = [i for i in range(36)]
#     start = time.perf_counter()
#     pool = Pool(processes=12)
#     a = pool.map(aimFunc2, args)
#     a = np.array(a)
#     # a = aimFunc(args)
#     end = time.perf_counter()
#     s = np.where(a[:, 0] == min(a[:, 0]))[0][0]
#     print('最小目标值为：%s' % (a[s, 0]))
#     print('相位为：%s' % (a[s, 1]))
#     print(f'耗时：{end - start}s')

"""=================================================================多进程(2)============================================================="""
def aimFunc(args):  # 一次传入所有的参数（36行）
    x = args[0]
    aim = args[1]
    a = []
    for i in range(36):
        a.append(aim.bias_2(0, x[i] * 10))
    a = np.array(a)
    return a

def aimFunc2(args):  # 每次传入一行args
    x = args[0]
    aim = args[1]
    a = aim.bias_2(0, x * 10)
    return a


if __name__ == '__main__':
    ad_part1 = 'G:/190708-190712data/MNJ-HPC-002ZP1-20190709.csv'
    ad_part2 = 'G:/190708-190712data/MNJ-HPT-001ZP1-20190708.csv'
    runout = np.stack((-pre.idata(ad_part1, [3]), pre.idata(ad_part1, [1]), pre.idata(ad_part1, [4]), 
                        -pre.idata(ad_part1, [2]), -pre.idata(ad_part2, [4]), pre.idata(ad_part2, [2]), 
                        pre.idata(ad_part2, [3]), pre.idata(ad_part2, [1])), axis=0)
    r = [84 / 2, 206.5 / 2, 80 / 2, 200 / 2, 206.5 / 2, 84 / 2, 200 / 2, 80 / 2]
    h = [687, 388]
    aim = Stack_rigidity(runout, r, h)
    x = [i for i in range(36)]
    start = time.perf_counter()
    """========================================分割线============================================="""
    args = list(zip(x, [aim] * len(x)))   # 返回一个迭代器，每次返回一行数据
    pool = Pool(processes=8)
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


