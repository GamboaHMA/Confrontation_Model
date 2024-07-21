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
    medallero = [[0,0,0,0,0,0,0,0] for i in range(len(athletes))]

    for i in range(iterations):
        athletes_ = copy.deepcopy(athletes)
        athletes_ordered = OrdenarPorRanking(athletes_)

        #Etapa1 Pools: repartir en 6 grupos equilibradamente para hacer los enfrentamientos de pools
        groups = DistribuirFasPool(athletes_ordered)

        pools_ranking = EnfrentaPools(groups, matrix)
        pools_ranking = OrdenarPools(pools_ranking)

        #Etapa2: Eliminación Directa
        #si hay mas de 32, entonces se hace unos combtes preeliminares 
        preelim_eliminated, preelim_winners = LlevarA32(pools_ranking, matrix)   #cada atleta tiene al lado sus victorias y puntos acumulados en fase de pools

        emparejamiento = EmparejamientoInicial(pools_ranking)
        #Ronda  de 32
        _32_lossers, _32_winners = Rondai(emparejamiento, matrix)
        #Ronda de 16
        _16_lossers, _16_winners = Rondai(emparejamiento, matrix)
        #Ronda de ocatavos
        _8_lossers, _8_winners = Rondai(emparejamiento, matrix)
        #Ronda de cuartos
        _4_lossers, _4_winners = Rondai(emparejamiento, matrix)
        #Final
        plata, oro = Rondai(emparejamiento, matrix)
        #Bronce
        bronce_losser, bronce_winner = Bronce(_4_lossers, matrix)

        ActualizarMedallero(medallero, oro, plata, bronce_losser, bronce_winner, _8_lossers)

    json_ = json.dumps(ReturnJson(athletes, medallero))
    with open(f'{table}.json', 'w') as archivo_json:
        archivo_json.write(json_)

    print(medallero)



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
        try:
            groups[i].append(grupo_permutado[i])
        except:
            groups[i-1].append(grupo_permutado[i])   #en caso de que sean 37, toma el ultimo y lo aniade al ultimo grupo

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

def OrdenarPools(pools_ranking):   #recibe diccionario y devualve lista ordenada
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
        
        results.append((max_atl, [max_dif_puntos, max_vict]))
        new_pools.remove(new_pools[max_index])

    return results
 
        


def GetPoints(prob_vict_a1_a2, desv_estandar):
    if desv_estandar == 3:
        random_ = random.random()
        if random_ < prob_vict_a1_a2:
            atl1_points = 5
            atl2_points = 4 - round(desv_estandar*(prob_vict_a1_a2 - random_))
            return (atl1_points - atl2_points, atl2_points - atl1_points, 1, 0)    
        
        else:
            atl1_points = 4 - round(desv_estandar*(random_ - prob_vict_a1_a2))
            atl2_points = 5
            return (atl1_points - atl2_points, atl2_points - atl1_points, 0, 1)  #los puntos que se acumulan son los que hacen menos los que le hacen

    if desv_estandar == 5:
        random_ = random.random()
        if random_ < prob_vict_a1_a2:
            atl1_points = 15
            atl2_points = 14 - round(desv_estandar*(prob_vict_a1_a2 - random_))
            return (atl1_points - atl2_points, atl2_points - atl1_points, 1, 0)    
        
        else:
            atl1_points = 14 - round(desv_estandar*(random_ - prob_vict_a1_a2))
            atl2_points = 15
            return (atl1_points - atl2_points, atl2_points - atl1_points, 0, 1)  #los puntos que se acumulan son los que hacen menos los que le hacen


