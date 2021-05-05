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

    def buscaHijo(self, arista): #Si lle
        for hijo in self.hijos:
            if hijo.arista==arista:
                return hijo
        raise 

class ArbolID3:
    def __init__(self):
        self.root=None
        self.atributos=None

    def entropia(self,atributo, ycol):
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

    def seleccionaMejorAtributo(self, df, atributos, ycol):
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

    def encontrarCaminos(self, nodoActual, atributos, ycol, dftrain):
        caminos = dftrain[nodoActual.valor].unique()
        #print("nodoCreado")
        for camino in caminos:
            dfAux = dftrain[dftrain[nodoActual.valor]==camino]
            #print(nodoActual.valor, "=",camino)
            del dfAux[nodoActual.valor]
            self.crearHijos(nodoActual, camino, ycol, dfAux, atributos)
        
    def crearHijos(self, nodoActual, camino, ycol, df, atributos):
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

    def predecir(self, df):
        total = 0
        correctas = 0
        for index, row in df.iterrows():
            predic = self.realizarPrognosis(row)
            total += 1
            print("Prediccion: "+predic, " || Correcta: "+row["prognosis"])
            if row["prognosis"] == predic:
                correctas += 1
            
        print(str((correctas/total)*100)+"% fueron correctas")
        
    def realizarPrognosis(self,caso):
        nodoActual = self.root
        for index, value in caso.items():
            if len(nodoActual.hijos) == 0:
                return nodoActual.valor
            else:
                #predic =  ""
                predic = (nodoActual.padre.valor + "-" + str(nodoActual.arista))if nodoActual.padre != None else ""
                print(predic)
                nodoActual = nodoActual.buscaHijo(caso[nodoActual.valor])
            
            #print(caso[index])
            #print(f"Index : {index}, Value : {value}")

    def diagnosticar(self):
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

def exportarArbol(nodo, nombre):
    arbol = crearArbolDiccionario(nodo)
    with open(nombre, 'w') as fp:
        json.dump(arbol, fp,  indent=2)

def importarArbol(archivo):
    with open(archivo) as f:
        arbol = json.load(f)
        return deDiccionarioAArbol(arbol)

def deDiccionarioAArbol(diccionario, nodoPadre=None):
    if diccionario == None:
        return
    nodo = Nodo(diccionario["valor"], nodoPadre, diccionario["arista"])
    for hijo in diccionario["hijos"]:
        nodo.addHijo(deDiccionarioAArbol(hijo, nodo))
    return nodo


def recortarArbol(nodo):
    if nodo == None:
        return
    #print(nodo.valor)
    if len(nodo.hijos) == 1 and nodo.padre != None:
        abuelo = nodo.padre
        nieto = nodo.hijos.pop()
        nieto.padre=abuelo
        abuelo.hijos.clear()
        abuelo.addHijo(nieto)
        nieto.arista=nodo.arista
        print(abuelo.valor, nodo.valor, nieto.valor)
    else:
        for hijo in nodo.hijos:
            recortarArbol(hijo)
        
    

ycol = "lluvia"
dftrain = pd.read_csv('prueba.csv')
y_train = dftrain[ycol] 

dftest = pd.read_csv('Testing.csv')


ic = ArbolID3()
#inicio = time.time()
#ic.entrenar(dftrain,ycol)
#print("--- %s segundos ---" % (time.time() - inicio))
#print("Arbol Generado al Entrenar")
#pprint_tree(ic.root)
#exportarArbol(ic.root, "ArbolChico.json")
#print("PreRecorte")
ic.root=importarArbol("ArbolID3.json")
#exportarArbol(ic.root, "A.json")
#pprint_tree(ic.root)
#ic.predecir(dftest)
ic.diagnosticar()
#recortarArbol(ic.root)
#print("PostRecorte")
#pprint_tree(ic.root)

