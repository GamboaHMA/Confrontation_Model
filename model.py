import sqlite3
import random
import copy
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import probando_regresion

class Object:
    def __init__(self):
        pass

def Results(style_category):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = f'SELECT * FROM {style_category}'
    #cursor.execute(query)
    athletes = cursor.fetchall()
    query = f'SELECT * FROM clashes_{style_category}'  #aqui construimos clashes_mgr_60g
    cursor.execute(query)
    clashes = cursor.fetchall()

    matrix = probando_regresion.GetMatrixVersusPlayers(clashes, athletes)  #matriz de probabilidades

    iterations = 1000
    medallero = [[0,0,0,0] for i in range(len(athletes))]

    for i in range(iterations):
        athletes = DistCuadrosEnfrentamientos(athletes)

        enfrentamientos = []

        athletes_2a2 = Get_2a2(athletes)
        octavos, winners = Enfrenta(athletes_2a2, enfrentamientos, matrix)
        athletes_2a2 = Get_2a2(winners)
        cuartos, winners = Enfrenta(athletes_2a2, enfrentamientos, matrix)
        athletes_2a2 = Get_2a2(winners)
        semi, winners = Enfrenta(athletes_2a2, enfrentamientos, matrix)
        athletes_2a2 = Get_2a2(winners)
        oro, plata = Enfrenta(athletes_2a2, enfrentamientos, matrix)
        bronce = Repechaje(enfrentamientos, oro, plata, semi, matrix)        

        RellenarMedallero(athletes, bronce, plata, oro, medallero)
    print(medallero)


def Get_2a2(athletes):
    athletes_2a2 = []
    athletes_copy = copy.deepcopy(athletes)

    while len(athletes_copy) != 0:
        if len(athletes_copy) == 1:
            athletes_2a2.append((athletes_copy[0], None))
            athletes_copy.remove(athletes_copy[0])
        else:           
            athletes_2a2.append((athletes_copy[0], athletes_copy[1]))
            athletes_copy.remove(athletes_copy[0])
            athletes_copy.remove(athletes_copy[0])    

    return athletes_2a2 
    

def Enfrenta(atls_2a2, enfrentamientos, matrix):
    result_lossers = []
    winners = []
    impar = False

    for par_atl in atls_2a2:
        atl_1 = par_atl[0]
        atl_2 = par_atl[1]
        if atl_2 == None:
            impar = True
            continue

        if len(matrix[atl_1[0] - 1][atl_2[0] - 1]) != 0:
            atl_1_points = matrix[atl_1[0] - 1][atl_2[0] - 1][1]    #atl1_0 es el id del atleta 1, la matriz en i,j [1] es la cantidad de puntos
            atl_2_points = matrix[atl_2[0] - 1][atl_1[0] - 1][1]
            total = atl_1_points + atl_2_points
            porcentaje_atl1 = atl_1_points/total
        else:
            atl_1_rank = int(atl_1[6])
            atl_2_rank = int(atl_2[6])
            total_rank = atl_1_rank + atl_2_rank
            porcentaje_atl1 = 1 - (atl_1_rank / total_rank)

        r = random.random()
        if r < porcentaje_atl1:
            winners.append(atl_1)
            result_lossers.append(atl_2)
            enfrentamientos.append((atl_1, atl_2, atl_1))
        else:
            winners.append(atl_2)
            result_lossers.append(atl_1)
            enfrentamientos.append((atl_1, atl_2, atl_2))

    if impar:
        atl_2 = winners[len(winners) - 1]
        winners.remove(atl_2)

        if len(matrix[atl_1[0] - 1][atl_2[0] - 1]) != 0:
            atl_1_points = matrix[atl_1[0] - 1][atl_2[0] - 1][1]    #atl1_0 es el id del atleta 1, la matriz en i,j [1] es la cantidad de puntos
            atl_2_points = matrix[atl_2[0] - 1][atl_1[0] - 1][1]
            total = atl_1_points + atl_2_points
            porcentaje_atl1 = atl_1_points/total
        else:
            atl_1_rank = atl_1[6]
            atl_2_rank = atl_2[6]
            total_rank = atl_1_rank + atl_2_rank
            porcentaje_atl1 = 1 - (atl_1_rank / total_rank)

        r = random.random()
        if r < porcentaje_atl1:
            winners.append(atl_1)
            result_lossers.append(atl_2)
            enfrentamientos.append((atl_1, atl_2, atl_1))
        else:
            winners.append(atl_2)
            result_lossers.append(atl_1)
            enfrentamientos.append((atl_1, atl_2, atl_2))

    return result_lossers, winners