def LlevarA32(pools_ranking, matrix):
    len_ = len(pools_ranking)

    if len_ > 32:
        resto = len_ - 32
    else:
        return pools_ranking

    lossers_results = {}

    winners = []
    winners_results = {}

    for i in range(resto):
        atl_1 = pools_ranking[len(pools_ranking) - resto*2 + i][0]    #checked
        atl_1_id = atl_1[0]

        atl_2 = pools_ranking[len(pools_ranking)-1 - i][0]      #checked
        atl_2_id = atl_2[0]

        prob_vict_a1_a2 = matrix[atl_1_id-1][atl_2_id-1][1] #prob de que atl1 le gane a atl2
        clash_result = GetPoints(prob_vict_a1_a2, 5)    #clash(atl1_ptos, atl2_ptos, atl1_win? 1:0, atl2_win? 1:0)

        if clash_result[2] == 1:
            if atl_1 in winners_results:
                winners_results[atl_1][0] += clash_result[0]
                winners_results[atl_1][1] += clash_result[2]
                if atl_2 in lossers_results:
                    lossers_results[atl_2][0] += clash_result[1]
                    lossers_results[atl_2][1] += clash_result[3]
                else:
                    lossers_results[atl_2] = []
                    lossers_results[atl_2].append(clash_result[1])
                    lossers_results[atl_2].append(clash_result[3])
            else:
                winners_results[atl_1] = []
                winners_results[atl_1].append(clash_result[0])
                winners_results[atl_1].append(clash_result[2])
                if atl_2 in lossers_results:
                    lossers_results[atl_2] += clash_result[1]
                    lossers_results[atl_2] += clash_result[3]
                else:
                    lossers_results[atl_2] = []
                    lossers_results[atl_2].append(clash_result[1])
                    lossers_results[atl_2].append(clash_result[3])


        elif clash_result[3] == 1:
            if atl_2 in winners_results:
                winners_results[atl_2][0] += clash_result[1]
                winners_results[atl_2][1] += clash_result[3]
                if atl_1 in lossers_results:
                    lossers_results[atl_1][0] += clash_result[0]
                    lossers_results[atl_1][1] += clash_result[2]
                else:
                    lossers_results[atl_1] = []
                    lossers_results[atl_1].append(clash_result[0])
                    lossers_results[atl_1].append(clash_result[2])
                
            else:
                winners_results[atl_2] = []
                winners_results[atl_2].append(clash_result[1])
                winners_results[atl_2].append(clash_result[3])
                if atl_2 in lossers_results:
                    lossers_results[atl_1] += clash_result[0]
                    lossers_results[atl_1] += clash_result[2]
                else:
                    lossers_results[atl_1] = []
                    lossers_results[atl_1].append(clash_result[0])
                    lossers_results[atl_1].append(clash_result[2])


    winners = OrdenarPools(winners_results)
    lossers = OrdenarPools(lossers_results)

    for losser in lossers:
        for i in range(len(pools_ranking)):
            if pools_ranking[i][0][0] == losser[0][0]:    #si tienen el mismo id de atleta
                pools_ranking.remove(pools_ranking[i])
                break

    return lossers, winners

def Rondai(pools_ranking, matrix):
    len_ = len(pools_ranking)

    winners = []
    lossers = []

    for i in range(int(len_ / 2)):
        atl_1 = pools_ranking[i*2][0]    #checked
        atl_1_id = atl_1[0]

        atl_2 = pools_ranking[i*2+1][0]      #checked
        atl_2_id = atl_2[0]

        prob_vict_a1_a2 = matrix[atl_1_id-1][atl_2_id-1][1] #prob de que atl1 le gane a atl2
        clash_result = GetPoints(prob_vict_a1_a2, 5)    #clash(atl1_ptos, atl2_ptos, atl1_win? 1:0, atl2_win? 1:0)

        if clash_result[2] == 1:
            pools_ranking[i*2][1][0] += clash_result[0]  #1 winner
            pools_ranking[i*2][1][1] += clash_result[2]
            winners.append(pools_ranking[i*2])

            pools_ranking[i*2+1][1][0] += clash_result[1]
            pools_ranking[i*2+1][1][1] += clash_result[3]
            lossers.append(pools_ranking[i*2+1])


        elif clash_result[3] == 1:
            pools_ranking[i*2+1][1][0] += clash_result[1]   #2 winner
            pools_ranking[i*2+1][1][1] += clash_result[3]
            winners.append(pools_ranking[i*2+1])

            pools_ranking[i*2][1][0] += clash_result[0]  
            pools_ranking[i*2][1][1] += clash_result[2]
            lossers.append(pools_ranking[i*2])


    winners = OrdenarPoolsArr(winners)
    lossers = OrdenarPoolsArr(lossers)

    for losser in lossers:
        for i in range(len(pools_ranking)):
            if pools_ranking[i][0][0] == losser[0][0]:    #si tienen el mismo id de atleta
                pools_ranking.remove(pools_ranking[i])
                break

    return lossers, winners

