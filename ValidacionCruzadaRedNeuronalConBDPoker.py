# -*- coding: utf-8 -*-
"""redneuronaldesdeceroSGS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12RkIjaGdkTvi91sMtQYutOz3dL6V_oaV

RED NEURONAL CON BASE DE DATOS "POKER"

La base de datos que usare para este trabajo de red neuronal tiene el nombre de "poker" Cada registro es un ejemplo de una mano que consta de cinco jugadores.
cartas extraídas de un mazo de cartas estándar de 52. Se describe cada carta usando dos atributos (simbolo y numero en la carta), para un total de 10 predictivos atributos. y hay un ultimo atributo de clase que describe la "Mano de póker" o resultado.

1) S1 "Traje de tarjeta # 1"
      Ordinal (1-4) que representa {Corazones, picas, diamantes, tréboles}

   2) C1 "Rango de la carta # 1"
      Representación numérica (1-13) (As, 2, 3, ..., Reina, Rey)

   3) S2 "Traje de tarjeta # 2"
      Ordinal (1-4) que representa {Corazones, picas, diamantes, tréboles}

   4) C2 "Rango de la tarjeta # 2"
      Representación numérica (1-13) (As, 2, 3, ..., Reina, Rey)

   5) S3 "Traje de tarjeta # 3"
      Ordinal (1-4) que representa {Corazones, picas, diamantes, tréboles}

   6) C3 "Rango de la carta # 3"
      Representación numérica (1-13) (As, 2, 3, ..., Reina, Rey)

   7) S4 "Traje de tarjeta # 4"
      Ordinal (1-4) que representa {Corazones, picas, diamantes, tréboles}

   8) C4 "Rango de la tarjeta # 4"
      Representación numérica (1-13) (As, 2, 3, ..., Reina, Rey)

   9) S5 "Juego de cartas # 5"
      Ordinal (1-4) que representa {Corazones, picas, diamantes, tréboles}

   10) C5 "Rango de la tarjeta 5"
      Representación numérica (1-13) (As, 2, 3, ..., Reina, Rey)

   11) CLASE "Mano de Poker"
      Ordinal (0-9)

      0: nada en mano; no es una mano de póker reconocida
      1: un par; un par de rangos iguales dentro de cinco cartas
      2: dos pares; dos pares de rangos iguales dentro de cinco cartas
      3: Tres de un tipo; tres rangos iguales dentro de cinco cartas
      4: recto; cinco cartas, clasificadas secuencialmente sin espacios
      5: rubor; cinco cartas con el mismo palo
      6: casa llena; par + diferente rango tres de un tipo
      7: Cuatro de un tipo; cuatro rangos iguales dentro de cinco cartas
      8: escalera de color; recta + ras
      9: Escalera real; {As, Rey, Reina, Jack, Diez}

# Metodología propuesta para desarrollar el taller

El objetivo de este taller es implementar un algoritmo de inteligencia computacional que permita realizar el ejercicio de clasificación de la base de datos asignada, puntualmente se pide mostrar de forma detallada cinco pasos o iteraciones por los cuales atraviese la máquina de aprendizaje seleccionada, evidenciando un mejor desempeño entre una implementación y la siguiente. 

En este taller se utilizaron las Redes Neuronales Artificiales como máquina de aprendizaje para desarrollar el ejercicio propuesto. Inialmente se realizó la preparación de los datos y posteriormente se propuso una primera arquitectura base, la cual fue incrementando su desempeño a medida que se implementaron las cinco itereaciones. Finalmente y de forma adicional, se propuso una segunda arquitectura, la cual presentó un desempeño similar a la primera arquitectura, utilizando la selección de características.

El desarrollo completo y detallado mensionado anterimente, se presenta a continuación:

# Preparación de los datos

Los siguientes fueron los pasos realizados en la importación y preparación previo al proceso de clasificación mediante las técnicas propuestas:

- Importación de librerias 
- Importación de la base de datos Online
- Verificación de datos faltantes o corruptos
- Separación de base datos por clases
- Cambio de formato a tipo numpy
- Formateo salidas a forma vectorial binarizada

### Importación de librerias 

Inicialmente se importaron las librerias "itertools", "numpy", "pandas", "sklearn" y "matplotlib".
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

"""### Importación de la base de datos Online

