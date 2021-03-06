# -*- coding: utf-8 -*-
"""Parcial3SistemasExpertosBDtriqui.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EaPbnB0wrqLXFe3h6EIpWLH1XkUzrbRD

**BASE DE DATOS TRIQUI O TRES EN LINEA**

Esta base de datos esta codificada para almacenar las posibles configuraciones de una tabla de triqui al final de cada juego.

DESCRIPCION DEL JUEGO:

La cantidad de atributos de entrada son 9, estas variables son espacios en el triqui los 3 primeros en la fila superior, los siguientes 3 en la fila del medio y los ultimos 3 en la fila inferior del triqui.

Cada jugador tiene un turno para escoger un espacio y la forma de ganar en este juego es lograr seleccionar 3 espacios consecutivos en forma de fila, de columna o en diagonal.

Cuando X gana la variable numero 10 que es de salida imprime = "verdadero"

Cuando O gana la variable numero 10 que es de salida imprime = "Falso" 

Número de instancias: 958 (tableros legales de final de juego de tres en raya)

la X gana el 65.3%. El O gana el 34.7%.

***Importacion de librerias***
"""

import itertools
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from sklearn.svm import SVC
from sklearn.metrics import precision_score

"""***Interpretacion y validacion de los datos***"""

DatasetName = "https://archive.ics.uci.edu/ml/machine-learning-databases/tic-tac-toe/tic-tac-toe.data"
Data = pd.read_csv(DatasetName, sep=',', header=None)

Data

"""***Preprocesamiento***"""

# Número de muestras por clase
NumSamples = Data.shape[0]

## Filtrando muestras por clase
dataClass0 = Data.loc[Data[:][9]=="positive"]
dataClass1 = Data.loc[Data[:][9]=="negative"]



## Número de muestras por clase
NumSamplesClass0 = dataClass0.shape[0]
NumSamplesClass1 = dataClass1.shape[0]



## Imprimiendo resultados
print('Número de muestras totales: ', NumSamples)
print('Número de muestras por clase 0: ',NumSamplesClass0,' (',100*NumSamplesClass0/NumSamples,' %)')
print('Número de muestras por clase 1: ',NumSamplesClass1,' (',100*NumSamplesClass1/NumSamples,' %)')

"""***Aplicar RNA***"""

## Cambio de datos a tipo numpy
DataAsNumpy = np.concatenate((dataClass0.values, dataClass1.values), axis=0)

#X = DataAsNumpy[:,(2,5)] 
X = DataAsNumpy[:,0:8]
Y = DataAsNumpy[:,9]


X = Data.replace({"positive": 1, "negative": 0,"x": 1, "o": 0, "b":2})
Y = Data.replace({"positive": 1, "negative": 0,"x": 1, "o": 0, "b":2})


print(X.shape)
print(Y.shape)

print(X)

## Formateando las salidas de Y a forma vectorial binarizada
lb = preprocessing.LabelBinarizer()
lb.fit([0, 1])
print('Salida Y Antes: ', Y.shape)
print(Y)
print("")
Y = lb.transform(Y)
print('Salida Y Después: ', Y.shape)
print(Y)

#Algortimo para resolver optimización del entrenamiento
#solver = 'sgd'
solver = 'adam'

#Número de Capas Ocultas '2' y Neuronas por Capa'100' 
hidden_layer_sizes=(100, 100)

#Función de activación
activation = 'logistic'
#activation = 'tanh'

#Máximo número de iteraciones para entrenamiento
#max_iter = 50
max_iter = 1000

#Construcción de la RNA con base en la arquitectura definida
clf = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, max_iter=max_iter, alpha=0.0001, activation=activation,
                     solver=solver, verbose=10,  random_state=21,tol=0.000000001)

#Entrenamiento y validación cruzada
scores = cross_val_score(clf, X, Y, cv=4)

"""***Aplicacion de SVM***"""

dataset = datasets.load_breast_cancer()


#Selecciono todas las columnas
x = dataset.data

#Defino los datos de las etiquetas 
y = dataset.target

#Separo los datos entre entrenamiento y prueba 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size= 0.25, random_state = 0)

#Defino el algoritmo a utilizar
algoritmo = SVC(kernel = 'linear')

#Entrenando el modelo
algoritmo.fit(x_train, y_train)

#realizamos una prediccion
y_pred = algoritmo.predict(x_test)

#verifico la matriz de confusion
m = confusion_matrix(y_test, y_pred)
print('matriz de confusion: ')
print(m)

#calculo la precision del modelo
precision = precision_score(y_test, y_pred)
print('precision del modelo: ')
print(precision)


#Linear = 0.98
#poly = 0.90
#rbf = 0.91
#sigmoid = 0.55

"""***Aplicacion de K-Vecinos***"""

dataset = datasets.load_breast_cancer()
#print(dataset)

#Verifico la informacion contenida en el dataset
#print(dataset.keys())

#verifico que datos tiene el dataset
#print(dataset.DESCR)

#Selecciono todas las columnas
x = dataset.data

#Defino los datos de las etiquetas 
y = dataset.target


#Separo los datos entre entrenamiento y prueba 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size= 0.25, random_state = 0)

#Definición del algoritmo a utilizar - distancia euclidiana - k= 5 (marcamos 5 elementos)
algoritmo = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)

#Entreno el algoritmo
algoritmo.fit(x_train, y_train)

#Realizamos una prediccion
y_pred = algoritmo.predict(x_test)

#verifico la matriz de confusion 
m = confusion_matrix(y_test, y_pred)
print("matriz de confusion : ")
print(m)

#calcula la precision del modelo
precision = precision_score(y_test, y_pred)
print("Precision del modelo: ")
print(precision)