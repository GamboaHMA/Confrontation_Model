import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import sqlite3
import data
from datetime import datetime
from datetime import date
import statsmodels.api as sm
import copy

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
    mfs = data.Style('mfs')

    mgr = data.Style('mgr')

    wfs = data.Style('wfs')

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

    _data = {
        'vict_1vs2': vict_1vs2,
        'vict_2vs1': vict_2vs1,
        'ptos_1vs2': ptos_1vs2,
        'ptos_2vs1': ptos_2vs1,
        'outcome': outcome
    }

    df = pd.DataFrame(_data)

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

def GetMatrixVersusPlayers(clashes, athletes):
    n = len(athletes)  
    if len(clashes) == 0:
        return None  
    matrix = []
    for i in range(n):
        fila = []
        for j in range(n):
            fila.append([])  #aniadir columna
        matrix.append(fila)

    dicc_2a2_clashes = {} #almacen de enfrentamientos

    min_max = GetMinMaxSMax(clashes)
    min_date = date(2006, 1, 1)
    max_date = min_max[1]
    
    for clash in clashes:

        #clash_date = GetDateMonthYear(clash[8])     #implementar luego ultimo combate
        #if clash_date == max_date:
        #    last_clash = clash
        #    continue

        a1_id = clash[1]     #clash(id, atl1_id, atl2_id, result, winner_id, date)
        a2_id = clash[2]
        
        if ((a1_id, a2_id) not in dicc_2a2_clashes):
            dicc_2a2_clashes[(a1_id, a2_id)] = []
            dicc_2a2_clashes[(a2_id, a1_id)] = []
            dicc_2a2_clashes[(a1_id, a2_id)].append(clash)
            dicc_2a2_clashes[(a2_id, a1_id)].append(clash)
        else:
            dicc_2a2_clashes[(a1_id, a2_id)].append(clash)
            dicc_2a2_clashes[(a2_id, a1_id)].append(clash)

    
    for i in range(1, n):
        for j in range(i + 1, n):
            if (i, j) not in dicc_2a2_clashes.keys():
                continue

            clashes_2a2 = dicc_2a2_clashes[(i, j)]
            if len(clashes_2a2) == 0:
                continue

            data_min_max = GetMinMaxSMax(clashes_2a2)
            data_min = data_min_max[0]
            data_max = data_min_max[1]

            a1_vict = 0
            a2_vict = 0
            a1_regist = 0    #puntos acumulados con respecto al otro atleta
            a2_regist = 0
            last_clash = Object()        #aqui vamos a guardar el outcome de cada par de atletas

            for clash_2a2 in clashes_2a2:
                #clash_date = GetDateMonthYear(clash_2a2[8])
                clash_date = GetDateMonthYear(clash_2a2[5])
                #if clash_date == data_max:
                #    last_clash = clash_2a2
                #    continue

                today = date.today()
                index_ =  ((clash_date.year - min_date.year)*12 + clash_date.month - min_date.month) / ((today.year - min_date.year)*12 + today.month - min_date.month)
                if (clash_2a2[4] == i):
                    a1_vict += 1
                    a1_regist += data.GetPointsByWinE(clash_2a2[3])[0] * index_ * 0.6 #puntos que obtiene al ganar el combate, fecha de combate
                    a2_regist += data.GetPointsByWinE(clash_2a2[3])[1] * index_ * 0.4

                else:
                    a2_vict += 1
                    a2_regist += data.GetPointsByWinE(clash_2a2[3])[1] * index_ * 0.6
                    a1_regist += data.GetPointsByWinE(clash_2a2[3])[0] * index_ * 0.4


            if (a1_regist + a2_regist == 0):
                pass
            else:
                matrix[i-1][j-1].append(a1_vict)
                matrix[i-1][j-1].append(a1_regist/(a1_regist+a2_regist))
            #matrix[i-1][j-1].append(1 if(last_clash[7] == i) else 0)    
            
            if (a1_regist + a2_regist == 0):
                pass
            else:
                matrix[j-1][i-1].append(a2_vict)      
                matrix[j-1][i-1].append(a2_regist/(a1_regist+a2_regist))
            #matrix[j-1][i-1].append(1 if(last_clash[7] == j) else 0) 


    matrix = AthletesInterception(matrix, athletes)   
    
    return matrix  

