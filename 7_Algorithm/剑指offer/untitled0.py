# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 18:40:20 2020

@author: Lenovo
"""
import time

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def twoSum(self, nums, target):
            seen = {}
            res = []
            for i, v in enumerate(nums):
                remaining = target - v
                if remaining in seen:
                    res.append([seen[remaining], i])
                    # return res
                seen[v] = i
            return res
         

    
A = time.perf_counter()
if __name__=='__main__':
    Solution = Solution()
    m = TreeNode(12)
    m.left = TreeNode(5)
    m.right = TreeNode(18)
    m.left.left = TreeNode(2)
    m.left.right = TreeNode(9)
    m.right.left = TreeNode(15)
    m.right.right = TreeNode(19)
    # m.left.left.left = TreeNode(9)
    n = Solution.twoSum([1,3,5,7], 8)
    print(n)
B = time.perf_counter()
print(f'耗时：{B - A}s')








