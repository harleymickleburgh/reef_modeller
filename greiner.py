#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 11:11:43 2023

@author: kl909
"""

from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

r = 0.55 # Rate coral recruits settle on turf algae (/time)
d = 0.24
a = 0.1
g = 0.77 #0.01 ≤g≤ 0.99
y = 0.77 #Rate macroalgae recruits settle on turf algae (/time)
lbc = 0.0025 # divided elmhirst value of all coral recruitment 0.005
lsc = 0.0025
mlbc = 0.0025
mlsc = 0.0025

def greiner(z,t):

     T = 1 - z[0] - z[1]
    
     growth = r*(1-lbc)*T*z[0]
     mortalityC = d*z[0]
     Movergrowth = a*z[1]*z[0]
     recruitment = r*lsc*z[0]*T
     dCdt = growth - mortalityC - Movergrowth + recruitment
    
    # macroalgae (z(2))
     MMovergrowth = a*z[1]*z[0]
     grazing = g*(z[1]*T)
     growthM1 = y*(1-mlbc)*z[1]*T
     growthM2 = y*mlsc * z[1]*T
     dMdt = MMovergrowth - grazing + growthM1 + growthM2
    
     return[dCdt, dMdt]
     
graz_pressure = np.arange(0.05, 1.0, 0.05) 
Cval = []
Mval = []
#t = np.linspace(0,250)
i = 0


# intial conditons
for point in graz_pressure:
    zstart = [0.8, 0.2]
    t = np.linspace(0,500, num = 500)
    g = point
    ode = odeint(greiner, zstart, t)
    C = ode[:,0]
    M = ode[:,1]
    Cval.append(C[-1])
    Mval.append(M[-1])
    i = + 1

plt.plot(graz_pressure, Cval, graz_pressure, Mval)
plt.show()