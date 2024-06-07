import pandas as pd
import sqlite3
import names_countries
import my_pyscraper

class obj():   #este objeto se utilizara para explotar la sintaxix de python, ejemplo obj_.name = ""
    pass

class Player:
    def __init__(self, name, country, style, category, age=0):
        self.name = name
        self.country = country
        self.age = age
        self.style = style
        self.category = category
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

def Get_Players_Country(players, style, category):
    info = players.split(',')
    info = [s.replace("'", "").replace("[", "").replace("]", "").replace(" ", "") for s in info]

    result = []

    dentro_de_parentesis = False   #dentro de los parentesis esta el pais del jugador
    player_name = ""
    player_country = ""

    for str_ in info:
        if(str_ != "(" and not dentro_de_parentesis):
            if(str_ == ")"):
                result.append(Player(name=player_name, country=player_country, style=style, category=category))
                player_name = ""
                player_country = ""
            else:
                player_name += str_ + " "
        
        elif (str_ == "("):
            dentro_de_parentesis = True
        else:
            player_country = str_
            dentro_de_parentesis = False
        
    return result

def Get_Wrestling_Athletes():
    index_ = 'index_'

    result = obj()

    men_free_style_categories = ['mfs_57kg','mfs_65kg','mfs_74kg','mfs_86kg','mfs_97kg','mfs_125kg']
    men_greco_roman_categories = ['mgr_60kg','mgr_67kg','mgr_77kg','mgr_87kg','mgr_97kg','mgr_130kg']
    women_free_style_categories = ['wfs_50kg','wfs_53kg','wfs_57kg','wfs_62kg','wfs_68kg','wfs_76kg']

    categories = [['mfs', men_free_style_categories], ['mgr', men_greco_roman_categories], ['wfs', women_free_style_categories]]

    count = 0
    category_index = 0
    category = categories[category_index][1]
    style = categories[category_index][0]
    category_ = category[0]

    for i in range(5, 23):
        if (count == 6):
            count = 0
            category_index += 1
            category = categories[category_index][1]
            style = categories[category_index][0]

        category_ = category[i + 1 - 6*(category_index + 1)][4:]
        index = index_ + str(i)
        players = []
        data = pd.read_csv(f'names_countries/{index}.csv', header=None)
        
        for data_ in data.values:
            players_country = Get_Players_Country(data_[2], style, category_)  #itera por cada fila de la tabla del ccv para obtener el total de atletas de una categoria en especifico
            for player_ in players_country:
                players.append(player_)
                

        setattr(result, category[i + 1 - 6*(category_index + 1)], players)
        count += 1

    return result

def Get_Clashes_From_Web():
    athetes_results_urls = ['https://uww.org/athletes-results/cao-liguo-4364-profile',
                            'https://uww.org/athletes-results/bakhramov-islomjon-2624-profile',
                            'https://uww.org/athletes-results/mohsen-nejad-mehdi-seifollah-143101-profile',
                            'https://uww.org/athletes-results/rodriguez-orozco-raiber-jose-151411-profile',
                            'https://uww.org/athletes-results/de-armas-kevin-5515-profile',
                            'https://uww.org/athletes-results/fergat-abdelkarim-7056-profile',
                            'https://uww.org/athletes-results/mahmoud-haythem-mahmoud-ahmed-fahmy-13978-profile',
                            'https://uww.org/athletes-results/ciobanu-victor-4988-profile',
                            'https://uww.org/athletes-results/basar-enes-2892-profile',
                            'https://uww.org/athletes-results/aidos-sultangali-26264-profile',
                            'https://uww.org/athletes-results/lalaev-sadyk-161871-profile',
                            'https://uww.org/athletes-results/mammadov-murad-14250-profile',
                            'https://uww.org/athletes-results/tibilov-georgij-22706-profile',
                            'https://uww.org/athletes-results/valizadeh-jamal-185324-profile']
    return my_pyscraper.GetAthletesClashes(athetes_results_urls)

#athetes_results_urls = ['https://uww.org/athletes-results/sharshenbekov-zholaman-20714-profile']
#my_pyscraper.GetAthletesClashes(athetes_results_urls)