def Enfrenta1_1(a_1, a_2, a1_vs_a2):
    
    loss_expect = []      #probabilidad de que un atleta pierda
    for enfrent in a1_vs_a2:
        cat_result = GetCatRes(enfrent.result)
        if (enfrent.winner == a_1.id):
            loss_expect.append()

    return loss_expect   #pendiente de calcular

def GetCatRes(result):
    pass

def GetRegresionFunction(cursor):
    athletes = cursor.execute('''SELECT * FROM athletes''')
    cursor.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
    tablas = cursor.fetchall()

    styles = Object()
    styles.mfs = []
    styles.mgr = []
    styles.wfs = []

    for tabla in tablas:
        if ('mfs_c' in tabla):        #c de clashes
            styles.mfs.append(tabla)
        elif ('mgr_c' in tabla):
            styles.mgr.append(tabla)
        elif ('wfs_c' in tabla):
            styles.wfs.append(tabla)
        
def DistCuadrosEnfrentamientos(athletes):       #arreglar al final
    #query = f'SELECT * FROM {style_category} ORDER BY ranking'
    #cursor.execute(query)
    #athletes = cursor.fetchall()
    athletes_ = copy.deepcopy(athletes)
    result = [0 for _ in range(len(athletes_))]
    result_mask = [False for _ in range(len(athletes_))]

    firstes = [athletes_[i] for i in range(4)]    #seleccionamos los primeros 4 del rankin para distribuirlos en cuadros diferentes
    random.shuffle(firstes)
    for i in range(4):
        result[i*4] = firstes[i]
        athletes_.remove(firstes[i])
        result_mask[i*4] = True
    
    indexs_restantes = []
    for index, element in enumerate(result):
        if result_mask[index]:
            continue
        else:
            indexs_restantes.append(index)
    
    random.shuffle(indexs_restantes)
    for i in range(len(indexs_restantes)):
        result[indexs_restantes[i]] = athletes_[i]

    return result

def Repechaje(enfrentamientos, oro, plata, semi, matrix):
    lossers_by_campeon = []
    lossers_by_subcampeon = []
    not_semifinalist_c = []
    semifinalist_c = []
    not_semifinalist_sc = []
    semifinalist_sc = []

    for enfrentamiento in enfrentamientos:
        if enfrentamiento[0] in oro:
            if enfrentamiento[1] not in plata:
                lossers_by_campeon.append(enfrentamiento[1])
                if enfrentamiento[1] in semi:
                    semifinalist_c.append(enfrentamiento[1])
                else:
                    not_semifinalist_c.append(enfrentamiento[1])
        if enfrentamiento[1] in oro:
            if enfrentamiento[0] not in plata:
                lossers_by_campeon.append(enfrentamiento[0])
                if enfrentamiento[0] in semi:
                    semifinalist_c.append(enfrentamiento[0])
                else:
                    not_semifinalist_c.append(enfrentamiento[0])
        if enfrentamiento[0] in plata:
            if enfrentamiento[1] not in oro:
                lossers_by_subcampeon.append(enfrentamiento[1])
                if enfrentamiento[1] in semi:
                    semifinalist_sc.append(enfrentamiento[1])
                else:
                    not_semifinalist_sc.append(enfrentamiento[1])
        if enfrentamiento[1] in plata:
            if enfrentamiento[0] not in oro:
                lossers_by_subcampeon.append(enfrentamiento[0])
                if enfrentamiento[0] in semi:
                    semifinalist_sc.append(enfrentamiento[0])
                else:
                    not_semifinalist_sc.append(enfrentamiento[0])
    
    atl1_por_bronce = Enfrenta([(not_semifinalist_c[0], not_semifinalist_c[1])], enfrentamientos, matrix)[1]
    bronce1 = Enfrenta([(atl1_por_bronce[0], semifinalist_c[0])], enfrentamientos, matrix)[1]
    
    atl2_por_bronce = Enfrenta([(not_semifinalist_sc[0], not_semifinalist_sc[1])], enfrentamientos, matrix)[1]
    bronce2 = Enfrenta([(atl2_por_bronce[0], semifinalist_sc[0])], enfrentamientos, matrix)[1]

    return (bronce1, bronce2)

def RellenarMedallero(athletes, bronce, plata, oro, medallero):
    for athlete in athletes:
        if athlete in oro:
            medallero[athlete[0] - 1][0] += 1
        elif athlete in plata:
            medallero[athlete[0] - 1][1] += 1
        elif athlete in bronce[0] or athlete in bronce[1]:
            medallero[athlete[0] - 1][2] += 1
        else:
            medallero[athlete[0] - 1][3] += 1
    return