def Bronce(pools_ranking_, matrix):
    pools_ranking = copy.deepcopy(pools_ranking_)
    len_ = len(pools_ranking)

    winners = []
    lossers = []

    for i in range(int(len_ / 2)):
        atl_1 = pools_ranking[i*2][0]    #checked
        atl_1_id = atl_1[0]

        atl_2 = pools_ranking[i*2+1][0]      #checked
        atl_2_id = atl_2[0]

        prob_vict_a1_a2 = matrix[atl_1_id-1][atl_2_id-1][1] #prob de que atl1 le gane a atl2
        clash_result = GetPoints(prob_vict_a1_a2, 5)    #clash(atl1_ptos, atl2_ptos, atl1_win? 1:0, atl2_win? 1:0)

        if clash_result[2] == 1:
            pools_ranking[i*2][1][0] += clash_result[0]  #1 winner
            pools_ranking[i*2][1][1] += clash_result[2]
            winners.append(pools_ranking[i*2])

            pools_ranking[i*2+1][1][0] += clash_result[1]
            pools_ranking[i*2+1][1][1] += clash_result[3]
            lossers.append(pools_ranking[i*2+1])


        elif clash_result[3] == 1:
            pools_ranking[i*2+1][1][0] += clash_result[1]   #2 winner
            pools_ranking[i*2+1][1][1] += clash_result[3]
            winners.append(pools_ranking[i*2+1])

            pools_ranking[i*2][1][0] += clash_result[0]  
            pools_ranking[i*2][1][1] += clash_result[2]
            lossers.append(pools_ranking[i*2])


    winners = OrdenarPoolsArr(winners)
    lossers = OrdenarPoolsArr(lossers)

    for losser in lossers:
        for i in range(len(pools_ranking)):
            if pools_ranking[i][0][0] == losser[0][0]:    #si tienen el mismo id de atleta
                pools_ranking.remove(pools_ranking[i])
                break

    return lossers, winners


def EmparejamientoInicial(pools_ranking_):
    pools_ranking = copy.deepcopy(pools_ranking_)
    len_pools = len(pools_ranking)
    result = []
    if len_pools == 32:
        for i in range(int(len_pools / 2)):
            pools_ranking[i][1][0] = 0
            pools_ranking[i][1][1] = 0
            result.append(pools_ranking[i])

            pools_ranking[len_pools-1 - i][1][0] = 0
            pools_ranking[len_pools-1 - i][1][1] = 0
            result.append(pools_ranking[len_pools -1 - i])

    return result


def OrdenarPoolsArr(pools_ranking):     #list(athlete, [points, victs]) 
    
    new_pools = pools_ranking.copy()     #((atleta como en la base de datos), [puntos, victorias en pools])
    #new_pools_mask = [False for i in range(len(pools_ranking))]  #mascara


    results = []

    while(len(new_pools) != 0):
        max_vict = float('-inf')
        max_dif_puntos = float('-inf')
        for i in range(len(new_pools)):
            atl = new_pools[i][0]
            atl_i_vict = new_pools[i][1][1]
            atl_i_dif_puntos = new_pools[i][1][0]
            if atl_i_vict > max_vict:    #si tiene mas victorias
                max_vict = atl_i_vict
                max_dif_puntos = atl_i_dif_puntos
                max_atl = atl
                max_index = i

            elif atl_i_vict == max_vict:
                if atl_i_dif_puntos >= max_dif_puntos:
                    max_vict = atl_i_vict
                    max_dif_puntos = atl_i_dif_puntos
                    max_atl = atl
                    max_index = i
        
        results.append((max_atl, [max_dif_puntos, max_vict]))
        new_pools.remove(new_pools[max_index])

    return results

