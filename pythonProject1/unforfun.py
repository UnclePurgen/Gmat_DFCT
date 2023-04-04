#Algoritmy s matricami
import numpy as np
from math import *
def matrix_rotate_ox (alpha):
    R = np.array([[1,0,0],[0,cos(alpha),sin(alpha)],[0,-sin(alpha),cos(alpha)]],dtype=float)
    return R
def matrix_rotate_oy (alpha):
    R = np.array([[cos(alpha),0,-sin(alpha)],[0,1,0],[sin(alpha),0,cos(alpha)]],dtype=float)
    return R
def matrix_rotate_oz (alpha):
    R = np.array([[cos(alpha),sin(alpha),0],[-sin(alpha),cos(alpha),0],[0,0,1]],dtype=float)
    return R