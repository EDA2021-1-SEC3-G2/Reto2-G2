"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """



import sys
import config as cf
import time
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as sel
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quick
assert cf

default_limit = 1000
sys.setrecursionlimit(default_limit*10) 

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos
listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos


def newArrayCatalog():
    catalog = {'videos': None,
               'category': None}
    catalog['videos'] = lt.newList("ARRAY_LIST")
    catalog['category'] = mp.newMap(30, maptype="CHAINING", loadfactor=0.5, comparefunction=comparecategories)

    return catalog


def list_user(cantidad):
    return 4


# Funciones para agregar informacion al catalogo


def addVideo(catalog, video):
    lt.addLast(catalog['videos'], video)


def addCategory(catalog, category):
    c = newCategory(category['id'], category['name'])
    lt.addLast(catalog['category'], c)


# Funciones para creacion de datos
def newCategory(name, id):
    category = {'id': name, 'name': id}
    return category


# Funciones de consulta


def getCategory_ID(catalog, category_name):
    categories = catalog['category']
    for element in range(1, lt.size(categories)+1):
        element_1 = lt.getElement(categories, element)
        if ((element_1["name"]).strip(" ")).lower() == (category_name.strip(" ")).lower():
            return element_1["id"]


def getVideosByCategoryAndCountry(catalog, category_name, country,  numvid):
    videos = catalog['videos']
    templist = lt.newList()
    cat_id = getCategory_ID(catalog, category_name)
    for video in range(1, lt.size(videos)+1):
        element = lt.getElement(videos, video)
        if element["country"].lower() == country.lower() and cat_id == element["category_id"]:
            lt.addLast(templist, element)
    mostviewedbycountandcat_1 = sortVideos(templist, 4)
    return mostviewedbycountandcat_1


def FindTrendVideoByCountry(catalog, country):
    videos_list = catalog['videos']
    reduced_list = lt.newList("ARRAY_LIST")
    for element in range(1, lt.size(videos_list)+1):
        thing = lt.getElement(videos_list, element)
        if ((thing["country"]).strip()).lower() == country.strip().lower():
            lt.addLast(reduced_list, thing)
    print(lt.size(reduced_list))
    sorted_final_list = merg.sort(reduced_list, cmpVideosByVideoID)
    final_element = ""
    days = 0
    contador = 0
    for element in range(1, lt.size(sorted_final_list)+1):
        actual = lt.getElement(sorted_final_list, element)
        pos = element+1
        if actual == lt.lastElement(sorted_final_list) :
            if actual["video_id"] == final_element["video_id"]:
                days += 1
            days += 1
            return final_element, days
        next_one = lt.getElement(sorted_final_list, pos)
        if actual["video_id"] == next_one["video_id"]:
            contador += 1
        else:
            if contador >= days:
                days = contador
                final_element = lt.getElement(sorted_final_list, element)
            contador = 0
    return final_element, days


def FindTrendVideoByCategory(catalog, category_name):
    videos_list = catalog['videos']
    reduced_list = lt.newList("ARRAY_LIST")
    category = getCategory_ID(catalog, category_name)
    for element in range(1, lt.size(videos_list)+1):
        thing = lt.getElement(videos_list, element)
        if thing["category_id"] == category:
            lt.addLast(reduced_list, thing)
    print(lt.size(reduced_list))
    sorted_final_list = merg.sort(reduced_list, cmpVideosByVideoID)
    final_element = ""
    days = 0
    contador = 0
    for element in range(1, lt.size(sorted_final_list)+1):
        actual = lt.getElement(sorted_final_list, element)
        pos = element+1
        if actual == lt.lastElement(sorted_final_list) :
            if actual["video_id"] == final_element["video_id"]:
                days += 1
            days += 1
            
            return final_element, days
        next_one = lt.getElement(sorted_final_list, pos)
        if actual["video_id"] == next_one["video_id"]:
            contador += 1
        else:
            if contador >= days:
                days = contador
                final_element = lt.getElement(sorted_final_list, element)
            contador = 0
    
    return final_element, days


"""def FindTrendVideoByCategory(catalog, category):
    paramater = getCategory_ID(catalog, category)
    for element in catalog["videos"]:
        if element["category_ID"] == catalog["videos"]["category_ID"] and element["category_ID"] != paramater:
            lt.deleteElement(element)
    most = FindTrendiestVideo(catalog)
    return most"""

