# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:20:26 2020

@author: Lenovo
"""
import time

class Node(object):
    def __init__(self, x, next=None):
        self.val = x
        self.next = next

def func(head):
    if head == None or head.next ==None:
        return head
    pre = None
    nex = None
    while head:
        nex = head.next
        head.next = pre
        pre = head
        head = nex
    return pre

a = time.perf_counter()
if __name__ == '__main__':
    l = Node(1)
    l.next = Node(2)
    l.next.next = Node(3)
    l.next.next.next = Node(4)
    l.next.next.next.next = Node(5)
    l.next.next.next.next.next = Node(6)
    print("反转前：", l.val, l.next.val, l.next.next.val, l.next.next.next.val, l.next.next.next.next.val, l.next.next.next.next.next.val)
    l1 = func(l)
    print("反转后：", l1.val, l1.next.val, l1.next.next.val, l1.next.next.next.val, l1.next.next.next.next.val, l1.next.next.next.next.next.val)
b = time.perf_counter()
print(f'耗时{b - a}秒')

