#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 14:11:11 2023

@author: kl909
"""
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot

class ModelName:
    def __init__(self, name):
        self.name = name

class mumby(ModelName):
    
    def ode(z,t):
        a = 0.1 #overgrowth
        g = 0.5 #0 - 0.5; grazing
        y = 0.77 #growth rate
        r = 0.55 #recruitment
        d = 0.24 #mortality
     
        T = 1 - z[0] - z[1]
         
             #coral (z(1))
        recruitmentC = r*T*z[0]
        mortalityC = d*z[0]
        Movergrowth = a*z[1]*z[0]
        dCdt = recruitmentC - mortalityC - Movergrowth
        
        # macroalgae (z(2))
        MMovergrowth = a*z[1]*z[0]
        grazing = (g*z[1]) / (z[1] + T)
        growthM = y*z[1]*T
        dMdt = MMovergrowth - grazing + growthM
    
        return[dCdt, dMdt]
       
zstart = [0.8, 0.2]

t = np.linspace(0,500, num = 500)

x = odeint(mumby, zstart, t)
C = x[:,0]
M = x[:,1]

# plot the results
plt.plot(t, C)
plt.plot(t, M)
plt.ylim(0,1)
plt.xlim(-1)
plt.show()       
