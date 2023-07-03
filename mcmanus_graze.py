#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 16:18:02 2023

@author: kl909
"""
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

#params
r = 0.55#growth
d = 0.24# mortality 0.02 - 1.0
a = 0.1# coral overgrowth
f = 10 # no. of larvae per meter per year
s = 0.01# area of newly settled recruit
g = 0.4# grazing (use fung?)
y = 0.77 # turf overgrowth
w = 0.005 # spawning larvae (use lsc from fung?)

#### THIS DOESN'T CONTAIN THE EXTERNAL LARVAE EQUATION OR THE GRAZING AS FUNCTION OF CORAL EQUATION

def mcmanus(z,t):
    F = 1 - z[0] - z[1]
    
    growth = (r*F) * z[0]
    mortality = d*z[0]
    movergrowsc = a*z[0]*z[1]
    recruitment = (f*s + w)*F
    dCdt = growth - mortality - movergrowsc + recruitment
    
    mmovergrowsc = a*z[0]*z[1]
    grazing = g*z[1]
    movergrowst = y*z[1]*F
    dMdt = mmovergrowsc - grazing + movergrowst
   
    return[dCdt, dMdt]

zstart = [0.8, 0.2]

graz_pressure = np.arange(0.05, 0.7, 0.05) 
Cval = []
Mval = []
#t = np.linspace(0,250)
i = 0


# intial conditons
for point in graz_pressure:
    zstart = [0.8, 0.2]
    t = np.linspace(0,500, num = 500)
    g = point
    ode = odeint(mcmanus, zstart, t)
    C = ode[:,0]
    M = ode[:,1]
    Cval.append(C[-1])
    Mval.append(M[-1])
    i = + 1

plt.plot(graz_pressure, Cval, graz_pressure, Mval)
plt.show()
