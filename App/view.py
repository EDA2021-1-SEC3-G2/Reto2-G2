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


def loadData(catalog):
    """
    carga los videos en la estructura de datos
    """
    controller.loadData(catalog)


def GoodVideosByCategoryAndConuntry(compilation):
    """
    busca videos por categoria y país"""
    size = lt.size(compilation)
    if size:
        for video in lt.iterator:
            print("Día que fue trending: " + compilation["trending_date"] + "Nombre del video: " + compilation["title"]+"Canal: " + compilation["channel_title"])
    else:
        print("No se encontraron videos")


def TrendByCategory(mosttrend):
    """video tendecia por categoría
    """


def MostLikedVideos(mostliked):
    """
    videos con mas likes
    """


catalog = {}


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        catalog = initLinkedCatalog()
        loadData(catalog)
        print("Categorias cargadas: " + str(lt.size(catalog['category'])))
        print("Videos cargados: " + str(lt.size(catalog['videos'])))
        # title, cannel_title, trending_date, country, views, likes, dislikes
        print("CATEGORIAS", end="\n\n")
        print(catalog['category'], end="\n\n")
        print("PRIMER VIDEO:", end="\n\n")
        print(catalog["videos"]["first"]["info"]["title"]+catalog["videos"]["first"]["info"]["channel_title"]+catalog["videos"]["first"]["info"]["trending_date"]+catalog["videos"]["first"]["info"]["country"]+catalog["videos"]["first"]["info"]["views"]+catalog["videos"]["first"]["info"]["likes"]+catalog["videos"]["first"]["info"]["dislikes"])
        print(catalog['videos'])
    elif int(inputs[0]) == 2:
        size = input("Indique tamaño de la muestra que desee: ")
        result = controller.sortVideos(catalog, int(size))
        print("Para la muestra de", size, " elementos, el tiempo (mseg) es: ",
                                          str(result[0]))
        country = input("Ingrese el país: ")
        category = input("Ingrese la categoria: ")
        number = input("cantidad de videos por listar: ")
        compilation = controller.getVideosByCategoryAndCountry(catalog, str(category), str(country), int(number))
        GoodVideosByCategoryAndConuntry(compilation)
    elif int(inputs[0]) == 3:
        country = input("Ingrese el país: ")
        mosttrend = controller.FindTrendVideoByCountry(catalog, country)
        print(mosttrend)

    elif int(inputs[0]) == 4:
        category = input("Ingrese la categoria: ")
        mosttrend = controller.TrendByCategory(catalog, category)
        TrendByCategory(mosttrend)

    elif int(inputs[0]) == 5:
        mostliked = controller.MostLikedVideos(catalog)
        MostLikedVideos(mostliked)

    else:
        sys.exit(0)
sys.exit(0)
