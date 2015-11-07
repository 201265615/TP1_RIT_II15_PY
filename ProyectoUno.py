#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################
##                                                  ##
##       Instituto Tecnologico de Costa Rica        ##
##           Primer Proyecto Programado             ##
##       Recuperacion de Informacion Textual        ##
##                                                  ##
######################################################
##                                                  ##
## Autor: Kevin Alonso Escobar Miranda - 201265615  ##
## Profesor: Jose Enrique Araya Monge               ##
## FechaCreacion: 29 de agosto de 2015              ##
##                                                  ##
######################################################
##                                                  ##
##                  Nomenclatura                    ##
## Funciones:                                       ##
##              deben iniciar en minuscula          ##
##              primer palabra verbo infinitivo     ##
##              segunda palabra describe funcion    ##
##              cada palabra inicia con mayuscula   ##
##              Ejemplo: ejemplicarFuncion          ##
##                                                  ##
## Parametros:                                      ##
##              deben tener el prefijo p            ##
##              seguido de la descripcion           ##
##              cada palabra inicia en mayuscula    ##
##              Ejemplo: pParametroEjemplo          ##
##                                                  ##
######################################################

import codecs                   # para leer unicode
import re                       # para expresiones regulares
import unicodedata              # para eliminar tildes
from collections import Counter # para contar apariciones de palabras
import collections              # para las colecciones
import csv                      # para crear csv


########################
##
## Nombre: cargarArchivo
## Descripcion:
##              Abre y carga el archivo que se seleccione segun la ruta
## Parametros:
##              pRuta: ruta donde se encuentra el archivo
## Return:
##              texto leido
##
########################

def cargarArchivo(pRuta):
    # se abre el archivo y se indica que es unicode para que lea las tildes (en mi caso daba error si no lo hacia asi)
    archivo = open(pRuta,"r",encoding='utf-8');

    textoLeido = ""

    # se leer el archivo linea por linea
    for linea in archivo:
        textoLeido += linea
    return textoLeido.lower() #convierte texto a minuscula


########################
##
## Nombre: sustituirPalabras
## Descripcion: 
##              lee el texto y sustituye las palabras segun la tabla de reemplazo
## Parametros:
##              pTexto: texto al cual hay que sustituir las palabras
##              tablaReemplazo: contiene las llaves y valores a sustituir
## Return:
##              nuevoTexto
##
########################

def sustituirPalabras(pTexto,pTablaReemplazo):
    # se crea una expresion regular desde el diccionario
    regex = re.compile("(%s)" % "|".join(map(re.escape, pTablaReemplazo.keys())))

    # se analiza el texto y si con tiene una abreviatura se reemplaza
    nuevoTexto = regex.sub(lambda x: str(pTablaReemplazo[x.string[x.start() :x.end()]]), pTexto)

    return nuevoTexto




########################
##
## Nombre: sustituirAbreviaturas
## Descripcion: 
##              lee el texto y sustituye las abreviaturas previamente definidas
## Parametros:
##              pTexto: texto al cual hay que sustituir las abreviaturas
## Return:
##              texto sin abreviaturas
##
########################

def sustituirAbreviaturas(pTexto):
    # se crea una tabla que contiene las abreviaturas y sus significados
    tablaReemplazo = {
            "ca."      :   "aproximadamente",
            "carib."   :   "caribe",
            "cord."    :   "cordillera",
            "pac."     :   "pacifico",
            "fl."      :   "flor",
            "fls."     :   "flores",
            "fr."      :   "fruto",
            "frs."     :   "frutos",
            "vert."    :   "vertiente",
            "verts."   :   "vertientes"
        }
    return sustituirPalabras(pTexto,tablaReemplazo)




########################
##
## Nombre: eliminarTildes
## Descripcion:
##              sustituye las letras tildadas por letras sin tildar
## Parametros:
##              pTexto
## Return:
##              texto sin acentuaciones (sin tildes)
##
########################

def eliminarTildes(pTexto):
    tablaReemplazo = {
            "á"     :   "a",
            "é"     :   "e",
            "í"     :   "i",
            "ó"     :   "o",
            "ú"     :   "u",
            "\r"    :   " ",
            "\n"    :   " ",
            "\t"    :   " "
        }
    return sustituirPalabras(pTexto,tablaReemplazo)


########################
##
## Nombre: eliminarTildes
## Descripcion:
##              sustituye las letras tildadas por letras sin tildar
## Parametros:
##              pTexto
## Return:
##              texto sin acentuaciones (sin tildes)
##
########################

