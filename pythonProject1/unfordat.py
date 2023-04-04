from datetime import datetime
from dateutil import tz
from math import *


def Moscow_to_utc(Year, Month, Day, Hour, Minute, Second, McSecond):
    Zone_M = tz.gettz('Europe/Moscow')
    Zone_utc = tz.gettz('UTC')
    Time_M = datetime(Year, Month, Day, Hour, Minute, Second, McSecond, Zone_M)
    Time_utc = Time_M.astimezone(Zone_utc)
    return Time_utc


def utc_to_mjd(Time_utc):
    year = Time_utc.year - 1900
    month = Time_utc.month - 3
    if month < 0:
        month = month + 12
        year = year - 1
    mjd = 15078.0 + 365.0 * year + year // 4 + int(0.5 + 30.6 * month)
    mjd = mjd + Time_utc.day + Time_utc.hour / 24 + Time_utc.minute / 1440 + Time_utc.second / 86400
    return mjd


def utc_to_tt(Time_utc):
    tt_ = Time_utc.year - 2000
    # с 1972 года включительно по 2020 - количество секунд
    dt_sec = [2, 3, 4, 5, 6, 7, 8, 9, 9,
              10, 11, 12, 12, 13, 13, 14, 14, 15, 16,
              16, 17, 18, 19, 20, 20, 21, 22, 22, 22,
              22, 22, 22, 22, 23, 23, 23, 24, 24, 24,
              24, 25, 25, 25, 26, 27, 27, 27, 27, 27]
    if (Time_utc.year >= 1972) and (Time_utc.year <= 2020):
        d_sec = dt_sec[Time_utc.year - 1972]
        dt_sec_ = 32.184 + 10 + d_sec
    elif (Time_utc.year > 2020):
        dt_sec_ = 62.92 + 0.32217 * tt_ + 0.005589 * tt_ ** 2
    TT = utc_to_mjd(Time_utc) + dt_sec_ / 86400
    return TT, dt_sec_


def utc_to_tdb(Time_utc):
    tt, delta = utc_to_tt(Time_utc)
    d = (tt - 51544.5) / 36525.0
    g = 0.017453 * (357.258 + 35999.050 * d)
    TDB = tt + (0.001658 * sin(g + 0.0167 * sin(g))) / 86400
    return TDB
