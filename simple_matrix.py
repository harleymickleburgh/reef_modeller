#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 14:15:34 2023

@author: kl909
"""

import greiner
import numpy as np

num_sites = 3
n_years = 1

#create coral objects 
corals = []
print(corals)


#names = ["Bob", "Fred"] # this will be for a dictionary holding the names of the reefs and their coral cover later on 

for n in range(0,num_sites):
    corals.append(greiner.greiner()) #what did this do?
   


#set up matrix
c_matrix = np.loadtxt("matrix_practice.csv",
                      delimiter=",", dtype=float)
#display(c_matrix)
np.shape(c_matrix)
#c_matrix = [[1,2,3],[4,5,6],[7,8,9]]
#c_matrix = np.identity(2)
#print(c_matrix)

# prep lsc calculations
p_m = 1 
r_area = 4.08/10000. #cm^2 area of settled recruit (fung appendix B)

# lists to hold final outputs for coral and macroalgae
lastC = []
lastM = []

# set up starting conditions
for c in corals:
    c.set_start_conditions([0.1,0.1])
    lastC.append(0.1)
    lastM.append(0.1)


for year in range(0,n_years):
     lsc_new = [] # list to hold updated lsc value
     for sink in range(0,num_sites): 
        Pl = 0
        for source in range(0,num_sites):
            #print(c_matrix[source])
            #begin calculating lsc
            Pl = Pl + (lastC[source] * p_m * r_area * c_matrix[sink][source]) 
        N = Pl * corals[sink].parameters["d"]
        T = 1 - lastC[sink] - lastM[sink]
        lsc_new.append((N * r_area) / T)
     #print(year)
     print(range(num_sites))
     for c in range(0,num_sites):
          #update lsc from above calculation
          corals[c].set_parameter("lsc", float(lsc_new[c]))
          corals[c].set_times([year,year+1])
          corals[c].solve_time() #ode solver
          #print(corals[c].output[1,:])
          corals[c].set_start_conditions(corals[c].output[1,:].tolist())
          lastC[c] = corals[c].output[1,0]
          lastM[c] = corals[c].output[1,1]
          #print(lastC)
         # print(lastM)

    # R1.set_parameter("lsc", c_matrix[0,0])
    # ode()
    # R1.solve_time(i, i+1)
    
