# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 15:28:40 2020

@author: Lenovo
"""
class Node(object):
    def __init__(self, data, next=None):
        self.val = data
        self.next = next

#法一：利用三个指针逐个翻转(原理同法五)
def fun1(head):
    p = head
    q = head.next
    p.next = None
    while q:
        r = q.next
        q.next = p
        p = q
        q = r
    return p 

#法二：尾插法翻转
def fun2(head):
    p = head.next
    while p.next:
        q = p.next
        p.next = q.next
        q.next = head.next
        head.next = q
    
    p.next = head
    head = head.next
    p.next.next = None
    return head

#法三：递归
def fun3(head):
    if head.next == None:
        return head
    new_head = fun3(head.next)
    head.next.next = head
    head.next = None
    return new_head

def fun4(head):
    if head == None:
        return None
    L,M,R = None,None,head
    while R.next != None:
        L = M
        M = R
        R = R.next
        M.next = L
    R.next = M
    return R

#法五：循环反转单链表
def fun5(head):
    if head == None or head.next==None:  # 若链表为空或者仅一个数就直接返回
        return head 
    pre = None
    nex = None
    while(head != None): 
        nex = head.next     # 1
        head.next = pre     # 2
        pre = head      # 3
        head = nex      # 4
    return pre

#测试用例
if __name__ == '__main__':
    l1 = Node(2)
    l1.next = Node(3)
    l1.next.next = Node(4)
    l1.next.next.next = Node(5)
    print("反转前：", l1.val, l1.next.val, l1.next.next.val, l1.next.next.next.val)
    l = fun5(l1)
    print("反转后：", l.val, l.next.val, l.next.next.val, l.next.next.next.val)




        