from unforfun import *
from unconst import *
import numpy as np

def prec(TDB):
    tc = (TDB - 51544.5)/36525.0
    d = rs*(2306.2181+(0.30188+0.017998*tc)*tc)*tc
    s = rs*(2004.3109+(0.42665+0.041833*tc)*tc)*tc
    z = rs*(2306.2181+(1.09468+0.018203*tc)*tc)*tc
    R = np.dot(matrix_rotate_oy(s),matrix_rotate_oz(-d))
    Pt = np.dot(matrix_rotate_oz(-z), R)
    return Pt