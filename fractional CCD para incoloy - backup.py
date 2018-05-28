#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 20:26:06 2018

@author: damian
"""

from pyDOE import *
import numpy as np

#  central composite design =   F + C + E
# F: matriz de los elementos del modelo factorial, +1 -1
# C: matriz de los puntos centrales, replicados m veces, default 5
# E: matriz de los puntos axiales, 2*k elementos, +alpha - alpha
#    alpha = (numero de elementos de la matriz F)^1/4 para que sea rotable

n = 5 #nro de factores
m = 5   #nro de replicados del centro
A_MAX = (960,480,144,0.5,0.5) #limite superior de concentracion
A_MIN = (240,120,36,0.05,0.05)  #limite inferio de concentracion


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