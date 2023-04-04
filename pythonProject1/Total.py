import math
from datetime import datetime
import numpy as np
from unfordat import *
import astropy
from astropy.time import Time
from unforpnm import *
from unfornut import *
from unforsit import *
from unforkep import *
from datetime import datetime
from dateutil import tz
need_time = datetime(year=2036, month=2, day=29, hour=2, minute=45, second=0, microsecond=0)
import PySimpleGUI as sg
import astropy.units as u


# region заглушка на обновление таблиц IERS
# from astropy.utils.data import clear_download_cache
# clear_download_cache()  # to be sure it is really working
# from astropy.utils import iers
# iers.conf.auto_download = False
# iers.conf.iers_auto_url = None
#endregion


text_days = [i for i in range(1,32)]
text_Months = [i for i in range(1,13)]
text_Years = [i for i in range(2000,2031)]
text_Hours = [i for i in range(0,24)]
text_Minutes = [i for i in range(0,60)]
text_Format = ['UTC', 'MJD', 'TT', 'TDB']
values_old = ''


def Window_Time():

    Pr_Kepler_old = False
    ta = 53000
    tb = 54000
    CheckAU_old = False
    str_time_old = ''
    sg.theme('LightGreen')
    layout1 = [[sg.Text('MoscowTime')], [sg.Combo(values = text_days, default_value=text_days[0], key='_Days_'),
                                        sg.Combo(values = text_Months, default_value=text_Months[0], key='_Months_'),
                                        sg.Combo(values = text_Years, default_value=text_Years[0], key='_Years_'),
                                        sg.Combo(values = text_Hours, default_value=text_Hours[0], key='_Hours_'),
                                        sg.Combo(values = text_Minutes, default_value=text_Minutes[0], key='_Minutes_'),
                                        sg.Input(default_text= '00.000', key='_Seconds_')],
              [sg.Text('Time Format')],
              [sg.Combo(values= text_Format, default_value=text_Format[0], key='_Format_')],
              [sg.Text('Result')],
              [sg.Input(default_text= '', key='_Result_')],
              [sg.Button('OK'), sg.Button('Cancel')],
              [sg.Output(size=(100, 100), key='OUTPUT')]]
    layout2 = [[sg.Text('Типы параметров')],
               [sg.Radio('Кеплер', 1, default = False, key = 'Kepler'),sg.Radio('Декарт', 1, default=True,key = 'Decard'),sg.Checkbox('A.е.',key='CheckAU',default=False)],
               [sg.Text('X  ',key='_Param1_name'), sg.Input(default_text= '-162909241.52551836', key='_Param1_'),sg.Text('км',key='_Param1_mrs')],
               [sg.Text('Y  ',key='_Param2_name'), sg.Input(default_text= '57795390.1914131', key='_Param2_'),sg.Text('км',key='_Param2_mrs')],
               [sg.Text('Z  ',key='_Param3_name'), sg.Input(default_text= '17070106.48718681', key='_Param3_'),sg.Text('км',key='_Param3_mrs')],
               [sg.Text('Vx',key='_Param4_name'), sg.Input(default_text= '-5.038450607729032', key='_Param4_'),sg.Text('км/c',key='_Param4_mrs')],
               [sg.Text('Vy',key='_Param5_name'), sg.Input(default_text= '-31.62091190767173', key='_Param5_'),sg.Text('км/c',key='_Param5_mrs')],
               [sg.Text('Vz',key='_Param6_name'), sg.Input(default_text= '-6.384382042675583', key='_Param6_'),sg.Text('км/c',key='_Param6_mrs')]]
               #[sg.Button('OK'), sg.Button('Cancel')],
               #[sg.Output(size=(100, 100), key='OUTPUT2')]]
    tabs_menu = [
        [sg.TabGroup([[sg.Tab('Времена', layout1),
                             sg.Tab('Вектор состояния', layout2),
                             sg.Tab('Эфемериды', [[]])
                       ]])
                    ]]
    layout = [  [tabs_menu]
        ]

    window = sg.Window('Time',layout,size=(800,600),enable_close_attempted_event=True)

    while True:
        event, values = window.read(timeout = 100)
        str_time = str(values["_Years_"]) + '-' + str(values['_Months_']) + '-' + str(values['_Days_']) + 'T' + str(
            values['_Hours_']) + ':' + str(values['_Minutes_']) + ':' + str(values['_Seconds_'])
        # time_moscow = Time(str_help)
        # time_utc = time_moscow - 3*u.hour

        if  event == sg.WINDOW_CLOSED or event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
            window.Close()
            break

        if not (str_time_old == str_time):
            str_time_old = str_time
            Zone_M = tz.gettz('Europe/Moscow')
            Sec = math.modf(float(values['_Seconds_']))
            Sec_ = int(Sec[1])
            McSec = int(Sec[0] * 1000000)
            Time_Moscow = datetime(int(values["_Years_"]), int(values['_Months_']), int(values['_Days_']),
                               int(values['_Hours_']), int(values['_Minutes_']), Sec_, McSec, Zone_M)
            time_utc_ = Moscow_to_utc(int(values["_Years_"]), int(values['_Months_']), int(values['_Days_']),
                                  int(values['_Hours_']), int(values['_Minutes_']), Sec_, McSec)
            Time_mjd = utc_to_mjd(time_utc_)
            Time_tt, delta = utc_to_tt(time_utc_)
            Time_tdb = utc_to_tdb(time_utc_)

        if values['_Format_'] == "UTC":
            window['_Result_'].Update(time_utc_)
        elif values['_Format_'] == "MJD":
            window['_Result_'].Update(Time_mjd)
        elif values['_Format_'] == "TT":
            window['_Result_'].Update(Time_tt)
        elif values['_Format_'] == "TDB":
            window['_Result_'].Update(Time_tdb)
        else:
            window['_Result_'].Update(Time_Moscow)

        if event == 'OK':
            if values['_Format_'] == "UTC":
                window['_Result_'].Update(time_utc_)
            elif values['_Format_'] == "MJD":
                window['_Result_'].Update(Time_mjd)
            elif values['_Format_'] == "TT":
                window['_Result_'].Update(Time_tt)
            elif values['_Format_'] == "TDB":
                window['_Result_'].Update(Time_tdb)
            else :
                window['_Result_'].Update(Time_Moscow)

            # window['OUTPUT'].print(time_utc_)
            # window['OUTPUT'].print(time_utc)
            #
            # window['OUTPUT'].print(Time_mjd)
            # window['OUTPUT'].print(time_utc.mjd)
            #
            # window['OUTPUT'].print(Time_tt)
            # window['OUTPUT'].print(time_utc.tt.mjd)
            #
            # window['OUTPUT'].print(Time_tdb)
            # window['OUTPUT'].print(time_utc.tdb.mjd)
            file = open('test1.txt', 'w')
            window['OUTPUT'].print('Московское время')
            window['OUTPUT'].print(Time_Moscow)
            file.write('Московское время')
            file.write(str(Time_Moscow))
            window['OUTPUT'].print('Универсальное координированное время (UTC)')
            window['OUTPUT'].print(time_utc_)
            file.write('Универсальное координированное время (UTC)')
            file.write(str(time_utc_))
            window['OUTPUT'].print('Модифицированная юлианская дата (MJD)')
            window['OUTPUT'].print(Time_mjd)
            file.write('Модифицированная юлианская дата (MJD)')
            file.write(str(Time_mjd))
            window['OUTPUT'].print('Барицентрическое динамическое время (TDB)')
            window['OUTPUT'].print(Time_tdb)
            file.write('Барицентрическое динамическое время (TDB)')
            file.write(str(Time_tdb))
            window['OUTPUT'].print('Земное время (TT)')
            window['OUTPUT'].print(Time_tt)
            window['OUTPUT'].print()
            file.write('Земное время (TT)')
            file.write(str(Time_tt))
            file.write(str())
            prec_= prec(Time_tdb)
            window['OUTPUT'].print('Матрица прецессии')
            window['OUTPUT'].print(prec_)
            file.write('Матрица прецессии')
            file.write(str(prec_))
            nut_, dgt, Et = nut(Time_tdb)
            window['OUTPUT'].print("Матрица нутации")
            window['OUTPUT'].print(nut_)
            file.write("Матрица нутации")
            file.write(str(nut_))
            TT, delta = utc_to_tt(time_utc_)
            Smd = sit(Time_mjd, delta)
            Sd = Smd + dgt * cos(Et)
            window['OUTPUT'].print("Гринвическое истинное звёздное время")
            window['OUTPUT'].print(Sd)
            file.write("Гринвическое истинное звёздное время")
            file.write(str(Sd))
            R = matrix_rotate_oz(Sd)
            window['OUTPUT'].print("Матрица вращения Земли")
            window['OUTPUT'].print(R)
            file.write("Матрица вращения Земли")
            file.write(str(R))
            Mnp = np.dot(nut_,prec_)
            window['OUTPUT'].print("Матрица преобразования от небесной СК к истинной экваториальной СК")
            window['OUTPUT'].print(Mnp)
            file.write("Матрица преобразования от небесной СК к истинной экваториальной СК")
            file.write(str(Mnp))
            Mpn = Mnp.transpose()
            window['OUTPUT'].print("Обратная матрица преобразований")
            window['OUTPUT'].print(Mpn)
            file.write("Обратная матрица преобразований")
            file.write(str(Mpn))
            Mct = np.dot(R,Mnp)
            window['OUTPUT'].print("Матрица перехода от небесной к земной СК")
            window['OUTPUT'].print(Mct)
            file.write("Матрица перехода от небесной к земной СК")
            file.write(str(Mct))
            file.close()

        # Переключение на расчет кеплеровких элементов
        if values['Kepler'] == True:
            if Pr_Kepler_old == False:  # перерасчет один раз - по изменению состояния признака
                Pr_Kepler_old = True
                if (bool(values['CheckAU']) == True): # перевод с формы данных в а.е. не нужен
                    k_1 = 1
                    k_2 = 1
                else:
                    k_1 = 1000 / AU
                    k_2 = 1000 * 3600 * 24 / AU
                xequ = float(values['_Param1_']) * k_1
                yequ = float(values['_Param2_']) * k_1
                zequ = float(values['_Param3_']) * k_1
                xtequ = float(values['_Param4_']) * k_2
                ytequ = float(values['_Param5_']) * k_2
                ztequ = float(values['_Param6_']) * k_2
                a, e, i, W, w, M = vs_from_equ_to_ecl(ta, tb, xequ, yequ, zequ, xtequ, ytequ, ztequ)
                window['_Param1_name'].Update('a  ')
                window['_Param2_name'].Update('e  ')
                window['_Param3_name'].Update('i   ' )
                window['_Param4_name'].Update('W ' )
                window['_Param5_name'].Update('w  ' )
                window['_Param6_name'].Update('M0')
                window['_Param1_mrs'].Update('AU  ')
                window['_Param2_mrs'].Update('    ')
                window['_Param3_mrs'].Update('град')
                window['_Param4_mrs'].Update('град')
                window['_Param5_mrs'].Update('град')
                window['_Param6_mrs'].Update('град')
                # перевод в градус для вывода на форму-интерфейса
                i_ = i * 180 / pi
                W_ = W * 180 / pi
                w_ = w * 180 / pi
                window['_Param1_'].Update(a)
                window['_Param2_'].Update(e)
                window['_Param3_'].Update(i_)
                window['_Param4_'].Update(W_)
                window['_Param5_'].Update(w_)
                window['_Param6_'].Update(M)
        # Переключение на расчет декартовых векторов
        if values['Decard'] == True:
            if Pr_Kepler_old == True:
                Pr_Kepler_old = False
                # переход на радианы
                a = float(values['_Param1_'])
                e = float(values['_Param2_'])
                i = float(values['_Param3_']) * pi/180
                W = float(values['_Param4_']) * pi/180
                w = float(values['_Param5_']) * pi/180
                M0 = float(values['_Param6_'])
                xequ, yequ, zequ, xtequ, ytequ, ztequ = vs_from_ecl_to_equ(ta, tb, M0, e, a, W, i, w)
                window['_Param1_name'].Update('X  ')
                window['_Param2_name'].Update('Y  ')
                window['_Param3_name'].Update('Z  ')
                window['_Param4_name'].Update('VX')
                window['_Param5_name'].Update('VY')
                window['_Param6_name'].Update('VZ')

                if (values['CheckAU'] == True): # перевод с формы данных в а.е. не нужен
                    k_1 = 1
                    k_2 = 1
                    window['_Param1_mrs'].Update('AU  ')
                    window['_Param2_mrs'].Update('    ')
                    window['_Param3_mrs'].Update('град')
                    window['_Param4_mrs'].Update('град')
                    window['_Param5_mrs'].Update('град')
                    window['_Param6_mrs'].Update('град')
                else:
                    k_1 = AU / 1000
                    k_2 = AU / 1000 / 3600 / 24
                    window['_Param1_mrs'].Update('км')
                    window['_Param2_mrs'].Update('км')
                    window['_Param3_mrs'].Update('км')
                    window['_Param4_mrs'].Update('км/c')
                    window['_Param5_mrs'].Update('км/c')
                    window['_Param6_mrs'].Update('км/c')

                window['_Param1_'].Update(xequ*k_1)
                window['_Param2_'].Update(yequ*k_1)
                window['_Param3_'].Update(zequ*k_1)
                window['_Param4_'].Update(xtequ*k_2)
                window['_Param5_'].Update(ytequ*k_2)
                window['_Param6_'].Update(ztequ*k_2)

        # Обработка переключателя един. измерения - астмические единицы в км
        if (CheckAU_old != values['CheckAU']):
            CheckAU_old = bool(values['CheckAU'])
            if values['Decard'] == True:
                if CheckAU_old == True:
                    window['_Param1_'].Update(float(values['_Param1_']) / AU * 1000)
                    window['_Param2_'].Update(float(values['_Param2_']) / AU * 1000)
                    window['_Param3_'].Update(float(values['_Param3_']) / AU * 1000)
                    window['_Param4_'].Update(float(values['_Param4_']) / AU * 1000 *3600*24)
                    window['_Param5_'].Update(float(values['_Param5_']) / AU * 1000 *3600*24)
                    window['_Param6_'].Update(float(values['_Param6_']) / AU * 1000 *3600*24)
                    window['_Param1_mrs'].Update('а.е.')
                    window['_Param2_mrs'].Update('а.е.')
                    window['_Param3_mrs'].Update('а.е')
                    window['_Param4_mrs'].Update('а.е/сутки')
                    window['_Param5_mrs'].Update('а.е./cутки')
                    window['_Param6_mrs'].Update('а.е./cутки')
                else:
                    window['_Param1_'].Update(float(values['_Param1_']) * AU / 1000)
                    window['_Param2_'].Update(float(values['_Param2_']) * AU / 1000)
                    window['_Param3_'].Update(float(values['_Param3_']) * AU / 1000)
                    window['_Param4_'].Update(float(values['_Param4_']) * AU / 1000 / 3600 / 24)
                    window['_Param5_'].Update(float(values['_Param5_']) * AU / 1000 / 3600 / 24)
                    window['_Param6_'].Update(float(values['_Param6_']) * AU / 1000 / 3600 / 24)
                    window['_Param1_mrs'].Update('км')
                    window['_Param2_mrs'].Update('км')
                    window['_Param3_mrs'].Update('км')
                    window['_Param4_mrs'].Update('км/c')
                    window['_Param5_mrs'].Update('км/c')
                    window['_Param6_mrs'].Update('км/c')
Window_Time()