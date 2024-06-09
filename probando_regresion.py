import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import sqlite3
import data
from datetime import datetime
from datetime import date
from data import Style
import statsmodels.api as sm

class Object():
    def __init__(self):
        pass

def PorDefinir():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clashes WHERE clashes.style = 'mgr' AND clashes.category = '60Kg'")
    clashes = cursor.fetchall() #clash(style, category, atl1_name, atl2_name, (atl1_points, atl2_points), atl1_name, winning_form, date)
    
    clashes = DeleteDuplicates(clashes)

    map_style = ['mfs', 'mgr', 'wfs']
    mfs = Style('mfs')

    mgr = Style('mgr')

    wfs = Style('wfs')

    for clash in clashes:
        if (clash[1] == 'mfs'):
            getattr(mfs, '_' + clash[2]).append(clash)
        elif(clash[1] == 'mgr'):
            getattr(mgr, '_' + clash[2]).append(clash)
        else: getattr(wfs, '_' + clash[2]).append(clash)

    #aqui vamos a construir los parametros que hay que pasarle al modelo de regresion logistica de sklearn
    #para cada combinacion de 2 (sin repetir pares) guardamos la cantidad de victorias de 1vs2, la cant de vict de 2vs1, la cant de ptos 1vs2 y la cant de pts 2vs1
    vict_1vs2 = []
    vict_2vs1 = []
    ptos_1vs2 = []
    ptos_2vs1 = []
    outcome = []

    styles = [mfs, mgr, wfs]

    for k in range(len(styles)):
        style = styles[k]

        for category in vars(style):
            query_select_ath_style_cat = f'SELECT * FROM {map_style[k] + category}'
            cursor.execute(query_select_ath_style_cat)
            athletes = cursor.fetchall()
            n = len(athletes)

            matrix = GetMatrixVersusPlayers(getattr(style, category), n)
            if matrix != None:
                for i in range(len(matrix)):
                    for j in range(i, len(matrix)):
                        if len(matrix[i][j]) == 0:
                            continue

                        vict_1vs2.append(matrix[i][j][0])
                        vict_2vs1.append(matrix[j][i][0])
                        ptos_1vs2.append(matrix[i][j][1])
                        ptos_2vs1.append(matrix[j][i][1])
                        outcome.append(matrix[i][j][2])

    data = {
        'vict_1vs2': vict_1vs2,
        'vict_2vs1': vict_2vs1,
        'ptos_1vs2': ptos_1vs2,
        'ptos_2vs1': ptos_2vs1,
        'outcome': outcome
    }

    df = pd.DataFrame(data)

    X = df[['vict_1vs2', 'vict_2vs1', 'ptos_1vs2', 'ptos_2vs1']]
    y = df['outcome']

    X = sm.add_constant(X)

    logit_model = sm.Logit(y, X)
    result = logit_model.fit()

    print (result.summary())

    X_train, X_Test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    coef = model.coef_[0]
    intercept = model.intercept_

    #calculando el margen de error


    print(coef)
    print(intercept)

def GetMatrixVersusPlayers(clashes, n):  
    if len(clashes) == 0:
        return None  
    matrix = []
    for i in range(n):
        fila = []
        for j in range(n):
            fila.append([])  #aniadir columna
        matrix.append(fila)

    dicc_2a2_clashes = {}

    min_max = GetMinMaxSMax(clashes)
    min_date = min_max[0]
    max_date = min_max[1]
    
    for clash in clashes:

        clash_date = GetDateMonthYear(clash[8])
        if clash_date == max_date:
            last_clash = clash
            continue

        a1_id = clash[3]
        a2_id = clash[4]
        if(a1_id > a2_id):
            id_ = a1_id
            a1_id = a2_id
            a2_id = id_
        
        if ((a1_id, a2_id) not in dicc_2a2_clashes):
            dicc_2a2_clashes[(a1_id, a2_id)] = []
            dicc_2a2_clashes[(a1_id, a2_id)].append(clash)
        else:
            dicc_2a2_clashes[(a1_id, a2_id)].append(clash)

    
    for i in range(1, n):
        for j in range(i + 1, n):
            if (i, j) not in dicc_2a2_clashes.keys():
                continue

            clashes_2a2 = dicc_2a2_clashes[(i, j)]
            if len(clashes_2a2) == 1:
                continue

            data_min_max = GetMinMaxSMax(clashes_2a2)
            data_min = data_min_max[0]
            data_max = data_min_max[1]

            a1_vict = 0
            a2_vict = 0
            a1_regist = 0    #puntos acumulados con restpecto al otro atleta
            a2_regist = 0
            last_clash = Object()        #aqui vamos a guardar el outcome de cada par de atletas

            for clash_2a2 in clashes_2a2:

                clash_date = GetDateMonthYear(clash_2a2[8])
                if clash_date == data_max:
                    last_clash = clash_2a2
                    continue

                today = date.today()
                index_ =  ((clash_date.year - min_date.year)*12 + clash_date.month - min_date.month) / ((today.year - min_date.year)*12 + today.month - min_date.month)
                if (clash_2a2[3] == i):
                    a1_vict += 1
                    a1_regist += data.GetPointsByWin(clash_2a2[6])[0] * index_  #puntos que obtiene al ganar el combate, fecha de combate
                    a2_regist += data.GetPointsByWin(clash_2a2[6])[1] * index_

                else:
                    a2_vict += 1
                    a2_regist += data.GetPointsByWin(clash_2a2[6])[0] * index_
                    a1_regist += data.GetPointsByWin(clash_2a2[6])[1] * index_


            matrix[i-1][j-1].append(a1_vict)
            matrix[i-1][j-1].append(a1_regist)
            matrix[i-1][j-1].append(1 if(last_clash[7] == i) else 0)    
            
            matrix[j-1][i-1].append(a2_vict)      
            matrix[j-1][i-1].append(a2_regist)
            matrix[j-1][i-1].append(1 if(last_clash[7] == j) else 0)    
    
    return matrix  


def GetDateMonthYear(Date: str):
    month_mapping = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
    'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
    'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }

    date_ = Date.split(' ')
    month = month_mapping[date_[0]]
    result = date(int(date_[1]), month, 1)
    return result

def GetMinMaxSMax(clashes):
    min_date = date.max
    max_date = date.min
    for clash in clashes:
        clash_date = GetDateMonthYear(clash[8])
        if min_date > clash_date:
            min_date = clash_date
        if max_date < clash_date:
            max_date = clash_date

    return (min_date, max_date)

def DeleteDuplicates(clashes):
    result = []
    for clash in clashes:
        if not Pertenece(clash, result):
            result.append(clash)
    return result

def Pertenece(clash, clashes):
    for clash_ in clashes:
        if(clash[1] == clash_[1] and clash[2] == clash_[2] and clash[3] == clash_[3] and clash[4] == clash_[4]
            and clash[5] == clash_[5] and clash[6] == clash_[6] and clash[7] == clash_[7] and clash[8] == clash_[8]):
            return True
    return False

PorDefinir()
