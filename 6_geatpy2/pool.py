# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 15:11:05 2020

@author: admin
"""
from multiprocessing.pool import Pool
import time


def hhh(i):
    a = time.perf_counter()
    time.sleep(2)
    b = time.perf_counter()
    return i * 2


if __name__ == '__main__':
    pool = Pool(processes=3)
    a = time.perf_counter()
    hh = pool.map(hhh, [1, 2, 3])
    b = time.perf_counter()
    print(f'耗时{b - a}秒')
    print(hh)


# if __name__ == '__main__':
#     a = time.perf_counter()
#     print(hhh(1), hhh(2), hhh(3))
#     b = time.perf_counter()
#     print(f'耗时{b - a}秒')
    