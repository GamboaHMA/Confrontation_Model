import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import sqlite3
import data
from datetime import datetime


class Object():
    def __init__(self):
        pass

def PorDefinir():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clashes WHERE clashes.style = 'mgr' AND clashes.category = '60Kg'")
    clashes = cursor.fetchall() #clash(style, category, atl1_name, atl2_name, (atl1_points, atl2_points), atl1_name, winning_form, date)
    

    mfs = Object()
    mfs._57kg = []
    mfs._60kg = []
    mfs._60kg = []
    mfs._60kg = []
    mfs._60kg = []
    mfs._60kg = []

    mgr = Object()
    mgr._60kg = []
    mgr._60kg = []
    mgr._60kg = []
    mgr._60kg = []
    mgr._60kg = []
    mgr._60kg = []

    wfs = Object()
    wfs._50kg = []
    wfs._50kg = []
    wfs._50kg = []
    wfs._50kg = []
    wfs._50kg = []
    wfs._50kg = []

    for clash in clashes:
        if (clash[0] == mfs.__class__.__name__):
            getattr(mfs, clash[1]).append(clash)
        elif(clash[0] == mgr.__class__.__name__):
            getattr(mgr, clash[1]).append(clash)
        else: getattr(wfs, clash[1]).append(clash)

    styles = [mfs, mgr, wfs]



    print(clashes)

def GetMatrixVersusPlayers(clashes):
    matrix = [[[] for _ in range(len(clashes) for _ in range(len(clashes)))]]

    dicc_2a2_clashes = {}

    for clash in clashes:

        min_date = datetime.max
        actual_date = GetDateMonthYear(clash[7])
        if (min_date > actual_date):
            min_date = actual_date
        
        a1_id = clash[2]
        a2_id = clash[3]
        if(a1_id > a2_id):
            id_ = a2_id
            a1_id = a2_id
            a2_id = id_
        
        if ((a1_id, a2_id) not in dicc_2a2_clashes):
            dicc_2a2_clashes[(a1_id, a2_id)] = []
            dicc_2a2_clashes[(a1_id, a2_id)].append(clash)
        else:
            dicc_2a2_clashes.append(clash)

    for i in range(1, len(clashes)):
        for j in range(i, len(clashes)):
            clashes_2a2 = dicc_2a2_clashes[(i, j)]
            a1_vict = 0
            a2_vict = 0
            a1_regist = []
            a2_regist = []

            for clash_2a2 in clash_2a2:
                if (clash_2a2[2] == i):
                    a1_vict += 1
                    a1_regist.append(data.GetPointsByWin(clash_2a2[6][0]), GetDateMonthYear(clash_2a2[7]))  #puntos que obtiene al ganar el combate, fecha de combate
                    a2_regist.append(data.GetPointsByWin(clash_2a2[6][1]), GetDateMonthYear(clash_2a2[7]))

                else:
                    a2_vict += 1
                    a2_regist.append(data.GetPointsByWin(clash_2a2[6][0]), GetDateMonthYear(clash_2a2[7]))  
                    a1_regist.append(data.GetPointsByWin(clash_2a2[6][1]), GetDateMonthYear(clash_2a2[7]))

            matrix[i-1, j-1].append(a1_vict)
            matrix[i-1, j-1].append()      #pendiente
            matrix[j-1, i-1].append(a2_vict)


def GetDateMonthYear(date: str):
    month_mapping = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
    'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
    'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dic': 12
    }

    date_ = date.split(' ')
    month = month[date_[0]]
    result = datetime(date_[1], month, 1)
    return result