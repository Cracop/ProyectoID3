import pandas as pd
import numpy as np
import itertools
import math

ycol = 'prognosis'
dftrain = pd.read_csv('Testing.csv')
y_train = dftrain[ycol] 

valores = y_train.unique()
#print(dftrain.head())

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
        entropia += proba1*(-1*n)
    print(atributo, entropia)

        
        
        



entropia('itching')

    

"""



  def entropy(self, attribute_column):
    # find unique values and their frequency counts for the given attribute
    values, counts = np.unique(attribute_column, return_counts=True)

    # calculate entropy for each unique value
    entropy_list = []

    for i in range(len(values)):
      probability = counts[i]/np.sum(counts)
      entropy_list.append(-probability*np.log2(probability))

    # calculate sum of individual entropy values
    total_entropy = np.sum(entropy_list)

    return total_entropy

class Nodo:
    def __init__(self):
        self.valor = None
        self.sig = None
        self.hijos = None
        self.padre = None"""