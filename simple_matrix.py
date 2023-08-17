#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 14:15:34 2023

@author: kl909
"""

import greiner
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

num_sites = 3
n_years = 5

#create coral objects 
corals = []

for n in range(0,num_sites):
    corals.append(greiner.greiner()) #what did this do?
   
#set up matrix
c_matrix = np.loadtxt("matrix_practice.csv",
                      delimiter=",", dtype=float)
#display(c_matrix)
np.shape(c_matrix)

# prep lsc calculations
p_m = 1 
r_area = 4.08/10000. #cm^2 area of settled recruit (fung appendix B)

# lists to hold final outputs for coral and macroalgae
lastC = []
lastM = []
times = []
times.append(0)


# set up starting conditions
for c in corals:
    c.set_start_conditions([0.1,0.1])
    lastC.append(0.1)
    lastM.append(0.1)   


for year in range(0,n_years):
     lsc_new = [] # list to hold updated lsc value
     times.append(year)
     for sink in range(0,num_sites): 
        Pl = 0
        for source in range(0,num_sites):
            #print(c_matrix[source])
            #begin calculating lsc
            Pl = Pl + (lastC[source] * p_m * r_area * c_matrix[sink][source]) 
        N = Pl * corals[sink].parameters["d"]
        T = 1 - lastC[sink] - lastM[sink]
        lsc_new.append((N * r_area) / T)

     
     #now solve ode using new lsc
     
     for c in range(0,num_sites):
          #update lsc from above calculation
          corals[c].set_parameter("lsc", float(lsc_new[c])) # set lsc in regard to the other reefs
          corals[c].set_times([year,year+1])
          corals[c].solve_time() #ode solver
          #print(corals[c].output[1,:])
          corals[c].set_start_conditions(corals[c].output[1,:].tolist())
          lastC[c] = corals[c].output[1,0]
          lastM[c] = corals[c].output[1,1]
     #print(lastC)
     #print(lastM)
     #reshape the 1D arrays into 2D arrays
     np.reshape(lastC, (-1,3))
     #np.reshape(lastM, (-1,3))
     print(lastC)
     #print(lastM)          

     times.pop(0)
     #print(times)
# create 3 arrays:

# time = 1D array (like: [1, 2, 3, 4, 5]
# corals = 2D array:
#   0.1   0.23
#   0.1   0.23
#   ...   ..
#   0.23  0.23
# columns are same length as time, each column is a different site.
# macros is the same structure as corals.


     fig_summary=plt.figure(figsize=(12.0,6),dpi=360)
     ax=fig_summary.add_subplot(111)
     colours = ['#377eb8', '#ff7f00', '#4daf4a',
            '#a65628', '#984ea3', '#f780bf',
              '#999999', '#e41a1c', '#dede00']

     

# # loop over sites, plot the coral and macro lines for each site, looping over colours
     # for c in range(0,2):
     #     ax.plot(times, lastC[c][:], label="Reef "+str(c)+" Coral", color=colours[c])
    
    
     #     ax.plot(times, lastM[c][:], label="Reef "+str(c)+" Macro", linestyle="--", color=colours[c])
    

     # plt.show()


     

     
     


    