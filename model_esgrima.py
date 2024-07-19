import sqlite3
import random
import copy
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import probando_regresion
import json

class Object:
    def __init__(self):
        pass

def Results(table):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = f'SELECT * FROM {table}'
    cursor.execute(query)
    athletes = cursor.fetchall()   #atletas

    query = f'SELECT * FROM {table}_clashes'
    cursor.execute(query)
    clashes = cursor.fetchall()   #enfrentamientos
    
    matrix = probando_regresion.GetMatrixVersusPlayers(clashes, athletes)

    iterations = 10000
    medallero = [[0,0,0,0,0,0,0,0,0] for i in range(len(athletes))]

    athletes_ = copy.deepcopy(athletes)
    athletes_ordered = OrdenarPorRanking(athletes_)

    #Etapa1 Pools: repartir en 6 grupos equilibradamente para hacer los enfrentamientos de pools
    groups = DistribuirFasPool(athletes_ordered)

    pools_ranking = EnfrentaPools(groups, matrix)
    pools_ranking = OrdenarPools(pools_ranking)

    #Etapa2: Eliminación Directa
    
    
    print('h')



def OrdenarPorRanking(athletes):
    athletes_mask = [False for i in range(len(athletes))]
    athletes_ordered = []
    for i in range(len(athletes)):
        min_rank = float('inf')
        min_athlete = None
        for j in range(len(athletes)):
            athlete_rank = athletes[j][3]
            if athlete_rank < min_rank and not athletes_mask[j]:
                min_rank = athlete_rank
                min_athlete = athletes[j]
                athlete_index = j
        athletes_ordered.append(min_athlete)
        athletes_mask[athlete_index] = True

    return athletes_ordered

def Permuta(group):
    new_group = []

    while(len(group) != 0):
        random_ = random.randint(0, len(group)-1)
        new_group.append(group[random_])
        group.remove(group[random_])
    
    return new_group

def DistribuirFasPool(athletes):          #pendiente a revisar pendiente en caso de que haya mas de 36 atletas
    groups = [[],[],[],[],[],[]]

    grupo_a_aniadir = []
    for i in range(6):
        grupo_a_aniadir.append(athletes[i])  #agrupamos los 6 primeros del ranking
    
    grupo_permutado = Permuta(grupo_a_aniadir)
    for i in range(len(grupo_permutado)):
        groups[i].append(grupo_permutado[i])

    grupo_a_aniadir = []
    for i in range(6, 12):
        grupo_a_aniadir.append(athletes[i])  #agrupamos del 7 al 12 del ranking

    grupo_permutado = Permuta(grupo_a_aniadir)
    for i in range(len(grupo_permutado)):
        groups[i].append(grupo_permutado[i])

    grupo_a_aniadir = []
    for i in range(12, 18):
        grupo_a_aniadir.append(athletes[i])  #agrupamos del 13 al 18 del ranking

    grupo_permutado = Permuta(grupo_a_aniadir)
    for i in range(len(grupo_permutado)):
        groups[i].append(grupo_permutado[i])

    grupo_a_aniadir = []
    for i in range(18, 24):
        grupo_a_aniadir.append(athletes[i])  #agrupamos del 19 al 24 del ranking

    grupo_permutado = Permuta(grupo_a_aniadir)
    for i in range(len(grupo_permutado)):
        groups[i].append(grupo_permutado[i])

    grupo_a_aniadir = []
    for i in range(24,30):
        grupo_a_aniadir.append(athletes[i])  #agrupamos del 25 al 30 del ranking

    grupo_permutado = Permuta(grupo_a_aniadir)
    for i in range(len(grupo_permutado)):
        groups[i].append(grupo_permutado[i])

    athletes_len = len(athletes)
    resto = athletes_len - 30

    grupo_a_aniadir = []
    for i in range(resto):
        grupo_a_aniadir.append(athletes[i+30])
    
    grupo_permutado = Permuta(grupo_a_aniadir)
    for i in range(len(grupo_permutado)):
        groups[i].append(grupo_permutado[i])

    return groups

def EnfrentaPools(groups, matrix): #en matrix esta la probabilidad de los atletas de ganar en los enfrentamientos dos a dos
    result = {}  #(atl, [puntos, diferencia_de_toques])  puntos respecto a la cantidad de victorias y puintos en cuanto a diferencia de toques

    for group in groups:
        for i in range(len(group)):
            for j in range(i+1, len(group)):
                atl1 = group[i]
                atl1_id = atl1[0]

                atl2 = group[j]
                atl2_id = atl2[0]

                prob_vict_atl1_atl2 = matrix[atl1_id-1][atl2_id-1][1]  #obtenemos la prob de vencer atl1 a atl2
                
                clash_result = GetPoints(prob_vict_atl1_atl2, 3)   #(atl1_result, atl2_result, atl1 win? 1 : 0, atl2 win? 1 : 0)
                
                if atl1 in result.keys():             #actualizamos puntos de atl1 en caso de que exista
                    result[atl1][0] += clash_result[0]
                    result[atl1][1] += clash_result[2]
                else:                                    #inicializamos puntos de atl1 en caso de que no exista
                    result[atl1] = []
                    result[atl1].append(clash_result[0])
                    result[atl1].append(clash_result[2])

                if atl2 in result.keys():             #lo mismo hacemos para atleta 2
                    result[atl2][0] += clash_result[1]
                    result[atl2][1] += clash_result[3]
                else:
                    result[atl2] = []
                    result[atl2].append(clash_result[1])
                    result[atl2].append(clash_result[3])



    return result

def OrdenarPools(pools_ranking):
    new_pools = []      #((atleta como en la base de datos), [puntos, victorias en pools])
    #new_pools_mask = [False for i in range(len(pools_ranking))]  #mascara

    for athlete, ptos_victs in pools_ranking.items():  #pasamos el diccionario a una lista
        new_pools.append((athlete, ptos_victs))

    results = []

    while(len(new_pools) != 0):
        max_vict = float('-inf')
        max_dif_puntos = float('-inf')
        for i in range(len(new_pools)):
            atl = new_pools[i][0]
            atl_i_vict = new_pools[i][1][1]
            atl_i_dif_puntos = new_pools[i][1][0]
            if atl_i_vict > max_vict:# and not new_pools_mask[i]:      #si tiene mas victorias
                #max_atl_id = atl_i_id
                max_vict = atl_i_vict
                max_dif_puntos = atl_i_dif_puntos
                max_atl = atl
                max_index = i

            elif atl_i_vict == max_vict:# and not new_pools_mask[i]:
                if atl_i_dif_puntos >= max_dif_puntos:# and not new_pools_mask[i]:
                    #max_atl_id = atl_i_id
                    max_vict = atl_i_vict
                    max_dif_puntos = atl_i_dif_puntos
                    max_atl = atl
                    max_index = i
        
        results.append((max_atl, (max_dif_puntos, max_vict)))
        new_pools.remove(new_pools[max_index])

    return results
 
        


def GetPoints(prob_vict_a1_a2, desv_estandar):
    if desv_estandar == 3:
        random_ = random.random()
        if random_ < prob_vict_a1_a2:
            atl1_points = 5
            atl2_points = 4 - round(3*(prob_vict_a1_a2 - random_))
            return (atl1_points - atl2_points, atl2_points - atl1_points, 1, 0)    
        
        else:
            atl1_points = 4 - round(3*(random_ - prob_vict_a1_a2))
            atl2_points = 5
            return (atl1_points - atl2_points, atl2_points - atl1_points, 0, 1)  #los puntos que se acumulan son los que hacen menos los que le hacen

        
