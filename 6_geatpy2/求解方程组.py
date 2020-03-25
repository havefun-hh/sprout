# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 23:29:51 2020

@author: admin
"""
import sympy as sy
from scipy.optimize import root, fsolve
import numpy as np
x, y, z = sy.symbols("x y z")

eq = [np.sqrt(np.sin(x) ** 2 + (np.cos(x) * np.sin(y)) ** 2) * np.cos(z + np.arctan(np.sin(y) / np.tan(x))) + 4.41648e-05, 
      np.sqrt(np.sin(x) ** 2 + (np.cos(x) * np.sin(y)) ** 2) * np.sin(z + np.arctan(np.sin(y) / np.tan(x))) - 8.21352e-05, 
      np.cos(x) * np.sin(y) - 1]
result = fsolve(eq, [x, y, z])
print(result)
print(sy.latex(result))



def f3(x):
    return np.array([np.sqrt(np.sin(x[0]) ** 2 + (np.cos(x[0]) * np.sin(x[1])) ** 2) * np.cos(x[2] + np.arctan(np.sin(x[1]) / np.tan(x[0]))) + 0.03716232633342362, 
                     np.sqrt(np.sin(x[0]) ** 2 + (np.cos(x[0]) * np.sin(x[1])) ** 2) * np.sin(x[2] + np.arctan(np.sin(x[1]) / np.tan(x[0]))) + 0.047065122646964254, 
                     np.cos(x[0]) * np.sin(x[1]) - 1008.0000380524432])


sol3_root = root(f3,[0.01,0.01,0.01])
sol3_fsolve = fsolve(f3,[0.01,0.01,0.01])
print(sol3_fsolve)

x, y, z = sol3_fsolve
# x, y, z = -1.2781e-06, 1.9938e-06, 0.1000
# x, y, z = -np.pi / 3, np.pi / 6, 0
Rotx = np.array([[1,0,0,0], [0,np.cos(x),-np.sin(x),0], [0,np.sin(x),np.cos(x),0], [0,0,0,1]])
Roty = np.array([[np.cos(y),0,np.sin(y),0], [0,1,0,0], [-np.sin(y),0,np.cos(y),0], [0,0,0,1]])
Rotz = np.array([[np.cos(z),-np.sin(z),0,0], [np.sin(z),np.cos(z),0,0], [0,0,1,0], [0,0,0,1]])
TR = np.dot(np.dot(Rotz, Roty), Rotx)

# Rot = np.array([[np.cos(x) * np.cos(y), np.cos(x) * np.sin(y) * np.sin(z) - np.sin(x) * np.cos(z), np.cos(x) * np.sin(y) * np.cos(z) + np.sin(x) * np.sin(z), 0], 
#                 [np.sin(x) * np.cos(y), np.sin(x) * np.sin(y) * np.sin(z) + np.cos(x) * np.cos(z), np.sin(x) * np.sin(y) * np.cos(z) - np.cos(x) * np.sin(z), 0], 
#                 [-np.sin(y), np.cos(y) * np.sin(z), np.cos(y) * np.cos(z), 0], 
#                 [0, 0, 0, 1]])

e = np.array([0, 0, 1, 1])
b = abs(np.sqrt(np.sin(x) ** 2 + (np.cos(x) * np.sin(y)) ** 2) * np.cos(z + np.arctan(np.sin(y) / np.tan(x))))
a = abs(np.sqrt(np.sin(x) ** 2 + (np.cos(x) * np.sin(y)) ** 2) * np.sin(z + np.arctan(np.sin(y) / np.tan(x))))
c = abs(np.cos(x) * np.sin(y) - 1)
# e1 = np.dot(Rot, e)
e2 = np.dot(TR, e)


# Rot1 = np.array([[np.cos(x) * np.cos(y), np.cos(x) * np.sin(y) * np.sin(z) - np.sin(x) * np.cos(z), np.cos(x) * np.sin(y) * np.cos(z) + np.sin(x) * np.sin(z)], 
#                 [np.sin(x) * np.cos(y), np.sin(x) * np.sin(y) * np.sin(z) + np.cos(x) * np.cos(z), np.sin(x) * np.sin(y) * np.cos(z) - np.cos(x) * np.sin(z)], 
#                 [-np.sin(y), np.cos(y) * np.sin(z), np.cos(y) * np.cos(z)]])
# e_1 = np.array([0, 0, 1])
# e_2 = np.dot(Rot1, e_1)

