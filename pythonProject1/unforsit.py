def sit(MJD, dut):
    tc = MJD + dut/86400
    Tu = (int(tc) - 51544.5)/36525
    r = 6.300388098984891 + (3.707456e-10 - 3.707e-14 * Tu) * Tu
    Sm = 1.753368559233266 + (628.3319706888409 + (6.770714e-6 - 4.51e-10 * Tu) * Tu) * Tu
    Smd = Sm+ r * (tc - int(tc))
    return Smd