def AthletesInterception(matrix, athletes):
    n = len(matrix)
    new_matrix = copy.deepcopy(matrix)
    noClashes = [] #pares de atletas que no se han enfrentado nunca

    for i in range(n):
        for j in range(i+1, n):
            if len(matrix[i][j]) == 0:
                noClashes.append((i+1,j+1))

    while(len(noClashes) != 0):         #mientras queden pares de luchadores sin tener una probabilidad
        change = False
        athl1, athl2 = noClashes[0]
        noClashes.remove(noClashes[0])

        athl1_set = {}  #atletas a los que se ha enfrentado athl1 
        athl2_set = {}  #atletas a los que se ha enfrentado athl2
        for i in range(n):
            if i + 1 != athl1:
                if len(matrix[athl1-1][i]) != 0:       #matrix[at-1][i][1] accede al porciento de ganarle at a i(id de athl)
                    p_a1_i = matrix[athl1-1][i][1]
                    athl1_set[i+1] = p_a1_i  #o sea guarda la prob que tiene athl1 de ganarle a i(id de algun atleta) 

        for j in range(n):
            if j + 1 != athl2:
                if len(matrix[athl2-1][j]) != 0:
                    p_a2_j = matrix[athl2-1][j][1]
                    athl2_set[j+1] = p_a2_j   #o sea guarda la prob que tiene athl1 de ganarle a i(id de algun atleta) 

        prob_athl1_athl2 = 0
        prob_athl2_athl1 = 0
        for athl, prob_a1 in athl1_set.items(): #probabilidad que tiene athl1 contra athl
            if athl in athl2_set.keys():
                change = True
                prob_a2 = athl2_set[athl] #prob que tiene athl2 contra atleta athl

                if prob_a1 > 0.5 and prob_a2 > 0.5:    #los dos le ganaron a athl
                    if prob_a1 > prob_a2: 
                        prob_athl1_athl2 += (prob_a1 - prob_a2)*0.6
                        prob_athl2_athl1 += (prob_a1 - prob_a2)*0.4
                    else:
                        prob_athl2_athl1 += (prob_a2 - prob_a1)*0.6
                        prob_athl1_athl2 += (prob_a2 - prob_a1)*0.4
            
                elif prob_a1 > 0.5 and prob_a2 < 0.5:  # a1 le gano a athl y a2 perdio contra athl
                    prob_athl1_athl2 += (prob_a1 - prob_a2)*0.85
                    prob_athl2_athl1 += (prob_a1 - prob_a2)*0.15
            
                elif prob_a1 < 0.5 and prob_a2 < 0.5:  # ambos perdieron contra athl
                    if prob_a1 > prob_a2: 
                        prob_athl1_athl2 += (prob_a1 - prob_a2)*0.4
                        prob_athl2_athl1 += (prob_a1 - prob_a2)*0.6
                    else:
                        prob_athl2_athl1 += (prob_a2 - prob_a1)*0.4
                        prob_athl1_athl2 += (prob_a2 - prob_a1)*0.6
    
        if prob_athl1_athl2 != 0 or prob_athl2_athl1 != 0:  
            new_matrix[athl1-1][athl2-1].append(-1)
            new_matrix[athl1-1][athl2-1].append(prob_athl1_athl2 / (prob_athl1_athl2 + prob_athl2_athl1))
            new_matrix[athl2-1][athl1-1].append(-1)
            new_matrix[athl2-1][athl1-1].append(prob_athl2_athl1 / (prob_athl1_athl2 + prob_athl2_athl1))
        else:
            new_matrix[athl1-1][athl2-1].append(-1)
            atl1_rank = athletes[athl1-1][3]
            atl2_rank = athletes[athl2-1][3]
            #new_matrix[athl1-1][athl2-1].append(atl2_rank/(atl1_rank+atl2_rank))
            new_matrix[athl1-1][athl2-1].append(0.5)
            new_matrix[athl2-1][athl1-1].append(-1)
            #new_matrix[athl2-1][athl1-1].append(atl1_rank/(atl1_rank+atl2_rank))
            new_matrix[athl2-1][athl1-1].append(0.5)
            
        print("ho")           

    return new_matrix


    #if len(noClashes) != 0:
    #    for par in noClashes:
    #        athl1 = par[0]
    #        athl2 = par[1]

    #        matrix[athl1-1][athl2-1].append(0)
    #        matrix[athl1-1][athl2-1].append(0.5)

    #        matrix[athl2-1][athl1-1].append(0)
    #        matrix[athl2-1][athl1-1].append(0.5)

            
            

    






        

def GetDateMonthYear(Date: str):
    month_mapping = {
    'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4,
    'may': 5, 'jun': 6, 'jul': 7, 'ago': 8,
    'sep': 9, 'oct': 10, 'nov': 11, 'dic': 12
    }
    Date = Date.replace('.', '')
    date_ = Date.split(' ')
    #month = month_mapping[date_[0]]
    month = month_mapping[date_[1].lower()]
    #result = date(int(date_[1]), month, 1)
    result = date(int(date_[2]), month, 1)
    return result

def GetMinMaxSMax(clashes): #clash(id, atl1_id, atl2_id, result, winner_id, date)
    min_date = date.max
    max_date = date.min
    for clash in clashes:
        #clash_date = GetDateMonthYear(clash[8])
        clash_date = GetDateMonthYear(clash[5])
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
