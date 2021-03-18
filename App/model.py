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



from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as merg
import time as time
import config as cf
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""


def newLinkedCatalog():
    catalog = {'videos': None,
               'category': None}
    catalog['videos'] = lt.newList()
    catalog['category'] = mp.newMap(30, maptype='CHAINING', loadfactor=0.5, comparefunction=comparecategories)
    return catalog


# Funciones para agregar informacion al catalogo


def addVideo(catalog, video):
    lt.addLast(catalog['videos'], video)


def addCategory(catalog, category):
    c = newCategory(category['id'], category['name'])
    lt.addLast(catalog['category'], c)


# Funciones para creacion de datos
def newCategory(name, id):
    category = me.newMapEntry(id, name)
    return category


# Funciones de consulta


def getCategory_ID(catalog, category_name):
    categories = catalog['category']
    for element in categories["elements"]:
        if lt.isPresent(element["name"], category_name) != 0:
            pos = lt.isPresent(element["name"], category_name)
    return categories['id'][pos]


def getFinalList(lis):
    final = {'trending_date': "", 'title': "",
             'channel_title': "", 'publish_time': "",
             'views': "", 'likes': "", 'dislikes': ""}
    final['trending_date'] = lis['trending date']
    final['title'] = lis['title']
    final['channel_title'] = lis['channel_title']
    final['publish_time'] = lis['publish_time']
    final['views'] = lis['views']
    final['likes'] = lis['likes']
    final['dislikes'] = lis['dislikes']
    return final


def getVideosByCategoryAndCountry(catalog, category_name, country,  numvid):
    videos = catalog['videos']
    mostviewedbycountandcat = lt.newList()
    templist = lt.newList()
    cat_id = getCategory_ID(catalog, category_name)
    cont = 0
    temp = numvid
    while cont < len(videos) and temp > 0:
        if videos[cont]['country'].lower() == country.lower() and videos[cont]['category_id'] == cat_id:
            lt.addLast(templist, videos[cont])
            temp -= 0
        cont += 1
    #mostviewedbycountandcat = getFinalList(templist)
    return mostviewedbycountandcat


def FindTrendVideoByCountry(catalog, country):
    videos_list = catalog['videos']
    sorted_list = merg.sort(videos_list, cmpVideosByCountry)
    pos = FindPositionTrendingCountry(sorted_list, country)
    sub_size = FindPositionEndTrendingCountry(sorted_list, country, pos)
    final_list = lt.subList(sorted_list, pos, sub_size)
    final_list = final_list.copy()
    sorted_final_list = merg.sort(final_list, cmpVideosByVideoID)
    result = FindTrendiestVideo(sorted_final_list)
    return result


def FindTrendVideoByCategory(catalog, category):
    paramater = getCategory_ID(catalog, category)
    for element in catalog["videos"]:
        if element["category_ID"] == catalog["videos"]["category_ID"] and element["category_ID"] != paramater:
            lt.deleteElement(element)
    most = FindTrendiestVideo(catalog)
    return most


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


# Funciones utilizadas para comparar elementos dentro de una lista


def comparecategories(name, category):
    return (name == category['name'])


def cmpVideosByViews(video1, video2):
    return(float(video1['views']) > float(video2['views']))


def cmpVideosByCountry(video1, video2):
    return(video1['country'].lower() < video2['country'].lower())


def cmpVideosByVideoID(video1, video2):
    return(video1['video_id'] == video2['video_id'])

# Funciones de ordenamiento


def sortVideos(catalog, size):
    sub_list = lt.subList(catalog['videos'], 1, size)
    sub_list = sub_list.copy()
    start_time = time.process_time()
    sorted_list = merg.sort(sub_list, cmpVideosByViews)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list
