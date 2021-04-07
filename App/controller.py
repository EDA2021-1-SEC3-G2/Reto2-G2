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
 """

import sys
import config as cf
import model
import csv
default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros


def initArrayCatalog():
    return model.newArrayCatalog()


# Funciones para la carga de datos


def loadData(catalog):
    loadVideos(catalog)
    loadCategoryID(catalog)


def loadVideos(catalog):
    videosfile = cf.data_dir + 'videos-large.csv'
    input_file = csv.DictReader(open(videosfile, encoding='utf-8'))
    for video in input_file:
        model.addVideo(catalog, video)


def loadCategoryID(catalog):
    categoryfile = cf.data_dir + 'category-id.csv'
    input_file = csv.DictReader(open(categoryfile, encoding='utf-8'), delimiter='\t')
    print(input_file)
    for categ in input_file:
        model.addCategory(catalog, categ)


# Funciones de ordenamiento
# test


def sortVideos(catalog, size, alg):
    return model.sortVideos(catalog, size, alg)

# Funciones de consulta sobre el catálogo


def getVideosByCategoryAndCountry(catalog, category_name, country,  numvid):
    print(category_name, country)
    return model.getVideosByCategoryAndCountry(catalog, category_name, country, numvid)


def FindTrendVideoByCountry(catalog, country):
    return model.FindTrendVideoByCountry(catalog, country)


def FindTrendVideoByCategory(catalog, category):
    return model.FindTrendVideoByCategory(catalog, category)


def FindMostLikedByTag(catalog, tag, country, elements):
    return model.FindMostLikedByTag(catalog, tag, country, elements)