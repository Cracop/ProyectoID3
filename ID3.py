import pandas as pd
import numpy as np
import itertools 
import math

ycol = 'lluvia'
dftrain = pd.read_csv('prueba.csv')
y_train = dftrain[ycol] 

valores = y_train.unique() 
#print(dftrain.head())

class Nodo:
    def __init__(self, nombre, padre, arista=None):
        self.nombre=nombre
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



def entropia(atributo):
    entropia = 0
   
    for valor in dftrain[atributo].unique():
        
        filasQueImportan = dftrain[dftrain[atributo]==valor] 
        n = 0
        print(len(filasQueImportan.index), "/", dftrain[atributo].size)
        proba1 = len(filasQueImportan.index)/dftrain[atributo].size
        
        for resultado in filasQueImportan[ycol].unique():
        
            resultadosQueImportan = filasQueImportan[filasQueImportan[ycol]==resultado]
            print("  ", resultado, len(resultadosQueImportan.index), "/", len(filasQueImportan.index))
            proba2 = len(resultadosQueImportan.index)/len(filasQueImportan.index)
            n += proba2*math.log2(proba2)
        
        entropia += proba1*(-1)*(n)
    print(atributo, entropia)

for atributo in dftrain.columns:
    entropia(atributo)
#entropia('anxiety')
#entropiaDelDataSet("prognosis")
#print(dftrain.columns)
