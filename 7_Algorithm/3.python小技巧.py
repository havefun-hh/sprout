# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 19:57:18 2020

@author: Lenovo
"""
#1.冒泡排序
def bubbleSort(a):
    for i in range(len(a)-1):
        for j in range(len(a)-1-i):
            if a[j+1] < a[j]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

lis = np.array([5, 6, 4, 9, 7, 3, 25, 16, 8])
print(bubbleSort(lis))

#2.计算x的n次方
def power(x, n):
    s = 1
    while n > 0:
        s *= x
        n -= 1
    return s

print(power(4, 3))

#3.十进制转二进制、八进制、十六进制
dec = int(input("输入数字："))
print("十进制数为：", dec)
print("转换为二进制为：", bin(dec))
print("转换为八进制为：", oct(dec))
print("转换为十六进制为：", hex(dec))

#4.计算阶乘factorial的几种方法
def fac1():
    num = int(input("请输入一个数字："))
    factorial= 1
    #查看数字是负数或0或正数
    if num < 0:
        print("抱歉，负数没有阶乘")
    elif num == 0:
        print("0的阶乘为1")
    else:
        for i in range(1, num+1):
            factorial = factorial * i
        print("%d的阶乘为%d" % (num, factorial))

def fac2(n):
    result = n
    for i in range(1, n):
        result *= i
    return result

def fac3(n):
    if n == 1:
        return 1
    return n * fac2(n-1)

#5.列出当前目录下的所有文件和目录名
[d for d in os.listdir('.')]

#6.生成日历
import calendar
yy = int(input("请输入年份"))
mm = int(input("请输入月份"))
print(calendar.month(yy, mm))

#7.查看python版本
import sys
sys.version_info

#8.使用IPython
%pip install [pkgs]  #在不离开Shell的情况下安装包
%cd                  #修改当前工作路径

#9.检查你的对象占用了多少内存
import sys
mylist = range(0, 10000)
print(sys.getsizeof(mylist))

#10.合并字典
#(1)
dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}
merged = { **dict1, **dict2 }
print(merged)   """{'a': 1, 'b': 3, 'c': 4}如果有重复的key,第一个会被覆盖掉"""
#(2)
dict1.update(dict2)  """同上，重复的会覆盖掉"""

#11.创建进度条
from progress.bar import Bar
bar = Bar('Processing', max=20)
for i in range(20):
    # Do some work
    bar.next()
bar.finish()

#12.将字符串分割成list
mystring = "The quick brown fox"
mylist = mystring.split(' ')
print(mylist)

#13.将字符创列表变成一个字符串
mylist = ['The', 'quick', 'brown', 'fox']
mystring = " ".join(mylist)
print(mystring)

#14.列表展平
#(1)
def flatten(li):
    return [x for y in li for x in y]
flatten([[1, 2, 3, 4], [5, 6, 7, 8]])
#(2)转成numpy数组使用flatten()方法，再转为list
import numpy as np
a = [[1, 2], [3, 4], [5, 6]]
b = np.array(a).flatten().tolist()
print(b)

#15.两个list相加相当于extend
a = [1, 2, 3]
b = [4, 5, 6]
res1 = a + b
a.extend(b)
print(res1, a)























