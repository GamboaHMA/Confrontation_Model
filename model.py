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

def Results(style_category):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = f'SELECT * FROM {style_category}'
    cursor.execute(query)
    athletes = cursor.fetchall()
    query = f'SELECT * FROM {style_category}_clashes'  #aqui construimos clashes_mgr_60g
    cursor.execute(query)
    clashes = cursor.fetchall()

    matrix = probando_regresion.GetMatrixVersusPlayers(clashes, athletes)  #matriz de probabilidades
    for i in range(len(matrix)):    #mijain
        if i == 3:
            continue
        matrix[3][i][1] = 1
        matrix[i][3][1] = 0
    for i in range(len(matrix)):
        if i == 10:
            continue
        matrix[10][i][1] = 0
        matrix[i][10][1] = 1
    for i in range(len(matrix)):
        if i == 1:
            continue
        matrix[1][i][1] = 0
        matrix[i][1][1] = 1

    iterations = 10000
    medallero = [[0,0,0,0,0,0,0,0,0] for i in range(len(athletes))]

    athletes_ = copy.deepcopy(athletes)
    for i in range(iterations):
        athletes_ = DistCuadrosEnfrentamientos(athletes_)

        enfrentamientos = []

        athletes_2a2 = Get_2a2(athletes_)
        octavos, winners = Enfrenta(athletes_2a2, enfrentamientos, matrix)
        athletes_2a2 = Get_2a2(winners)
        cuartos, winners = Enfrenta(athletes_2a2, enfrentamientos, matrix)
        athletes_2a2 = Get_2a2(winners)
        semi, winners = Enfrenta(athletes_2a2, enfrentamientos, matrix)
        athletes_2a2 = Get_2a2(winners)
        plata, oro = Enfrenta(athletes_2a2, enfrentamientos, matrix)

        other_places = Repechaje(athletes, enfrentamientos, oro, plata, semi, matrix)
        bronce = (other_places[0], other_places[1])
        quinto = (other_places[2], other_places[3])
        septimo, octavo, noveno, decimo = other_places[4], other_places[5], other_places[6], other_places[7]
        rest_of_places = other_places[8]

        RellenarMedallero(athletes_, bronce, plata, oro, quinto, septimo, octavo, noveno, decimo, rest_of_places, medallero)
    
    json_ = json.dumps(ReturnJson(athletes, medallero))
    with open(f'{style_category}.json', 'w') as archivo_json:
        archivo_json.write(json_)

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
            porcentaje_atl1 = matrix[atl_1[0]-1][atl_2[0]-1][1]
        else:
            atl_1_rank = int(atl_1[6])
            atl_2_rank = int(atl_2[6])
            total_rank = atl_1_rank + atl_2_rank
            porcentaje_atl1 = 1 - (atl_1_rank / total_rank)

        r = random.random()

        #######
        #if matrix[atl_1[0]-1][atl_2[0]-1][1] == 1:
        #    winners.append(atl_1)
        #    result_lossers.append(atl_2)
        #    enfrentamientos.append((atl_1, atl_2, atl_1))
        #elif matrix[atl_2[0]-1][atl_1[0]-1][1] == 1:
        #    winners.append(atl_2)
        #    result_lossers.append(atl_1)
        #    enfrentamientos.append((atl_1, atl_2, atl_2))
        #elif matrix[atl_1[0]-1][atl_2[0]-1][1] == 0:
        #    winners.append(atl_2)
        #    result_lossers.append(atl_1)
        #    enfrentamientos.append((atl_1, atl_2, atl_2))
        #elif matrix[atl_2[0]-1][atl_1[0]-1][1] == 0:
        #    winners.append(atl_1)
        #    result_lossers.append(atl_2)
        #    enfrentamientos.append((atl_1, atl_2, atl_1))
        #######

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

