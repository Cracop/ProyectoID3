import pandas as pd
import numpy as np
import itertools 
import math
import time 
import json

class Nodo:
    def __init__(self,valor, padre, arista=None):
        self.valor=valor
        self.padre=padre
        self.hijos = []
        self.arista=arista #Es como der e izq en un bst
        #Una arista es por donde llego al nodo, tipo trie

    def addHijo(self, hijo):
        self.hijos.append(hijo)

    def buscaHijo(self, arista): #Me regresa el hijo en el camino que diga
        for hijo in self.hijos:
            if hijo.arista==arista:
                return hijo
        raise 

class ArbolID3:
    def __init__(self):
        self.root=None
        self.atributos=None

    def entropia(self,atributo, ycol): #Calcula la entropía de un solo atributo
        entropia = 0
   
        for valor in dftrain[atributo].unique():
        
            filasQueImportan = dftrain[dftrain[atributo]==valor] 
            n = 0
            proba1 = len(filasQueImportan.index)/dftrain[atributo].size
        
            for resultado in filasQueImportan[ycol].unique():
        
                resultadosQueImportan = filasQueImportan[filasQueImportan[ycol]==resultado]
                proba2 = len(resultadosQueImportan.index)/len(filasQueImportan.index)
                n += proba2*math.log2(proba2)
        
            entropia += proba1*(-1)*(n)
        return entropia

    def crearNodo(self, valor, padre, arista=None):
        return Nodo(valor, padre, arista)

    def seleccionaMejorAtributo(self, df, atributos, ycol): #Selecciono el atributo con menor entropía que sea mayor a cero
        atri = list()
        entropias = list()
        for atributo in  atributos:
            if atributo != ycol:
                atri.append(atributo)
                entropias.append(self.entropia(atributo, ycol))
        return atri[np.argmin(np.nonzero(entropias))]

    def entrenar(self, dftrain, ycol):
        self.atributos=list(dftrain.columns) #Creo una lista de los atributos (para pasarlos luego)
        self.atributos.remove(ycol) #Para quitar la columna que me importa
        #Busco el atributo con la menor entropía y la vuelvo raíz
        root = self.seleccionaMejorAtributo(dftrain,self.atributos, ycol)
        self.atributos.remove(root)
        self.root=self.crearNodo(root, None)
        #self.crearHijos(self.root, self.atributos, ycol, dftrain)
        self.encontrarCaminos(self.root, self.atributos, ycol, dftrain)

    def encontrarCaminos(self, nodoActual, atributos, ycol, dftrain): #Encuentro los caminos que salen de cada nodo
        caminos = dftrain[nodoActual.valor].unique()
        #print("nodoCreado")
        for camino in caminos:
            dfAux = dftrain[dftrain[nodoActual.valor]==camino]
            #print(nodoActual.valor, "=",camino)
            del dfAux[nodoActual.valor]
            self.crearHijos(nodoActual, camino, ycol, dfAux, atributos)
        
    def crearHijos(self, nodoActual, camino, ycol, df, atributos): #Creo los hijos dependiendo del camino
        resultados = df[ycol].unique()
        if len(resultados)==1: #Caso base
            #print(df)
            nodoActual.addHijo(self.crearNodo(resultados[0], nodoActual, camino))
            return
        else:
            atributosAux=atributos.copy()
            nodo = self.seleccionaMejorAtributo(df,atributosAux, ycol)
            atributosAux.remove(nodo)
            nodo = self.crearNodo(nodo, nodoActual, camino)
            nodoActual.addHijo(nodo)
            self.encontrarCaminos(nodo, atributosAux, ycol, df)

    def predecir(self, df): #Analizo todo el dataset de prueba
        total = 0
        correctas = 0
        for index, row in df.iterrows():
            predic = self.realizarPrognosis(row)
            total += 1
            print("Prediccion: "+predic, " || Correcta: "+row["prognosis"])
            if row["prognosis"] == predic:
                correctas += 1
            
        print(str((correctas/total)*100)+"% fueron correctas")
        
    def realizarPrognosis(self,caso): #Para cada renglón del dataset de prueba, realizo una predicción
        nodoActual = self.root
        for index, value in caso.items():
            if len(nodoActual.hijos) == 0:
                return nodoActual.valor
            else:
                #predic =  ""
                predic = (nodoActual.padre.valor + "-" + str(nodoActual.arista))if nodoActual.padre != None else ""
                #print(predic)
                nodoActual = nodoActual.buscaHijo(caso[nodoActual.valor])
            
            #print(caso[index])
            #print(f"Index : {index}, Value : {value}")

    def diagnosticar(self): #Sirve para diagnosticar por medio de la terminal
        nodo = self.root
        while len(nodo.hijos)!= 0:
            print(nodo.valor+"?")
            ans = input()
            try:
                nodo = nodo.buscaHijo(int(ans))
            except:
                print("Say Again?")
        print("Diagnóstico: "+nodo.valor)