Se realizó la importación de la base de datos desde la URL "http://archive.ics.uci.edu/ml/machine-learning-databases/poker/poker-hand-training-true.data", indicando que es un archivo .CSV, el cual esta separado por comas (,) y que no posee una cabecera (para no perder el primer dato).
"""

DatasetName = "http://archive.ics.uci.edu/ml/machine-learning-databases/poker/poker-hand-training-true.data"
Data = pd.read_csv(DatasetName, sep=',', header=None)

#DatasetName = 'newThyroid.csv'
#Data = pd.read_csv(DatasetName, sep=',')

#Data.head(100)

#Data.describe()

Data

"""### Separación de base datos por clases

Se realizó la separación de la base de datos en tres arreglos distintos, uno para cada clase y se calculo el numero de muestras para cada clase, calculando el aporte porcentual de cada clase en la base de datos, observando una base de datos desbalanceada, distribuida de la sigueinte forma:

 - 0: nada en mano; no es una mano de póker reconocida
 - 1: un par; un par de rangos iguales dentro de cinco cartas
 - 2: dos pares; dos pares de rangos iguales dentro de cinco cartas
 - 3: Tres de un tipo; tres rangos iguales dentro de cinco cartas
 - 4: recto; cinco cartas, clasificadas secuencialmente sin espacios
 - 5: rubor; cinco cartas con el mismo palo
 - 6: casa llena; par + diferente rango tres de un tipo
 - 7: Cuatro de un tipo; cuatro rangos iguales dentro de cinco cartas
 - 8: escalera de color; recta + ras
 - 9: Escalera real; {As, Rey, Reina, Jack, Diez}
"""

## Número de muestras por clase
NumSamples = Data.shape[0]

## Filtrando muestras por clase
dataClass0 = Data.loc[Data[:][10]==0]
dataClass1 = Data.loc[Data[:][10]==1]
dataClass2 = Data.loc[Data[:][10]==2]
dataClass3 = Data.loc[Data[:][10]==3]
dataClass4 = Data.loc[Data[:][10]==4]
dataClass5 = Data.loc[Data[:][10]==5]
dataClass6 = Data.loc[Data[:][10]==6]
dataClass7 = Data.loc[Data[:][10]==7]
dataClass8 = Data.loc[Data[:][10]==8]
dataClass9 = Data.loc[Data[:][10]==9]


## Número de muestras por clase
NumSamplesClass0 = dataClass0.shape[0]
NumSamplesClass1 = dataClass1.shape[0]
NumSamplesClass2 = dataClass2.shape[0]
NumSamplesClass3 = dataClass3.shape[0]
NumSamplesClass4 = dataClass4.shape[0]
NumSamplesClass5 = dataClass5.shape[0]
NumSamplesClass6 = dataClass6.shape[0]
NumSamplesClass7 = dataClass7.shape[0]
NumSamplesClass8 = dataClass8.shape[0]
NumSamplesClass9 = dataClass9.shape[0]


## Imprimiendo resultados
print('Número de muestras totales: ', NumSamples)
print('Número de muestras por clase 0: ',NumSamplesClass0,' (',100*NumSamplesClass0/NumSamples,' %)')
print('Número de muestras por clase 1: ',NumSamplesClass1,' (',100*NumSamplesClass1/NumSamples,' %)')
print('Número de muestras por clase 2: '+str(NumSamplesClass2)+' ('+str(round(100*NumSamplesClass2/NumSamples))+' %)')
print('Número de muestras por clase 3: ',NumSamplesClass3,' (',100*NumSamplesClass3/NumSamples,' %)')
print('Número de muestras por clase 4: ',NumSamplesClass4,' (',100*NumSamplesClass4/NumSamples,' %)')
print('Número de muestras por clase 5: ',NumSamplesClass5,' (',100*NumSamplesClass5/NumSamples,' %)')
print('Número de muestras por clase 6: ',NumSamplesClass6,' (',100*NumSamplesClass6/NumSamples,' %)')
print('Número de muestras por clase 7: ',NumSamplesClass7,' (',100*NumSamplesClass7/NumSamples,' %)')
print('Número de muestras por clase 8: ',NumSamplesClass8,' (',100*NumSamplesClass8/NumSamples,' %)')
print('Número de muestras por clase 9: ',NumSamplesClass9,' (',100*NumSamplesClass9/NumSamples,' %)')

"""### Cambio de formato a tipo numpy

