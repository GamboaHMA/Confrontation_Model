import pandas as pd
import sqlite3
import names_countries
import my_pyscraper
import temporales.athletes_urls

class obj():   #este objeto se utilizara para explotar la sintaxix de python, ejemplo obj_.name = ""
    pass

class Style:
    def __init__(self, style):
        if style == 'mfs':
            self._57Kg = []
            self._65Kg = []
            self._74Kg = []
            self._86Kg = []
            self._97Kg = []
            self._125Kg = []
        elif style == 'mgr':
            self._60Kg = []
            self._67Kg = []
            self._77Kg = []
            self._87Kg = []
            self._97Kg = []
            self._130Kg = []
        elif style == 'wfs':
            self._50Kg = []
            self._53Kg = []
            self._57Kg = []
            self._62Kg = []
            self._68Kg = []
            self._76Kg = []

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
    athetes_results_urls = temporales.athletes_urls.GetData()
    return my_pyscraper.GetAthletesClashes(athetes_results_urls)

def GetPointsByWin(status):
    points_by_win = {(7, 0): ['VFA', 'VIN', 'VCA', 'VFO', 'DSQ'],  #referencia a https://www.felucha.com/wp-content/uploads/2023/02/2023_FELODA-Reglamento-Luchas-Olimpicas_cambios-en-color.pdf
                     (6, 0): ['VSU'],
                     (6, 1): ['VSU1'],
                     (3, 0): ['VPO'],
                     (3, 1): ['VPO1']}
    
    status_ = status.replace('by ', '')
    for key, value in points_by_win.items():
        if status_ in value:
            return key[0], key[1]
    raise Exception('no se encontró el status de victoria ')

def GetPointsByWinE(result):
    result = result.split('_')
    atl1_res = int(result[0])
    atl2_res = int(result[1])

    return (atl1_res, atl2_res)


#athetes_results_urls = ['https://uww.org/athletes-results/sharshenbekov-zholaman-20714-profile']
#my_pyscraper.GetAthletesClashes(athetes_results_urls)