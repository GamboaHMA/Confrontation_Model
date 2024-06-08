import sqlite3
import pandas as pd
import data
import Levenshtein

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

#query = ('''UPDATE mgr_60kg
#               SET name =?
#               WHERE id=?''')
#cursor.execute(query, ('Haythem Mahmoud Ahmed Fahmy MAHMOUD', 9))
#conn.commit()

#cursor.execute('''DROP TABLE IF EXISTS clashes''')

#cursor.execute('''CREATE TABLE IF NOT EXISTS clashes(
#               id INTEGER PRIMARY KEY AUTOINCREMENT,
#               style TEXT,
#               category TEXT,
#               athlete1_id INTEGER NOT NULL,
#               athlete2_id INTEGER NOT NULL,
#               result TEXT,
#               state TEXT,
#               winner_id INTEGER NOT NULL,
#               date TEXT NOT NULL,
#               FOREIGN KEY (athlete1_id) REFERENCES athletes(athlete1_id),
#               FOREIGN KEY (athlete2_id) REFERENCES athletes(athlete2_id),
#               FOREIGN KEY (winner_id) REFERENCES athletes(winner_id)
#)
#''')
#conn.commit()

data_ = data.Get_Clashes_From_Web()
for clash in data_:     #clash(style, category, atl1_name, atl2_name, (atl1_points, atl2_points), atl1_name, winning_form, date)
    
    clashes = []
    style = clash[0]
    category = clash[1]
    atl1_name = clash[2]
    atl2_name = clash[3]
    clash_result = str(clash[4][0]) + '_' + str(clash[4][1])
    state = clash[6]
    date = clash[7]

    category = category.replace(" ","")
    
    if (style == 'gr'):
        style = 'mgr'
    elif(style == 'fs'):
        style = 'mfs'
    else:
        style = 'wfs'
    

    table = style + '_' + category
    query = f'''SELECT id, name FROM {table}'''
    cursor.execute(query)
    names_ids = cursor.fetchall()

    atl1_id = 0
    atl2_id = 0

    for fila in names_ids:
        id, name = fila
        if (Levenshtein.distance(name.lower(), atl1_name.lower()) <= 4):
            atl1_id = int(id)
        if (Levenshtein.distance(name.lower(), atl2_name.lower()) <= 4):
            atl2_id = int(id)

    if (atl1_id == 0 or atl2_id == 0):
        continue

    query_insert_clash = f'''INSERT OR IGNORE INTO clashes(style, category, athlete1_id, athlete2_id, result, state, winner_id, date) VALUES(?,?,?,?,?,?,?,?)'''
    cursor.execute(query_insert_clash, (style, category, atl1_id, atl2_id, clash_result, state, atl1_id, date))


#cursor.execute('''DROP TABLE IF EXISTS athletes''')

#cursor.execute('''CREATE TABLE IF NOT EXISTS athletes(
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#               name TEXT,
#               country TEXT,
#               age INTEGER DEFAULT 0,
#               style TEXT,
#               category TEXT               
#)
#''')



#for table in tables_:
#    table_name = table[0]
#    cursor.execute("PRAGMA table_info({})".format(table_name))
#    columns = cursor.fetchall()
#    print("\nPropiedades de la tabla '{}:'".format(table_name))
#    for column in columns:
#        print("Nombre: {}| Tipo de dato: {}| Clave primaria: {}".format(column[1], column[2], "Sí" if column[5] == 1 else "No"))



#insertando nombre y pais de cada atleta en las tablas de athletas y categorias de peso
#_data = data.Get_Wrestling_Athletes()
#tables = vars(_data)
#for table, values in tables.items():
#    query_create_table = f'''CREATE TABLE IF NOT EXISTS {table}(
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    name TEXT NOT NULL,
#    country TEXT NOT NULL,
#    age INTEGER DEFAULT 0,
#    style TEXT,
#    category TEXT
#    )'''
#    cursor.execute(query_create_table)
#
#    for value in values:
#        query_insert_athlete = f'''INSERT OR IGNORE INTO {table} (name, country, style, category) VALUES (?, ?, ?, ?)'''
#        query_insert_athlet_in_athletes = f'''INSERT OR IGNORE INTO athletes (name, country, style, category) VALUES (?, ?, ?, ?)'''
#        name = value.name
#        country = value.country
#        style = value.style
#        category = value.category
#
#        cursor.execute(query_insert_athlete, (name, country, style, category))
#        cursor.execute(query_insert_athlet_in_athletes, (name, country, style, category))


def GetAthletes(cursor):
    cursor.execute('''SELECT * FROM athletes''')
    athletes = cursor.fetchall()
    return athletes

#conn.close()
print('h')
conn.commit()