Se realizó el cambio del tipo de datos a tipo numpy, ya actualmente se tienen los datos en tipo "DataFrame" y es el tipo "numpy" el que se utilizará con las máquinas de aprendizaje.

Posterioemente se separaron los datos de entrada y salidas del sistema, denominados "X" para las entradas (columnas 0 a 9) y "Y" para la salida (columna 10).
"""

## Cambio de datos a tipo numpy
DataAsNumpy = np.concatenate((dataClass0.values, dataClass1.values, dataClass2.values, dataClass3.values, dataClass4.values, dataClass5.values, dataClass6.values, dataClass7.values, dataClass8.values, dataClass9.values), axis=0)

#X = DataAsNumpy[:,(2,5)] 
X = DataAsNumpy[:,0:9]
Y = DataAsNumpy[:,10]


print(X.shape)
print(Y.shape)

print(X)

"""### Formateo salidas a forma vectorial binarizada

Finalmente se realizó el cambio del vector de salida "Y" para que presente un comportamiento vectorial y binarizado compuesto por tres columnas donde cada columna corresponde a cada una de las clases, como se ejemplifica a continuación:

- Y antes: "0" - Y después: "[1 0 0 0 0 0 0 0 0 0]"
- Y antes: "1" - Y después: "[0 1 0 0 0 0 0 0 0 0]"
- Y antes: "2" - Y después: "[0 0 1 0 0 0 0 0 0 0]"
- Y antes: "3" - Y después: "[0 0 0 1 0 0 0 0 0 0]"
- Y antes: "4" - Y después: "[0 0 0 0 1 0 0 0 0 0]"
- Y antes: "5" - Y después: "[0 0 0 0 0 1 0 0 0 0]"
- Y antes: "6" - Y después: "[0 0 0 0 0 0 1 0 0 0]"
- Y antes: "7" - Y después: "[0 0 0 0 0 0 0 1 0 0]"
- Y antes: "8" - Y después: "[0 0 0 0 0 0 0 0 1 0]"
- Y antes: "9" - Y después: "[0 0 0 0 0 0 0 0 0 1]"

En este punto ya se tiene la base de datos pre-procesada y lista para aplicar los algoritmos de aprendizaje automático.
"""

print(Y.tolist())

## Formateando las salidas de Y a forma vectorial binarizada
lb = preprocessing.LabelBinarizer()
lb.fit([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
print('Salida Y Antes: ', Y.shape)
print(Y)
print("")
Y = lb.transform(Y)
print('Salida Y Después: ', Y.shape)
print(Y)

print(type(Y))
print(Y.shape)

type(Y)

"""## Implementación del clasificador base
La arquitectua base implementada fue:

    - Algoritmo optimización: adam
    - Capas ocultas: 2
    - Función de activación: logistic
    - Neuronas por capa oculta: 100
    - Máximas iteraciones: 5000
    
Utilizando esta arquitectura se obtuvo un desempeño de: 0.557 (+/- 0.287)
"""

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
max_iter = 5000

#Construcción de la RNA con base en la arquitectura definida
clf = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, max_iter=max_iter, alpha=0.0001, activation=activation,
                     solver=solver, verbose=10,  random_state=21,tol=0.000000001)

#Entrenamiento y validación cruzada
scores = cross_val_score(clf, X, Y, cv=4)

#Resultados de la validación cruzada
print("Resultados Validaciones Cruzadas:")
print(scores)
print(" ")
#Resultado Final (Promedio resultados validación cruzada)
print("Resultado Promedio Final - Clasificador Base")
print("%0.3f (+/- %0.3f)" % (scores.mean(), scores.std() * 2))

"""## La segunda implementación del clasificador base
La 2 arquitectua implementada fue:

    - Algoritmo optimización: adam
    - Capas ocultas: 3
    - Función de activación: logistic
    - Neuronas por capa oculta: 100
    - Máximas iteraciones: 2000
    
