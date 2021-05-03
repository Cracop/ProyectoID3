import pandas as pd
import numpy as np
import itertools 
import math
import time 

ycol = "prognosis"
dftrain = pd.read_csv('Training.csv')
y_train = dftrain[ycol] 

valores = y_train.unique() 
#print(dftrain.head())

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
        return None 
    
    def imprimeHijos(self, level=0):
        if self.arista != None:
            print("\t" * level + self.arista + " -- "+self.valor)
        else:
            print("\t" * level + self.valor)
        #print(self.hijos)
        for hijo in self.hijos:
            hijo.imprimeHijos(level+1)

    
class ArbolID3:
    def __init__(self):
        self.root=None
        self.atributos=None

    def entropia(self,atributo, ycol):
        entropia = 0
   
        for valor in dftrain[atributo].unique():
        
            filasQueImportan = dftrain[dftrain[atributo]==valor] 
            n = 0
            #print(len(filasQueImportan.index), "/", dftrain[atributo].size)
            proba1 = len(filasQueImportan.index)/dftrain[atributo].size
        
            for resultado in filasQueImportan[ycol].unique():
        
                resultadosQueImportan = filasQueImportan[filasQueImportan[ycol]==resultado]
                #print("  ", resultado, len(resultadosQueImportan.index), "/", len(filasQueImportan.index))
                proba2 = len(resultadosQueImportan.index)/len(filasQueImportan.index)
                n += proba2*math.log2(proba2)
        
            entropia += proba1*(-1)*(n)
        return entropia

    def crearNodo(self, valor, padre, arista=None):
        return Nodo(valor, padre, arista)

    def seleccionaMejorAtributo(self, df, atributos, ycol):
        #print(atributos)
        atri = list()
        entropias = list()
        for atributo in  atributos:
            if atributo != ycol:
                atri.append(atributo)
                entropias.append(self.entropia(atributo, ycol))
        #print(entropias, atri)
        return atri[np.argmin(entropias)]

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
            #print(df)

    def verArbol(self):
        self.root.imprimeHijos()

    #Código sacado de https://vallentin.dev/2016/11/29/pretty-print-tree
def pprint_tree(node, file=None, _prefix="", _last=True):
    print(_prefix, "`- " if _last else "|- ", node.arista if node.arista != None else "","-> ",node.valor, sep="", file=file)
    _prefix += "   " if _last else "|  "
    child_count = len(node.hijos)
    for i, child in enumerate(node.hijos):
        _last = i == (child_count - 1)
        pprint_tree(child, file, _prefix, _last)
    
ic = ArbolID3()
#for atributo in dftrain.columns:
#    ic.entropia(atributo)
#print(ic.seleccionaMejorAtributo(dftrain))
#print(ic.entropia('vomiting'))
inicio = time.time()
ic.entrenar(dftrain,ycol)
print("--- %s segundos ---" % (time.time() - inicio))
print(" ")
#ic.verArbol()
pprint_tree(ic.root)
#entropiaDelDataSet("prognosis")
#print(dftrain.columns)print("--- %s segundos ---" % (time.time() - inicio))
