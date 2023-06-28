#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 13:58:34 2023

@author: kl909
"""
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt


a = 0.1 #overgrowth
g = 0.5 #0 - 0.5; grazing
y = 0.77 #growth rate
r = 0.55 #recruitment
d = 0.24 #mortality

def mumby(z,t):

     
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
  

# grazing pressure
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
    ode = odeint(mumby, zstart, t)
    C = ode[:,0]
    M = ode[:,1]
    Cval.append(C[-1])
    Mval.append(M[-1])
    i = + 1
    
    #Cval = C[-1]
   # Tval = T[-1]
#print(Cval, Tval, Mval)
# for each value of theta, collect the result of C at t 250 and result of T at t 250
# array for result of C at t 250
    # array for T at t 250
    # store result in new array
    
plt.plot(graz_pressure, Cval, graz_pressure, Mval)
plt.show()