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


class ArbolID3:
    def __init__(self):
        self.root=None
        self.atributos=None



    def entropia(self,atributo):
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

    def seleccionaMejorAtributo(self, df):
        atri = list()
        entropias = list()
        for atributo in  df.columns:
            if atributo != ycol:
                atri.append(atributo)
                entropias.append(self.entropia(atributo))
            print(entropias, atri)
        return atri[np.argmin(entropias)]
        


ic = ArbolID3()
#for atributo in dftrain.columns:
#    ic.entropia(atributo)
print(ic.seleccionaMejorAtributo(dftrain))
#entropia('anxiety')
#entropiaDelDataSet("prognosis")
#print(dftrain.columns)
