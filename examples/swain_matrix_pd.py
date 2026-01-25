#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 14:15:34 2023

@author: kl909
"""
import sys
sys.path.insert(0,"../")
import reef_modeller.greiner
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



#set up matrix of connectivity
c_matrix = np.loadtxt("../data/swain_matrix.csv",
                       delimiter=",", dtype=float)

c_matrix = np.divide(c_matrix,100)

# set up start conditions
# row 1 is corals
# row 2 is algae
start_conditions = np.loadtxt("../data/swain_start_noheads.csv",
                      delimiter=",", dtype=float)

start_conditions = np.divide(start_conditions,100)

num_sites = len(start_conditions[0])
n_years = 50
year1 = 2006
year2 = 2023
years = list(range(year1, year2))


#create coral objects 
corals = []
# set up starting conditions
tempM = []
tempC = []

for n in range(0,num_sites):
    corals.append(reef_modeller.greiner.greiner())

# lists to hold final outputs for coral and macroalgae
lastC = []
lastM = []
times = []


counter = 0
for c in corals:
    cpoint = float(start_conditions[0][counter])
    mpoint = float(start_conditions[1][counter])
    c.set_start_conditions([cpoint, mpoint]) # this may be very wrong, how to check?
    tempC.append(cpoint) # but these are correct
    tempM.append(mpoint)
    counter = counter+1


lastC.append(tempC)
lastM.append(tempM)


# prep lsc calculations
p_m = 1 
r_area = 4.08/10000. #cm^2 area of settled recruit (fung appendix B)


for year in range(0,n_years):
    lsc_new = [] # list to hold updated lsc value
    times.append(year)
    for sink in range(0,num_sites): 
        Pl = 0
        for source in range(0,num_sites):
            #begin calculating lsc
            Pl = Pl + (lastC[-1][source] * p_m * r_area * c_matrix[sink][source]) 
        N = Pl * corals[sink].parameters["d"]
        T = 1 - lastC[-1][sink] - lastM[-1][sink]
        lsc_new.append((N * r_area) / T)
        
        #now solve ode using new lsc
        tempC = []
        tempM = []
        #now solve ode using new lsc

    for c in range(0,num_sites):
        #update lsc from above calculation
        #print(lsc_new[c])
        corals[c].set_parameter("lsc", float(lsc_new[c])) # set lsc in regard to the other reefs
        corals[c].set_times([year,year+1])
        corals[c].solve_time() #ode solver
        #print(corals[c].output[1,:])
        corals[c].set_start_conditions(corals[c].output[1,:].tolist())
        tempC.append(corals[c].output[1,0])
        tempM.append(corals[c].output[1,1])

    lastC.append(tempC)
    lastM.append(tempM)


times.append(n_years)

# create 3 arrays:

# time = 1D array (like: [1, 2, 3, 4, 5]
# corals = 2D array:
#   0.1   0.23
#   0.1   0.23
#   ...   ..
#   0.23  0.23
# columns are same length as time, each column is a different site.
# macros is the same structure as corals.
times = np.array(times)
lastC = np.array(lastC).transpose()
lastM = np.array(lastM).transpose()

fig_summary=plt.figure(figsize=(12.0,6),dpi=180)
ax=fig_summary.add_subplot(111)
colours = ['#377eb8', '#ff7f00', '#4daf4a',
           '#a65628', '#984ea3', '#f780bf',
           '#999999', '#e41a1c', '#dede00']

     

# loop over sites, plot the coral and macro lines for each site, looping over colours
for c in range(0,num_sites):
    ax.plot(times, lastC[:][c], label="Reef "+str(c)+" Coral", color=colours[c])
    ax.plot(times, lastM[:][c], label="Reef "+str(c)+" Macro", linestyle="--", color=colours[c])
    
ax.legend()
plt.show()