def eliminarTildes(pTexto):
    tablaReemplazo = {
            "á"     :   "a",
            "é"     :   "e",
            "í"     :   "i",
            "ó"     :   "o",
            "ú"     :   "u",
            "\r"    :   " ",
            "\n"    :   " ",
            "\t"    :   " "
        }
    return sustituirPalabras(pTexto,tablaReemplazo)


########################
##
## Nombre: extraerPalabrasNumeros
## Descripcion:
##              extrae las palabras y numeros en una lista              
## Parametros:
##              pTexto
## Return:
##              [listaNumeros+listaPalabras]
##
########################

def extraerPalabrasNumeros(pTexto):
    # listas donde se almacenaran las palabras extraidas
    listaNumeros = []
    listaPalabras = []

    # nota: \b es para indicar que es fin o inicio de palabra
    # \b\d+\.?\d+\b para extraer solo numeros segun la especificacion ej: 0.4
    listaNumeros = re.findall(r'\b\d+\.?\d+?\b', pTexto)
    
    # ([b([A-Za-zÑñ]+)\b para extraer palabras mayus o minus
    listaPalabras = re.findall(r'\b([A-Za-zÑñ]+)\b', pTexto)

    return listaNumeros+listaPalabras
    


    
########################
##
## Nombre: contarPalabrasNumeros
## Descripcion:
##              cuenta las palabras y numeros del texto que cumplen las exp reg
## Parametros:
##              pListaPalabrasNumeros
## Return:
##              [cantidad]
##
########################

def contarPalabrasNumeros(pListaPalabrasNumeros):
    cantidad = sorted(Counter(pListaPalabrasNumeros).items())
    return cantidad




########################
##
## Nombre: estructurarClaveDicotomica
## Descripcion:
##              leer el texto para estructurar la clave dicotomica
## Parametros:
##              pTexto
## Return:
##              [[clave1],[clave2],[claveN]]
##
########################

def estructurarClaveDicotomica(pTexto):
    #############################################################################
    #                                                                           #
    #                 DESCRIPCION DE LA EXPRESION REGULAR                       #
    #                                                                           #
    # group(nivel)     ->    (?P<nivel>\d+\ ?)      : nivel                     #
    # group(prima)     ->    (?P<prima>\'\ )?       : prima                     #
    # group(condicion) ->    (?P<condicion>.*?\.\ ) : condicion                 #
    # group(puntos)    ->    (?P<puntos>\.\ )*      : puntos                    #
    # group(grupo)     ->    (?P<grupo>[a-z]*)      : grupo                     #
    #                                                                           #
    #############################################################################
    
    # se declara el patron con los grupos
    patron = r'(?P<nivel>\d+\ ?)(?P<prima>\'\ )?(?P<condicion>.*?\.\ )(?P<puntos>\.\ )*(?P<grupo>[a-z]*)'

    listaResultado = []
    
    # se realiza la busqueda
    for busqueda in re.finditer(patron, pTexto):
        # se obtienen los valores de los grupos
        nivel = busqueda.group('nivel')
        prima = busqueda.group('prima')
        condicion = busqueda.group('condicion')
        grupo = busqueda.group('grupo')

        # evaluar si tiene prima(1) o no(0)
        resultadoPrima = (1,0)[prima is None]
        
        #print(str(nivel)+"\t"+str(resultadoPrima)+"\t"+str(condicion)+"\t"+str(grupo))
        tuplaNueva = (str(nivel),str(resultadoPrima),str(condicion),str(grupo))
        listaResultado.append(tuplaNueva)
    return listaResultado

        




#######################
##
## Nombre: eliminarNone
## Descripcion:
##              evita que se imprima la palabra None
## Parametros:
##              pTexto
## Return:
##              pTexto or ''
##
########################

def eliminarNone(pTexto):
    if pTexto is None:
        return ''
    return str(pTexto)



#######################
##
## Nombre: extraerRangos
## Descripcion:
##              leer el texto para extraer los rangos
## Parametros:
##              pTexto
## Return:
##              [[clave1],[clave2],[claveN]]
##
########################