def ActualizarMedallero(medallero, oro, plata, bronce_losser, bronce_winner, _8_lossers):
    
    primer_id = oro[0][0][0]
    medallero[primer_id-1][0] += 1

    segundo_id = plata[0][0][0]
    medallero[segundo_id-1][1] += 1

    tercer_id = bronce_winner[0][0][0]
    medallero[tercer_id-1][2] += 1

    cuarto_id = bronce_losser[0][0][0]
    medallero[cuarto_id-1][3] += 1

    quinto_id = _8_lossers[0][0][0]
    medallero[quinto_id-1][4] += 1

    sexto_id = _8_lossers[1][0][0]
    medallero[sexto_id-1][5] += 1

    septimo_id = _8_lossers[2][0][0]
    medallero[septimo_id-1][6] += 1

    octavo_id = _8_lossers[3][0][0]
    medallero[octavo_id-1][7] += 1


def ReturnJson(athletes, medallero):
    athletes_to_organizate = []

    for i in range(len(medallero)):
        sum, index = 0, i   #puntos acumulados para cada atleta

        sum += 5 * medallero[i][0] #medallas de oro
        sum += 3 * medallero[i][1] #medallas de plata
        sum += 2 * medallero[i][2] #medallas de bronce
        sum += 1 * medallero[i][3] #cantidad de veces en 4to lugar
        sum += 0 * medallero[i][4] #cantidad de veces en 5to lugar
        sum += 0 * medallero[i][5] #cantidad de veces en 6to lugar
        sum += -1* medallero[i][6] #cantidad de veces en septimo lugar
        sum += -2* medallero[i][7] #cantidad de veces en octavo lugar

        athletes_to_organizate.append((athletes[i], sum))
    
    athletes_to_organizate = OrganizateAthletes(athletes_to_organizate)

    first_place = athletes_to_organizate[0][0]
    second_place = athletes_to_organizate[1][0]
    third_place = athletes_to_organizate[2][0]
    fourth_place = athletes_to_organizate[3][0]
    fifth_place = athletes_to_organizate[4][0]
    sixth_place = athletes_to_organizate[5][0]
    seventh_place = athletes_to_organizate[6][0]
    eighth_place = athletes_to_organizate[7][0]

    datos = {
        "name": "Espada Individual",
        "name_en": "Individual Epée",
        "type": "single",
        "sport": "esg",
        "sex": {
            "male": {
                    "date": "2024/07/27",
                    "date_pred": None,
                    "finished": False,
                    "previa": [],
                    "analysis": [],
                    "previa_en": [],
                    "analysis_en": [],
                    "prediction": {
                        "1": {
                            "name": f'{first_place[1]}',
                            "name_en": f'{first_place[1]}',
                            "country_domain": f'{first_place[2]}',
                            "status": 0
                        },
                        "2": {
                            "name": f'{second_place[1]}',
                            "name_en": f'{second_place[1]}',
                            "country_domain": f'{second_place[2]}',
                            "status": 0
                        },
                        "3": {
                            "name": f'{third_place[1]}',
                            "name_en": f'{third_place[1]}',
                            "country_domain": f'{third_place[2]}',
                            "status": 0
                        },
                        "4": {
                            "name": f'{fourth_place[1]}',
                            "name_en": f'{fourth_place[1]}',
                            "country_domain": f'{fourth_place[2]}',
                            "status": 0
                        },
                        "5": {
                            "name": f'{fifth_place[1]}',
                            "name_en": f'{fifth_place[1]}',
                            "country_domain": f'{fifth_place[2]}',
                            "status": 0
                        },
                        "6": {
                            "name": f'{sixth_place[1]}',
                            "name_en": f'{sixth_place[1]}',
                            "country_domain": f'{sixth_place[2]}',
                            "status": 0
                        },
                        "7": {
                            "name": f'{seventh_place[1]}',
                            "name_en": f'{seventh_place[1]}',
                            "country_domain": f'{seventh_place[2]}',
                            "status": 0
                        },
                        "8": {
                            "name": f'{eighth_place[1]}',
                            "name_en": f'{eighth_place[1]}',
                            "country_domain": f'{eighth_place[2]}',
                            "status": 0
                        }
                    },
            }
        }
    }

    return datos


def OrganizateAthletes(athletes):
    result = []
    while(len(athletes) != 0):
        max_athlete_sum = float('-inf')
        max_index = 0
        for i in range(len(athletes)):
            athlete_sum = athletes[i][1]
            if athlete_sum > max_athlete_sum:
                max_athlete_sum = athlete_sum
                max_index = i
        result.append(athletes[max_index])
        athletes.remove(athletes[max_index])
    return result