Utilizando esta arquitectura se obtuvo un desempeño de: 0.086  (+/ 0.29)
"""

#Algortimo para resolver optimización del entrenamiento
#solver = 'sgd'
solver = 'adam'

#Número de Capas Ocultas '2' y Neuronas por Capa'100' 
hidden_layer_sizes=(100, 100,100)

#Función de activación
activation = 'logistic'
#activation = 'tanh'

#Máximo número de iteraciones para entrenamiento
#max_iter = 50
max_iter = 2000

#Construcción de la RNA con base en la arquitectura definida
clf = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, max_iter=max_iter, alpha=0.0001, activation=activation,
                     solver=solver, verbose=10,  random_state=21,tol=0.000000001)

#Entrenamiento y validación cruzada
scores = cross_val_score(clf, X, Y, cv=4)

#Resultados de la validación cruzada
print("Resultados Validaciones Cruzadas:")
print(scores)
print(" ")
#Resultado Final (Promedio resultados validación cruzada)
print("Resultado Promedio Final - Clasificador Base")
print("%0.3f (+/- %0.3f)" % (scores.mean(), scores.std() * 2))

"""#EL HISTORICO DE ARQUITECTURAS IMPLEMENTADAS Y SUS RESPECTIVAS CONCLUSIONES:
adam, 100,100,100 .  Logistic. Max = 1100

[0  0.0020  0  0.34]

0.086  (+/ 0.29)

Conclusion : teniendo en cuenta que son 25000 datos la cantidad maxima de iteraciones 1100 es muy poco para lograr algo optimo

---------------------------------------------
adam, 100,100,100 .  Logistic. Max = 2000

[0  0.0020  0  0.34]

0.086  (+/ 0.29)

Conclusion : La cantidad maxima de iteraciones sigue siendo muy poca con 2000

---------------------------------------------
adam 100,100,100,100,100 Logistic Max 1000

[0.    0.0020 0.    0.]

0.001 (+/- 0.002) 

Conclusion : Intente poniendo mas capas ocultas entre las neuronas de entrada y de salida y el resultado fue menor porcentaje de optimizacion

---------------------------------------------
adam 100,100,100,100,100 Logistic Max 1000

[0.       0.002079 0.       0. ]

0.001 (+/- 0.002)

Conclusion : Intente poniendo mas capas ocultas entre las neuronas de entrada y de salida y el resultado fue menor porcentaje de optimizacion

---------------------------------------------
adam 100,100 Logistic Max 5000

[0.75355829 0.63153686 0.39363404 0.44881638]

0.557 (+/- 0.287)

Conclusion : teniendo en cuenta las conclusiones anteriores intente con un numero menor de capas ocultas 2 de 100 neuronas cada una y una cantidad de interacciones maximas de 5000 y esta arquitectura me dio el mayor porcentaje

---------------------------------------------
adam 100,100 Logistic Max 10000

[0.75355829 0.63153686 0.39363404 0.44881638]

0.557 (+/- 0.287)

Conclusion: En esta oportunidad intente incrementar el doble las interacciones maximas llegando a 10000 y me dio un resultado identico a si tuviera 5000 iteraciones maximas.

---------------------------------------------
adam 100 Logistic Max 10000

[0.58100112 0.46473693 0.16682662 0.41410749]

0.407 (+/- 0.302)

Conclusion = En esta oportunidad deje el maximo de iteraciones en 10000 y baje la cantidad de capas ocultas a 1 lo cual me dio un menor porcentaje de optimizacion de cuando se tienen 2 capas ocultas

---------------------------------------------
adam 30 Logistic Max 5000

[0.31376939 0.36206621 0.05134357 0.15259117]

0.220 (+/- 0.249)

Conclusion : Teniendo en cuenta que me daba el mismo resultado si dejaba 10000 iteraciones maximas a si dejaba 5000 iteraciones maximas intente con 1 sola capa oculta y 30 neuronas en ella y me dio un porcentaje menor

---------------------------------------------
adam 1000 Logistic Max 5000

[0.52534783 0.5106349  0.24136276 0.41730646]

0.424 (+/- 0.226)
"""

