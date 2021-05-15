from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

import pandas as pd

from django.shortcuts import render

from Modelo.ID3 import *

""" Conjunto de entrenamiento que vimos en clase, para ver que funcionara """
"""
ycol = "lluvia"
dftrain = pd.read_csv('prueba.csv')
y_train = dftrain[ycol] 
"""

""" Conjunto de Entrenamiento que utilizamos """
ycol = "prognosis"
dftrain = pd.read_csv('./Modelo/Training.csv')
y_train = dftrain[ycol]

""" Conjunto con el que probamos nuestro modelo """
dftest = pd.read_csv('./Modelo/Testing.csv')

""" Creo el objeto Arbol, el cual lo voy a entrenar """
ic = ArbolID3()

""" Descomentar esto cuando lo quiero entrenar desde cero """
# ic.entrenar(dftrain,ycol)

""" Para guardar el arbol en un formato JSON y no tener que generarlo desde cero """
#exportarArbol(ic.root, "ArbolID3.json")

""" Para cargar un árbol desde un archivo JSON """
ic.root = importarArbol("./Modelo/ArbolID3.json")

""" Para ver de una forma bonita el árbol generado """
# pprint_tree(ic.root)

""" Para hacer más cortas las ramas del arbol """
# ic.root=recortarArbol(ic.root)
# pprint_tree(ic.root)
# exportarArbol(ic.root, "ArbolID3.json")

""" Para realizar pruebas con el conjunto de prueba """
ic.predecir(dftest)


""" Para responder a las preguntas por medio de la terminal """
# ic.diagnosticar()

""" Para conectarse con  la parte gráfica """
dc = Doctor(ic.root)

# while not dc.Diagnostico:
#     print(dc.preguntar())
#     dc.responderParam(input())
#     dc.preguntar()

# print(dc.preguntar())


def index(request):
    return render(request, "build/index.html")


@api_view(['GET'])
def comenzarJuego(request):
    if request.method == 'GET':
        dc = Doctor(ic.root)
        return Response({
            'status': 'QA start',
            'pregunta': dc.preguntar(),
        })


@api_view(['GET'])
def sendAns(request, ans):
    if request.method == 'GET':
        dc.responderParam(ans)
        if len(dc.root.hijos) == 0:
            return Response({
                'status': "Diagnostico Final",
                'pregunta': dc.preguntar(),
            })
        else:
            return Response({
                'status': ans,
                'pregunta': dc.preguntar(),
            })
