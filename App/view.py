"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido")
    print("1- Cargar los videos")
    print("2- Buenos videos por categoría y país")
    print("3- Encontrar video tendencia por país")
    print("4- Buscar video tendencia por categoria")
    print("5- Video con más likes")
    print("0- Salir")


def initLinkedCatalog():
    # intento pasar la info tomada del imput en el menú.
    """inicializa el catalogo de videos"""
    return controller.initLinkedCatalog()


def initArrayCatalog():
    return controller.initArrayCatalog()


def loadData(catalog):
    """
    carga los videos en la estructura de datos
    """
    controller.loadData(catalog)


def GoodVideosByCategoryAndConuntry(compilation):
    """
    busca videos por categoria y país"""
    for element in range(1, number+1):
        video = lt.getElement(compilation, element)
        print(video["trending_date"]+"     "+video["title"]+"   "+video["channel_title"]+"   "+video["publish_time"]+"    "+video["views"]+"   "+video["likes"]+"    "+video["dislikes"])
    if lt.isEmpty(compilation):
        print("No se encontraron videos")


def TrendByCountry(info):
    "utiliza la informacion de la tupla y la ordena para entregarla al usuario"
    video = info[0]
    days = info[1]
    print(video["title"]+"   "+video["channel_title"]+"    "+video["country"]+"    "+str(days))


def TrendByCategory(mosttrend):
    """video tendecia por categoría
    """
    video = mosttrend[0]
    days = mosttrend[1]
    print(video["title"]+"   "+video["channel_title"]+"    "+video["country"]+"    "+str(days))


def MostLikedVideos(mostliked):
    """
    videos con mas likes
    """
    for element in range(1, lt.size(mostliked)):
        video = lt.getElement(mostliked, element)
        print("")
        print(video["title"]+"   "+video["channel_title"]+"   "+video["publish_time"]+"    "+video["views"]+"   "+video["likes"]+"    "+video["dislikes"]+"    "+video["tags"])


catalog = {}


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        catalog = initArrayCatalog()
        loadData(catalog)
        print("Categorias cargadas: " + str(lt.size(catalog['category'])))
        print("Videos cargados: " + str(lt.size(catalog['videos'])))
        # title, cannel_title, trending_date, country, views, likes, dislikes
        print("CATEGORIAS", end="\n\n")
        print(catalog['category'], end="\n\n")
        print("PRIMER VIDEO:", end="\n\n")
        print(lt.getElement(catalog["videos"], 1))
    elif int(inputs[0]) == 2:
        country = input("Ingrese el país: ")
        category = input("Ingrese la categoria: ")
        number = int(input("cantidad de videos por listar: "))
        compilation = controller.getVideosByCategoryAndCountry(catalog, str(category), str(country), int(number))
        GoodVideosByCategoryAndConuntry(compilation)
    elif int(inputs[0]) == 3:
        country = input("Ingrese el país: ")
        mosttrend = controller.FindTrendVideoByCountry(catalog, country)
        TrendByCountry(mosttrend)
        
    elif int(inputs[0]) == 4:
        category = input("Ingrese la categoria: ")
        mosttrend = controller.FindTrendVideoByCategory(catalog, category)
        TrendByCategory(mosttrend)

    elif int(inputs[0]) == 5:
        tag = input("Ingrese el tag de interés: ")
        country = input("ingrese el país: ")
        elements = input("Ingrese el numero de elementos a listar: ")
        mostliked = controller.FindMostLikedByTag(catalog, tag, country, elements)
        MostLikedVideos(mostliked)

    else:
        sys.exit(0)
sys.exit(0)