# Estas funciones no las usé, deben tener similitud con lo que hice pero pues se me facilitó mas partir de 0. Si las quieres implementar igualemnte está bien.
def FindTrendiestVideo(catalog):
    i = 1
    cont = 0
    recount = 0
    temppos = 0
    videoid = lt.getElement(catalog, 1)['video_id']
    while i <= lt.size(catalog):
        if lt.getElement(catalog, i)['video_id'] == videoid:
            cont += 1
        else:
            if cont > recount:
                recount = cont
                temppos = i - 1
                videoid = lt.getElement(catalog, i)
                cont = 1
            else:
                videoid = lt.getElement(catalog, i)
                cont = 1
        i += 1
    result = lt.getElement(catalog, temppos)
    final_result = {'title': result['title'], 'channel_title': result['channel_title'], 'country': result['country'], 'días': recount}
    return final_result


def FindPositionEndTrendingCountry(catalog, country, pos):
    ver = True
    endpos = 0
    i = pos
    print(i)
    while ver:
        if lt.getElement(catalog, i)['country'].lower() != country.lower():
            endpos = i
            ver = False
        i += 1
    sub_size = endpos - pos
    return sub_size


def FindPositionTrendingCountry(catalog, country):
    ver = True
    i = 1
    pos = 0
    while ver:
        if lt.getElement(catalog, i)['country'].lower() == country.lower():
            ver = False
            pos = i
        i += 1
    return pos


def FindMostLikedByTag(catalog, tag, country, elements):    
    videos = catalog["videos"]
    country_list = lt.newList("ARRAY_LIST")
    for element in range(1, lt.size(videos)+1):
        video = lt.getElement(videos, element)
        if video["country"] == country:
            lt.addLast(country_list, video)
    print(lt.size(country_list))
    tag_list = lt.newList("ARRAY_LIST")
    for element in range(1, lt.size(country_list)+1):
        video = lt.getElement(country_list, element)
        yes = video["tags"].split("|")
        for sub_element in yes:
            if sub_element.find(tag) != -1:
                lt.addLast(tag_list, video)
    print(lt.size(tag_list))
    final_list = merg.sort(tag_list, cmpVideosByLikes)
    user_list = lt.newList("ARRAY_LIST")
    lt.addFirst(user_list, lt.firstElement(final_list))
    iterator = 1
    primero = lt.firstElement(final_list)["title"]
    help_list = [primero]                                                                   # esto se hizo por que la operacion de lt.isPresent no funcionó.
    while lt.size(user_list) < int(elements)+1 and iterator != lt.size(final_list):                  # la forma de hacerlo por la otra forma y usando TADlist lo adjunto al final de esta funcion.
        video = lt.getElement(final_list, iterator)
        if video["title"] not in help_list:
            help_list.append(video["title"])
            lt.addLast(user_list, video)
        iterator += 1
    return user_list
    
        


"""while lt.size(user_list)<int(elements)+1 and iterator != lt.size(final_list):
    video = lt.getElement(final_list, iterator)
    if lt.isPresent(user_list, video) != 0:
        iterator += 1
    else:
        lt.addLast(user_list)
        iterator += 1"""

# Funciones utilizadas para comparar elementos dentro de una lista

def comparecategories(name, category):
    return (name == category['name'])


def cmpVideosByViews(video1, video2):
    return(float(video1['views']) > float(video2['views']))


def cmpVideosByCountry(video1, video2):
    return(video1['country'].lower() < video2['country'].lower())


def cmpVideosByVideoID(video1, video2):
    return(video1['video_id'] > video2['video_id'])


def cmpVideosByLikes(video1, video2):
    return (float(video1["likes"]) > float(video2["likes"])) 


# Funciones de ordenamiento


def sortVideos(list_2, alg):
    start_time = time.process_time()
    if alg == 1:
        sorted_list = sa.sort(list_2, cmpVideosByViews)
    elif alg == 2:
        sorted_list = sel.sort(list_2, cmpVideosByViews)
    elif alg == 3:
        sorted_list = ins.sort(list_2, cmpVideosByViews)
    elif alg == 4:
        sorted_list = merg.sort(list_2, cmpVideosByViews)
    else:
        sorted_list = quick.sort(list_2, cmpVideosByViews)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return sorted_list