#Código sacado de https://vallentin.dev/2016/11/29/pretty-print-tree
def pprint_tree(node, file=None, _prefix="", _last=True):
    print(_prefix, "`-" if _last else "|-", node.arista if node.arista != None else "","-> ",node.valor, sep="", file=file)
    _prefix += " " if _last else "| "
    child_count = len(node.hijos)
    for i, child in enumerate(node.hijos):
        _last = i == (child_count - 1)
        pprint_tree(child, file, _prefix, _last)
#


def crearArbolDiccionario(nodo): #Creo un megadiccionario
    if nodo == None:
        return
    node = dict()
    node["valor"]=nodo.valor
    if nodo.arista != None:
        node["arista"]= int(nodo.arista) #if type(nodo.arista) is int else nodo.arista
    else:
        node["arista"]=nodo.arista
    if nodo.padre != None:
        node["padre"]=nodo.padre.valor
    else:
        node["padre"]=nodo.padre
    node["hijos"]=[]
    for hijo in nodo.hijos:
        node["hijos"].append(crearArbolDiccionario(hijo))
    return node

def exportarArbol(nodo, nombre): #Paso el megadiccionario a un JSON
    arbol = crearArbolDiccionario(nodo)
    with open(nombre, 'w') as fp:
        json.dump(arbol, fp,  indent=2)

def importarArbol(archivo): #Leo un JSON y lo paso a un megadiccionario
    with open(archivo) as f:
        arbol = json.load(f)
        return deDiccionarioAArbol(arbol)

def deDiccionarioAArbol(diccionario, nodoPadre=None): #Conforme voy leyendo los diccionarios voy creando los nodos
    if diccionario == None:
        return
    nodo = Nodo(diccionario["valor"], nodoPadre, diccionario["arista"])
    for hijo in diccionario["hijos"]:
        nodo.addHijo(deDiccionarioAArbol(hijo, nodo))
    return nodo


def recortarArbol(nodo): #Se trató de eliminar ramas donde no había valores distintos
    if nodo == None:
        return None
    nuevosHijos = nodo.hijos.copy()
    nodo.hijos.clear()
    for hijo in nuevosHijos:
        nodo.addHijo(recortarArbol(hijo))
    
    if len(nodo.hijos)==0:
        return nodo

    if len(nuevosHijos) == 1:
        nuevoNodo = nuevosHijos.pop()
        nuevoNodo.arista = nodo.arista
        nuevoNodo.padre = nodo.padre
        temp = nodo
        nodo = None
        del (temp)
        return nuevoNodo

    return nodo  

class Doctor(): #Clase con la cual la parte gráfica puede realizar los diagnósticos
    def __init__(self, root):
        self.root = root
        self.Diagnostico = False

    def preguntar(self):
        if len(self.root.hijos) == 0:
            self.Diagnostico = True
            return self.root.valor
        return self.root.valor

    def responderParam(self, arista):
        if self.Diagnostico==True:
            return
        try:
            self.root = self.root.buscaHijo(int(arista))
        except:
            self.root=self.root

""" Conjunto de entrenamiento que vimos en clase, para ver que funcionara """
"""
ycol = "lluvia"
dftrain = pd.read_csv('prueba.csv')
y_train = dftrain[ycol] 
"""

""" Conjunto de Entrenamiento que utilizamos """
ycol = "prognosis"
dftrain = pd.read_csv('Training.csv')
y_train = dftrain[ycol] 

""" Conjunto con el que probamos nuestro modelo """
dftest = pd.read_csv('Testing.csv')

""" Creo el objeto Arbol, el cual lo voy a entrenar """
ic = ArbolID3()

""" Descomentar esto cuando lo quiero entrenar desde cero """
#ic.entrenar(dftrain,ycol)

""" Para guardar el arbol en un formato JSON y no tener que generarlo desde cero """
#exportarArbol(ic.root, "ArbolID3.json")

""" Para cargar un árbol desde un archivo JSON """
ic.root=importarArbol("ArbolID3.json")

""" Para ver de una forma bonita el árbol generado """
#pprint_tree(ic.root)

""" Para hacer más cortas las ramas del arbol """
# ic.root=recortarArbol(ic.root)
# pprint_tree(ic.root)
# exportarArbol(ic.root, "ArbolID3.json")

""" Para realizar pruebas con el conjunto de prueba """
ic.predecir(dftest)

""" Para responder a las preguntas por medio de la terminal """
#ic.diagnosticar()

""" Para conectarse con  la parte gráfica """
dc = Doctor(ic.root)

# while not dc.Diagnostico:
#     print(dc.preguntar())
#     dc.responderParam(input())
#     dc.preguntar()

# print(dc.preguntar())



    



