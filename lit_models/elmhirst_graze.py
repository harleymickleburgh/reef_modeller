#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 11:28:05 2023

@author: kl909
"""
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# parameters
r = 0.55 # growth
d = 0.24 # mortality
a = 0.1 # overgrowth of coral by M
s = 0.005 # coral recruitment
g = 0.2 #grazing 0 - 0.5
y = 0.77 # M overgrowing T
e = 0.005 # algae recruitment

def elmhirst(z,t):
    """
    Setting up equations for Elmhirst et al. 


    """
    T = 1 - z[0] - z[1]
    
    growth = z[0]*(r*T)
    mortality = d*z[0]
    overgrowthM = a*z[1]*z[0]
    recruitment = s*T
    dCdt = growth - mortality - overgrowthM + recruitment
    
    movergrowingC = a*z[1]*z[0]
    grazing = z[1]*(g/(z[0]-1)) 
    MovergrowsT = y*z[1]*T
    Mrecruitment = e*T
    dMdt = movergrowingC + grazing + MovergrowsT + Mrecruitment
    
    return( dCdt, dMdt)
    
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
    ode = odeint(elmhirst, zstart, t)
    C = ode[:,0]
    M = ode[:,1]
    Cval.append(C[-1])
    Mval.append(M[-1])
    i = + 1

plt.plot(graz_pressure, Cval, graz_pressure, Mval)
plt.show()

