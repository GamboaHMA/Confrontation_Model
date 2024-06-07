import sqlite3
import random
import copy
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class Object:
    def __init__(self):
        pass

def Results():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    athletes = cursor.execute('SELECT * FROM athletes')
    random.shuffle(athletes)
    regresion_func = GetRegresionFunction(cursor)
    enfrentamientos = []

    athletes_2a2 = Get_2a2(athletes)
    octavos = Enfrenta(athletes_2a2, enfrentamientos)
    cuartos = Enfrenta(athletes_2a2, enfrentamientos)
    subcampeon = Enfrenta(athletes_2a2, enfrentamientos)
    campeon = Enfrenta(athletes_2a2, enfrentamientos)

    posiciones = [octavos, cuartos, subcampeon, campeon]
    return (posiciones, enfrentamientos)

def Get_2a2(athletes):
    athletes_2a2 = []
    athletes_copy = copy.deepcopy(athletes)
    count = 0

    while (len(athletes_copy) != 0):
        if (len(athletes_copy) == 1):
            athl_1 = athletes_copy[0]
            athletes_2a2.append(athl_1, None)
        else:
            r = random.randint(len(athletes_copy))
            athl_1 = athletes_copy[r]
            athletes_copy.remove(athl_1)
            r = random.randint(len(athletes_copy))
            athl_2 = athletes_copy(r)
            athletes_copy.remove(athl_2)
            athletes_2a2.append((athl_1, athl_2))

    return athletes_2a2 
    

def Enfrenta(athls_2a2, enfrentamientos, cursor):
    result = []

    for par_atl in athls_2a2:
        atl_1 = par_atl[0]
        atl_2 = par_atl[1]
        query = f'''SELECT * FROM clashes WHERE (clashes.athletes == {atl_1.id} AND 
                       clashes.athletes == {atl_2.id}) OR (clashes.athletes == {atl_2} AND 
                       clashes.athletes == {atl_1})'''

        cursor.execute(query)
        
        atl_1_vs_atl_2 = cursor.fetchall()
        losser = Enfrenta1_1(atl_1, atl_2, atl_1_vs_atl_2)
        winner = atl_1 if (losser == atl_2) else atl_2
        enfrentamientos.append([atl_1, atl_2, winner])
        result.append(losser)

    for atl in result:
        athls_2a2.remove(atl)
    
    return result, enfrentamientos

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
        