def Repechaje(athletes, enfrentamientos, oro, plata, semi, matrix):
    lossers_by_campeon = []
    lossers_by_subcampeon = []
    not_semifinalist_c = []
    semifinalist_c = []
    not_semifinalist_sc = []
    semifinalist_sc = []

    athletes_ = copy.deepcopy(athletes)
    toRemoveFromAthletes = []

    for enfrentamiento in enfrentamientos:
        if enfrentamiento[0] in oro:  #fue derrotado por el oro
            if enfrentamiento[1] not in plata:   #no es el plata
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
    
    atl1bronce_atl1_7mo = Enfrenta([(not_semifinalist_c[0], not_semifinalist_c[1])], enfrentamientos, matrix)
    septimo = atl1bronce_atl1_7mo[0]
    quinto1_bronce1 = Enfrenta([(atl1bronce_atl1_7mo[1][0], semifinalist_c[0])], enfrentamientos, matrix)
    quinto1 = quinto1_bronce1[0]
    bronce1 = quinto1_bronce1[1]
    
    atl2bronce_atl2_8vo = Enfrenta([(not_semifinalist_sc[0], not_semifinalist_sc[1])], enfrentamientos, matrix)
    octavo = atl2bronce_atl2_8vo[0]
    quinto2_bronce2 = Enfrenta([(atl2bronce_atl2_8vo[1][0], semifinalist_sc[0])], enfrentamientos, matrix)
    quinto2 = quinto2_bronce2[0]
    bronce2 = quinto2_bronce2[1]

    athletesToRemove = [oro[0], plata[0], bronce1[0], bronce2[0], quinto1[0], quinto2[0], septimo[0], octavo[0]]
    toRemoveFromAthletes.extend(athletesToRemove)

    for athlet in toRemoveFromAthletes:
        for i in range(len(athletes_)):
            if athletes_[i][0] == athlet[0]:
                athletes_.remove(athletes_[i])
                break

    last_places_wins = {}
    last_places_ordered = []
    for i in range(len(athletes_)):
        last_places_wins[athletes_[i][0]] = 0
        for enfrentamiento in enfrentamientos:
            if athletes_[i][0] == enfrentamiento[2][0]:
                last_places_wins[athletes_[i][0]] += 1
        Ubicate(last_places_ordered, athletes_[i], last_places_wins)
    noveno = [last_places_ordered[0]]
    last_places_ordered.remove(last_places_ordered[0])
    decimo = [last_places_ordered[0]]
    last_places_ordered.remove(last_places_ordered[0])

    return (bronce1, bronce2, quinto1, quinto2, septimo, octavo, noveno, decimo, last_places_ordered)  #bronces, quintos lugares y 7mo y 8vo lugares

def Ubicate(list, athlete, last_places_wins):
    ubicado = False
    if len(list) == 0:
        list.append(athlete)
        ubicado = True
    else:
        for i in range(len(list)):
            athlete_id = list[i][0]
            if last_places_wins[athlete_id] > last_places_wins[athlete[0]]:
                continue
            else:
                list.insert(i, athlete)
                ubicado = True
                break
    if not ubicado:
        list.append(athlete)


def RellenarMedallero(athletes, bronce, plata, oro, quinto, septimo, octavo, noveno, decimo, others, medallero):
    for athlete in athletes:
        if athlete in oro:
            medallero[athlete[0] - 1][0] += 1
        elif athlete in plata:
            medallero[athlete[0] - 1][1] += 1
        elif athlete in bronce[0] or athlete in bronce[1]:
            medallero[athlete[0] - 1][2] += 1
        elif athlete in quinto[0] or athlete in quinto[1]:
            medallero[athlete[0] - 1][3] += 1
        elif athlete in septimo:
            medallero[athlete[0] - 1][4] += 1
        elif athlete in octavo:
            medallero[athlete[0] - 1][5] += 1
        elif athlete in noveno:
            medallero[athlete[0] - 1][6] += 1
        elif athlete in decimo:
            medallero[athlete[0] - 1][7] += 1
        else:
            medallero[athlete[0] - 1][8] += 1
    return

def ReturnJson(athletes, medallero):
    medallero_masc = [False for i in range(len(medallero))]

    max = float('-inf')
    first_place = None
    for i in range(len(medallero)):
        if medallero[i][0] > max and not medallero_masc[i]:
            max = medallero[i][0]
            first_place, index = athletes[i], i
    medallero_masc[index] = True
    
    max = float('-inf')
    second_place = None
    for i in range(len(medallero)):
        if medallero[i][1] > max and not medallero_masc[i]:
            max = medallero[i][1]
            second_place, index = athletes[i], i
    medallero_masc[index] = True

    max = float('-inf')
    third_place = None
    for i in range(len(medallero)):
        if medallero[i][2] > max and not medallero_masc[i]:
            max = medallero[i][2]
            third_place, index = athletes[i], i
    medallero_masc[index] = True

    max = float('-inf')
    fourth_place = None
    for i in range(len(medallero)):
        if medallero[i][2] > max and not medallero_masc[i]:
            max = medallero[i][2]
            fourth_place, index = athletes[i], i
    medallero_masc[index] = True

    max = float('-inf')
    fifth_place = None
    for i in range(len(medallero)):
        if medallero[i][3] > max and not medallero_masc[i]:
            max = medallero[i][3]
            fifth_place, index = athletes[i], i
    medallero_masc[index] = True

    max = float('-inf')
    sixth_place = None
    for i in range(len(medallero)):
        if medallero[i][3] > max and not medallero_masc[i]:
            max = medallero[i][3]
            sixth_place, index = athletes[i], i
    medallero_masc[index] = True

    max = float('-inf')
    seventh_place = None
    for i in range(len(medallero)):
        if medallero[i][4] > max and not medallero_masc[i]:
            max = medallero[i][4]
            seventh_place, index = athletes[i], i
    medallero_masc[index] = True

    max = float('-inf')
    eighth_place = None
    for i in range(len(medallero)):
        if medallero[i][5] > max and not medallero_masc[i]:
            max = medallero[i][5]
            eighth_place, index = athletes[i], i
    medallero_masc[index] = True

    datos = {
        "name": "77 kg",
        "name_en": "67 kg",
        "type": "single",
        "sport": "luc",
        "sex": {
            "male": {
                    "date": "2024/08/08",
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