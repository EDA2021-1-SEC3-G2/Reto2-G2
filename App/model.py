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
    catalog['category'] = mp.newMap(37, maptype="CHAINING", loadfactor=5.0, comparefunction=comparecategoriesmap)
    return catalog


def list_user(cantidad):
    return 4


# Funciones para agregar informacion al catalogo


def addVideo(catalog, video):
    lt.addLast(catalog['videos'], video)


# Se agrega un mapentry
def addCategory(catalog, category):
    if mp.contains(catalog["category"], me.getKey(category)) is False:
        mp.put(catalog["category"], me.getKey(category), me.getValue(category))


# Funciones para creacion de datos, se agerga un mapentry
def newCategory(name, id):
    category = me.newMapEntry(id, name)
    return category


# Funciones de consulta


def getCategory_ID(catalog, category_name):
    categories = catalog['category']
    # Lista de los nombres de categoria
    list1 = mp.valueSet(categories)
    # Variable para el while
    ver = True
    i = 0
    # El while te da la posicion en que estaria el nombre de la categoria (value)
    while ver:
        if category_name.lower() == list1[i]:
            pos = i
            ver = False
        i += 1
    # Esa posicion es la misma que el id de la categoria (key)
    list2 = mp.keySet(categories)
    return list2[pos]


def getVideosByCategoryAndCountry(catalog, category_name, country,  numvid):
    videos = catalog['videos']
    templist = lt.newList()
    cat_id = getCategory_ID(catalog, category_name)
    for video in lt.iterator(videos):
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
            if sub_element.lower().find(tag) != -1:
                lt.addLast(tag_list, video)
    print(lt.size(tag_list))
    final_list = merg.sort(tag_list, cmpVideosByLikes)
    user_list = lt.newList("ARRAY_LIST", comparador_ascendente)
    lt.addFirst(user_list, lt.firstElement(final_list))
    iterator = 1
    while lt.size(user_list) < int(elements)+1 and iterator != lt.size(final_list):
        video = lt.getElement(final_list, iterator)
        if lt.isPresent(user_list, video) == 0:
            lt.addLast(user_list, video)
            iterator += 1
        else:
            iterator += 1
    return user_list



# Funciones utilizadas para comparar elementos dentro de una lista
def comparecategoriesmap(id, entry):
    identry = me.getKey(entry)
    if (id == identry):
        return 0
    elif (id > identry):
        return 1
    else:
        return -1

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


def comparador_ascendente(pos1, pos2):
    if pos1["video_id"] != pos2["video_id"]:
        return True
    return False


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
