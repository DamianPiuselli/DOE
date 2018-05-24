# -*- coding: utf-8 -*-
"""
Created on Wed May 23 15:47:55 2018

@author: damian
"""
from pyDOE import ccdesign
import numpy as np

def ccd(n, MAX, MIN):
    
#modelo ccd rotable centrado en 0,0 de dimension n
    model = ccdesign(n,face='cci', alpha='r')  
        
# Escalado del modelo  con A la coordenada escalada y B la coordenada sin escalar.
#
# Ax - Amin   Bx - -1
#---------- = ---------
# Amax-Amin   2 
#
#
#      (Bx - -1) x (Amax-Amin)
# Ax = -----------                + Amin
#      2

    scaledmodel = ((model + 1)/2) * (np.subtract(MAX, MIN)) + MIN
    print(scaledmodel.shape)
    print(scaledmodel)
    return scaledmodel 

asd= ccd(5, (100,100,100,100,100), (50,50,50,50,50))