def extraerRangos(pTexto):
    #############################################################################
    #                                                                           #
    #                 DESCRIPCION DE LA EXPRESION REGULAR                       #
    #                                                                           #
    # group(inf1) -> (\((?P<inf1>\d+\.\d+|\d+)\-\))?             : inferior1    #
    # group(min1) -> (?P<min1>\d+\.\d+|\d+)                      : minimo1      #
    # \-                                                                        #
    # group(max1) -> (?P<max1>\d+\.\d+|\d+)                      : maximo1      #
    # group(sup1) -> (\(\-(?P<sup1>\d+\.\d+|\d+)\))?             : superior1    #
    # /                                                                         #
    # group(dimension) -> (?P<dimension>\ [x]\ )                 : dimension    #
    # group(inf2) -> (\((?P<inf2>\d+\.\d+|\d+)\-\))?             : inferior1    #
    # group(min2) -> (?P<min2>\d+\.\d+|\d+)                      : minimo2      #
    # \-                                                                        #
    # group(max2) -> (?P<max2>\d+\.\d+|\d+)                      : maximo2      #
    # group(sup2) -> (\(\-(?P<sup2>\d+\.\d+|\d+)\))?             : superior2    #
    # )?                                                                        #
    # group(unidadMedida) -> (\+?\ (?P<unidadMedida>[a-zñ][a-zñ]?)\b)? : undMedid #
    #                                                                           #
    #############################################################################
    
    # se declara el patron con los grupos anteriormente descritos
    patron = r'(\((?P<inf1>\d+\.\d+|\d+)\-\))?(?P<min1>\d+\.\d+|\d+)\-(?P<max1>\d+\.\d+|\d+)(\(\-(?P<sup1>\d+\.\d+|\d+)\))?((?P<dimension>\ [x]\ )(\((?P<inf2>\d+\.\d+|\d+)\-\))?(?P<min2>\d+\.\d+|\d+)\-(?P<max2>\d+\.\d+|\d+)(\(\-(?P<sup2>\d+\.\d+|\d+)\))?)?(\+?\ (?P<unidadMedida>[a-zñ][a-zñ]?)\b)?'

    listaResultados = []
    # se realiza la busqueda
    for busqueda in re.finditer(patron, pTexto):
        # se obtienen los valores de los grupos 1
        inf1 = busqueda.group('inf1')
        min1 = busqueda.group('min1')
        max1 = busqueda.group('max1')
        sup1 = busqueda.group('sup1')

        # se obtienen los valores de los grupos 2
        inf2 = busqueda.group('inf2')
        min2 = busqueda.group('min2')
        max2 = busqueda.group('max2')
        sup2 = busqueda.group('sup2')

        # se obtiene la unidad de medida y la dimension
        unidadMedida = busqueda.group('unidadMedida')
        dimension = busqueda.group('dimension')
        
        # se verifica si es de una o dos dimensiones
        resultadoDimension = (1,2)[dimension == " x "]

        # se muestra la estructura
        #print(str(resultadoDimension)+"\t"+eliminarNone(unidadMedida)+"\t"+eliminarNone(inf1)+"\t"+eliminarNone(min1)+"\t"+eliminarNone(max1)+"\t"+eliminarNone(sup1)+"\t"+eliminarNone(inf2)+"\t"+eliminarNone(min2)+"\t"+eliminarNone(max2)+"\t"+eliminarNone(sup2))
        tuplaNueva = (str(resultadoDimension),eliminarNone(unidadMedida),eliminarNone(inf1),eliminarNone(min1),eliminarNone(max1),eliminarNone(sup1),eliminarNone(inf2),eliminarNone(min2),eliminarNone(max2),eliminarNone(sup2))
        listaResultados.append(tuplaNueva)
    return listaResultados


########################
##
## Nombre: crearCSV
## Descripcion:
##              crea un archivo csv (valores separados por comas)
## Parametros:
##              pRuta: ruta y nombre donde se creara
## Return:
##              0
##
########################
        
def crearCSV(pRuta,pListaValores):
    c = csv.writer(open(pRuta, "w",encoding='utf-8'), delimiter = "\t")
    c.writerows(pListaValores)

        

########################
##
## Nombre: desplegarMenu
## Descripcion:
##              muestra el menu para utilizar el programa
## Parametros:
##              no tiene
## Return:
##              no tiene
##
########################

def desplegarMenu():
    while(True):
        rutaArchivo = str(input("Escribe la ruta del archivo:\n"))
        try:
            textoArchivo = cargarArchivo(rutaArchivo)

            textoArchivo = sustituirAbreviaturas(textoArchivo)
            textoArchivo = eliminarTildes(textoArchivo)
            
            listaPalabrasNumeros = extraerPalabrasNumeros(textoArchivo)
            listaConteoPalabrasNumeros = contarPalabrasNumeros(listaPalabrasNumeros)
            crearCSV("Diccionario.csv",listaConteoPalabrasNumeros)

            listaRangos = extraerRangos(textoArchivo)
            crearCSV("Rangos.csv",listaRangos)
            
            listaClaves = estructurarClaveDicotomica(textoArchivo)
            crearCSV("Claves.csv",listaClaves)
        except:
            print("Error, Intenta de nuevo")
        

        
desplegarMenu()
