# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 17:22:25 2020

@author: Lenovo
"""
import numpy as np

# 1.冒泡排序
def bubbleSort(a):
    for i in range(len(a)-1):
        for j in range(len(a)-1-i):
            if a[j+1] < a[j]:
                a[j], a[j+1] = a[j+1], a[j]
    return a

lis = np.array([5, 6, 4, 9, 7, 3, 25, 16, 8])
print(bubbleSort(lis))

# 2.选择排序
def selectionSort_1(a):
    for i in range(len(a)-1):
        for j in range(i+1, len(a)):
            if a[j] < a[i]:
                a[i], a[j] = a[j], a[i]
    return a

def selectionSort_2(a):    # 与第一种方法一样，记录minIndex感觉无用
    for i in range(len(a)-1):
        # 记录最小数的索引
        minIndex = i
        for j in range(i+1, len(a)):
            if a[j] < a[i]:
                a[i], a[j] = a[j], a[i]
        # i 不是最小数时，将 i 和最小数进行交换
        if i != minIndex:
            a[i], a[minIndex] = a[minIndex], a[i]
    return a

lis = np.array([5, 6, 4, 9, 7, 3, 25, 16, 8])
print(selectionSort_2(lis))

# 3.插入排序
def insertionSort(a):
    for i in range(len(a)):
        preIndex = i - 1
        current = a[i]
        while preIndex >= 0 and a[preIndex] > current:
            a[preIndex+1] = a[preIndex]
            preIndex -= 1
        a[preIndex+1] = current
    return a

lis = np.array([5, 6, 4, 9, 7, 3, 25, 16, 8])
print(insertionSort(lis))

# 4.希尔排序
def shellSort(a):
    import math
    gap= 1
    while(gap < len(a)/3):
        gap = gap * 3 + 1
    while gap > 0:
        for i in range(gap, len(a)):
            temp = a[i]
            j = i - gap
            while j>= 0 and a[j] > temp:
                a[j+gap] = a[j]
                j -= gap
            a[j+gap] = temp
        gap = math.floor(gap / 3)
    return

lis = np.array([5, 6, 4, 9, 7, 3, 25, 16, 8])
print(shellSort(lis))




















