#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 20:26:06 2018

@author: damian
"""

from pyDOE import *
import pandas as pd
from pandas import DataFrame
import numpy as np


#  central composite design =   F + C + E
# F: matriz de los elementos del modelo factorial, +1 -1
# C: matriz de los puntos centrales, replicados m veces, default 5
# E: matriz de los puntos axiales, 2*k elementos, +alpha - alpha
#    alpha = (numero de elementos de la matriz F)^1/4 para que sea rotable

n = 5   #nro de factores
m = 5   #nro de replicados del centro
v = 8  # nro de muestras para  validacion (latin hypercube)
filename = 'ccd-incoloy'  #nombre del archivo a generar
header = ['Cr ppm', 'Ni ppm','Fe ppm','Co ppm','B ppm'] # nombre y unidades de los analitos, en el orden adecuado

######## Cr , Ni, Fe , Co, B   (analitos, en ppm)
A_MAX = (200,450,500,0.340,0.060) #limite superior de concentracion
A_MIN = (100,190,220,0.050,0.020)  #limite inferio de concentracion


# Calculo de la matriz F - Usando un modelo factorial FRACCIONAL!
# el modelo tiene resolucion tipo V,  generador I = ABCDE

F = fracfact('a b c d abcd')
nF = len(F)

#Calculo de la matriz E, alpha de modo que sea rotable.
alpha = nF**0.25
E_pos = np.zeros((n,n),float)
np.fill_diagonal(E_pos, alpha)  #Convierto a E_pos en una matriz diagonal de +alpha
E_neg = -E_pos # Ejes negativos, por simetria.
E = np.concatenate((E_pos,E_neg)) #uno las matrices para generar E.

#Calculo de la matriz C
C = np.zeros((n,m), float)

#Finalmente
ccd_unscaled = np.concatenate((F,E,C))

# Se escala el modelo para pasarlo a concentraciones.
# los vectores MAX y MIN definen el rango de concentraciones de cada iesimo componente
#
# Ax-Amin   Bx-Bmin
#-------- = -------    ===>    Ax = Amin + (Amax-Amin)*(Bx-Bmin) / (Bmax-Bmin)
#Amax-Amin  Bmax-Bmin
#
# Bmax es +alpha y Bmin -alpha ==> (Bmax-Bmin) = 2*alpha
#

ccd = ((ccd_unscaled+alpha)*np.subtract(A_MAX,A_MIN)/(2*alpha))+A_MIN

# El set de validacion se genera con un set randomizado (latin-hypercube) centermaximin, para que no alla clusters.
val_unscaled = lhs(n,samples=v,criterion='centermaximin')
val = ((val_unscaled)*np.subtract(A_MAX,A_MIN)/(1))+A_MIN
df_val = pd.DataFrame(val, columns=header)

# convirtiendo en un dataframe y exportando a excel-

df_ccd = pd.DataFrame(ccd, columns=header)

writer = pd.ExcelWriter(filename+'.xlsx')
df_ccd.to_excel(writer,'Sheet1',index=False)
df_val.to_excel(writer,'Sheet2',index=False)
writer.save()