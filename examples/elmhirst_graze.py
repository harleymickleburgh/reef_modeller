#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 11:28:05 2023

@author: kl909
"""
import sys
sys.path.insert(0,"../")
import numpy as np
import matplotlib.pyplot as plt
import reef_modeller.elmhirst
from scipy.optimize import fsolve



parameters = {
    # parameters
    "r" : 0.55, # growth
    "d" : 0.24, # mortality
    "a" : 0.1,  # overgrowth of coral by M
    "s" : 0.005,# coral recruitment
    "g" : 0.2,  # grazing 0 - 0.5
    "y" : 0.77, # M overgrowing T
    "e" : 0.000 # algae recruitment
}

coralModel = reef_modeller.elmhirst.elmhirst()

graz_pressure = np.arange(0.05, 0.55, 0.05) 


# intial conditons
zstart = [0.1, 0.6]
coralModel.set_parameters(parameters)
corals = []
algae = []
for g in graz_pressure:
    coralModel.set_start_conditions(zstart)        
    coralModel.set_parameter("g",g)
    eq = fsolve(coralModel.ode, zstart, args=(0))
    print(eq)
    corals.append(eq[0])
    algae.append(eq[1])
    

fig, ax = plt.subplots()
ax.plot(graz_pressure, corals, label="Coral", color=coralModel._coral_colour)
ax.plot(graz_pressure, algae, label="Algae", color=coralModel._malgae_colour)

ax.set(xlabel='Grazing', ylabel='Perc Cover')
ax.grid()

plt.show()
