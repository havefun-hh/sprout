# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 17:00:52 2020

@author: Lenovo
"""
import os
import sys
root_path = os.path.abspath("F:/anaconda/链表反转/剑指offer")
if root_path not in sys.path:
    sys.path.append(root_path)

# from Solution import Node
from Solution import *


Solution = Solution()
l1 = Node(2)
l1.next = Node(3)
l1.next.next = Node(4)
l1.next.next.next = Node(5)
print("反转前：", l1.val, l1.next.val, l1.next.next.val, l1.next.next.next.val)
l = Solution.printListFromTailToHead(l1)
print("反转后：", l)