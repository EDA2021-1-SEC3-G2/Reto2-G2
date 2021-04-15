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
    catalog['category'] = mp.newMap(33, maptype="PROBING", loadfactor=0.5, comparefunction=comparecategoriesmap)
    catalog["country"] = mp.newMap(30, maptype="CHAINING", loadfactor=5.0, comparefunction=compareCountrysByNameMap)
    catalog["categories"] = mp.newMap(33,maptype="CHAINING", loadfactor=5.0, comparefunction=comparecategoriesmap)

    # catalog['category_id'] = mp.newMap(37, maptype="CHAINING", loadfactor=5.0, comparefunction=comparecategoriesmap)
    return catalog


def list_user(cantidad):
    return 4


# Funciones para agregar informacion al catalogo

def addVideo(catalog, video):
    lt.addLast(catalog['videos'], video)
    addVideoCountry(catalog, video["country"].strip().lower(), video)
    addVideoCategoryMap(catalog, video["category_id"], video)


# Se agrega un mapentry
def addCategory(catalog, category):
    if mp.contains(catalog["category"], category['name']) is False:
        temp = newCategory(category['name'], category['id'])
        mp.put(catalog["category"], me.getKey(temp), me.getValue(temp))

def addVideoCountry(catalog, country, video):
    countries = catalog["country"]
    countryin = mp.contains(countries, country)
    if countryin:
        entry = mp.get(countries, country)
        keycountry = me.getValue(entry)
    else:
        keycountry = newCountry(country)
        mp.put(countries, country, keycountry)
    lt.addLast(keycountry["videos"], video)

def addVideoCategoryMap(catalog, category, video):
    categories_ = catalog["categories"]
    categoryin = mp.contains(categories_, category)
    if categoryin:
        entry = mp.get(categories_, category)
        keycategory = me.getValue(entry)
    else:
        keycategory = newCategoryID(category)
        mp.put(categories_, category, keycategory)
    lt.addLast(keycategory["videos"], video)


# Funciones para creacion de datos, se agerga un mapentry
def newCategory(name, id):
    category = me.newMapEntry(name.strip().lower(), id)
    return category

def newCountry(country):
    country = {"country":country, 
               "videos":lt.newList("ARRAY_LIST", cmpVideosByVideoID)}
    return country

def newCategoryID(categoryID):
    country = {"category":categoryID, 
               "videos":lt.newList("ARRAY_LIST", cmpVideosByVideoID)}
    return country


# Funciones de consulta


def getCategory_ID(catalog, category_name):
    categories = catalog['category']
    pair = mp.get(categories, category_name)
    result = me.getValue(pair)
    return result


def getVideosByCategoryAndCountry(catalog, category_name, country,  numvid):
    entry = mp.get(catalog["country"], country.strip().lower())
    dos = me.getValue(entry)
    reduced_list = dos["videos"]
    cat_id = getCategory_ID(catalog, category_name.strip().lower())
    templist = lt.newList("ARRAY_LIST")
    for element in lt.iterator(reduced_list):
        if element["country"].strip().lower() == country.strip().lower() and cat_id == element["category_id"]:
            lt.addLast(templist, element)
    sorted_videos = sortVideos(templist, 4)
    return sorted_videos


def FindTrendVideoByCountry(catalog, country):
    entry = mp.get(catalog["country"], country.strip().lower())
    dos = me.getValue(entry)
    reduced_list = dos["videos"]
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
    cat_id = getCategory_ID(catalog, category_name)
    entry = mp.get(catalog["categories"], cat_id)
    dos = me.getValue(entry)
    reduced_list = dos["videos"]
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
    entry = mp.get(catalog["country"], country.strip().lower())
    dos = me.getValue(entry)
    reduced_list = dos["videos"]
    print(lt.size(reduced_list))
    tag_list = lt.newList("ARRAY_LIST")
    for element in range(1, lt.size(reduced_list)+1):
        video = lt.getElement(reduced_list, element)
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


def compareCountrysByNameMap(keyname, country):
    """
    Compara dos nombres de paises. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(country)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
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
