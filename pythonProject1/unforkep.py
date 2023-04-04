from unconst import *
from math import *
from astropy.coordinates import Angle

def vs_from_ecl_to_equ(ta, tb, M0, e, a, W, i, w):
    n_ = 57.2957795130823209 * kgaus / sqrt(a * a * a)
    M = M0 + n_ * (tb - ta)
    M = M * pi/180
    E0 = M - e*sin(M)
    for i in range(0,4):
        E0 = E0 - (E0-e*sin(E0)-M)/(1-e*cos(E0))
    E = E0
    v_sin = (sqrt(1 - e * e) * sin(E)) / (1 - e * cos(E))
    v_cos = (cos(E) - e) / (1 - e * cos(E))
    u_sin = v_sin * cos(w) + v_cos * sin(w)
    u_cos = v_cos * cos(w) - v_sin * sin(w)
    r = a * (1 - e * cos(E))
    p = a * (1 - e * e)
    x = r * (u_cos * cos(W) - u_sin * sin(W) * cos(i))
    y = r * (u_cos * sin(W) + u_sin * cos(W) * cos(i))
    z = r * u_sin * sin(i)
    Vr = kgaus / sqrt(p) * e * v_sin
    Vn = kgaus / sqrt(p) * (1 + e * v_cos)
    xt = x / r * Vr + (-u_sin * cos(W) - u_cos * sin(W) * cos(i)) * Vn
    yt = y / r * Vr + (-u_sin * sin(W) + u_cos * cos(W) * cos(i)) * Vn
    zt = z / r * Vr + u_cos*sin(i)*Vn
    Ea = Angle('23:26:21.448 degrees')
    xequ = x
    yequ = y * cos(Ea.radian) - z * sin(Ea.radian)
    zequ = y * sin(Ea.radian) + z * cos(Ea.radian)
    xtequ = xt
    ytequ = yt * cos(Ea.radian) - zt * sin(Ea.radian)
    ztequ = yt * sin(Ea.radian) + zt * cos(Ea.radian)
    return xequ, yequ, zequ, xtequ, ytequ, ztequ

def vs_from_equ_to_ecl(ta, tb, xequ, yequ, zequ, xtequ, ytequ, ztequ):
    Ea = Angle('23:26:21.448 degrees')
    xecl = xequ
    yecl = yequ * cos(Ea.radian) + zequ * sin(Ea.radian)
    zecl = -yequ * sin(Ea.radian) + zequ * cos(Ea.radian)
    xtecl = xtequ
    ytecl = ytequ * cos(Ea.radian) + ztequ * sin(Ea.radian)
    ztecl = -ytequ * sin(Ea.radian) + ztequ * cos(Ea.radian)
    r = sqrt(xecl**2 + yecl**2 + zecl**2)
    V2 = xtecl**2 + ytecl**2 + ztecl**2
    h = V2 / 2 - kgaus**2 / r
    c1 = yecl * ztecl - zecl * ytecl
    c2 = zecl * xtecl - xecl * ztecl
    c3 = xecl * ytecl - yecl * xtecl
    l1 = -kgaus**2*xecl / r + ytecl * c3 - ztecl * c2
    l2 = -kgaus**2*yecl / r + ztecl * c1 - xtecl * c3
    l3 = -kgaus**2*zecl / r + xtecl * c2 - ytecl * c1
    c = sqrt(c1**2 + c2**2 + c3**2)
    l = sqrt(l1**2 + l2**2 + l3**2)
    a = -kgaus**2/(2*h)
    e = l/kgaus**2
    p = c**2/kgaus**2
    i_cos = c3 / c
    i_sin = sqrt(1 - i_cos**2)
    i = atan(i_sin / i_cos)
    if i < 0:
        i += pi * 2
    else:
        if i > pi * 2:
            i -= pi * 2
    W_sin = c1 / (c * i_sin)
    W_cos = -c2 / (c * i_sin)
    W = atan(W_sin / W_cos)
    if W < 0:
        W += pi
    else:
        if W > pi * 2:
            W -= pi
    w_sin = l3 / (l * i_sin)
    w_cos = (l1 / l) * W_cos + (l2 / l) * W_sin
    w = atan(w_sin / w_cos)
    if w < 0:
        w += pi * 2
    else:
        if w > pi * 2:
            w -= pi * 2
    u_sin = zecl / (r * i_sin)
    u_cos = (xecl / r) * W_cos + (yecl / r) * W_sin
    u = atan(u_sin / u_cos)
    if u < 0:
        u += pi * 2
    else:
        if u > pi * 2:
            u -= pi * 2
    v_sin = u_sin * w_cos - u_cos * w_sin
    v_cos = u_cos * w_cos - u_sin * w_sin
    v = atan(v_sin / v_cos)

    E_sin = (sqrt(1 - e**2) * v_sin) / (1 + e * v_cos)
    E_cos = (v_cos + e) / (1 + e * v_cos)
    E = v + atan((E_sin * v_cos - E_cos * v_sin)/(E_cos * v_cos + E_sin * v_sin))
    M = E - e * E_sin
    n_ = 57.2957795130823209 * kgaus / sqrt(a * a * a)
    M = M*180/pi - n_ * (tb - ta)
    while (M<0):
        M += 360
    return a, e, i, W, w, M



