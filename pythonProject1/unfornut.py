from unconst import *
from math import *
from unforfun import *
import numpy as np

def nut(TDB):
    tc = (TDB - 51544.5) / 36525.0
    Et = rs * (84381.448 - (46.815 + (0.0059 - 0.001813 * tc) * tc) * tc)

    at = rg * (218.31643250 + (481267.8812772222 - (0.00161167 - 0.00000528 * tc) * tc) * tc)
    lt = rg * (134.96298139 + (477198.8673980556 - (0.00869722 - 0.00001778 * tc) * tc) * tc)
    lst = rg * (357.52772333 + (35999.05034 - (0.00016028 - 0.00000333 * tc) * tc) * tc)
    Ft = rg * (93.27191028 + (483202.0175380555 - (0.00368250 - 0.00000306 * tc) * tc) * tc)
    Dt = rg * (297.8536306 + (445267.85036306 - (0.00191417 - 0.00000528 * tc) * tc) * tc)

    dgt = rs * ((-17.1996 - 0.01742 * tc) * sin(at - Ft) + (0.2062 + 0.00002 * tc) * sin(2 * at - 2 * Ft) + 0.0046 * sin(at - 2 * lt + Ft) + 0.0011 * sin(2 * lt - 2 * Ft) - (1.3187 + 0.00016 * tc) * sin(2 * at - 2 * Dt) + (0.1426 - 0.00034 * tc) * sin(lst) - (0.0517 - 0.00012 * tc) * sin(2 * at + lst - 2 * Dt) + (0.0217 - 0.00005 * tc) * sin(2 * at - lst - 2 * Dt) + (0.0129 - 0.00001 * tc) * sin(at + Ft - 2 * Dt) + 0.0048 * sin(2 * lt - 2 * Dt) - 0.0022 * sin(2 * Ft - 2 * Dt))
    det = rs * ((9.2025 + 0.00089 * tc) * cos(at - Ft) - (0.0895 - 0.00005 * tc) * cos(2 * at - 2 * Ft) - 0.0024 * cos(at - 2*lt + Ft) + (0.5736 - 0.00031 * tc) * cos(2 * at - 2 * Dt) + (0.0054 - 0.00001 * tc) * cos(lst) + (0.0224 - 0.00006 * tc) * cos(2 * at + lst - 2 * Dt) - (0.0095 - 0.00003 * tc) * cos(2 * at - lst - 2 * Dt) - 0.0070 * cos(at + Ft - 2 * Dt))

    R = np.dot(matrix_rotate_oz(-dgt),matrix_rotate_ox(Et))
    Nt = np.dot(matrix_rotate_ox(-Et-det), R)

    return Nt, dgt, Et