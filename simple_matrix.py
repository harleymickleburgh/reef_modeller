#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 14:15:34 2023

@author: kl909
"""

import greiner
import numpy as np

num_sites = 2
n_years = 10

#create coral objects 
corals = []



#names = ["Bob", "Fred"] # this will be for a dictionary holding the names of the reefs and their coral cover later on 

for n in range(0,num_sites):
    corals.append(greiner.greiner())
    
print(corals)


#set up matrix
#c_matrix = np.zeros((num_sites,num_sites))
c_matrix = np.identity(2)
#print(c_matrix)

# prep lsc calculations
p_m = 1 
r_area = 4.08/10000. #cm^2 area of settled recruit (fung appendix B)


lastC = []
lastM = []

# set up starting conditions
for c in corals:
    c.set_start_conditions([0.1,0.1])
    lastC.append(0.1)
    lastM.append(0.1)


for year in range(0,n_years):
     lsc_new = []
     for sink in range(0,num_sites):
        Pl = 0
        for source in range(0,num_sites):
            Pl = Pl + (lastC[source] * p_m * r_area * c_matrix[source,sink]) # which bit of the matrix? also is C z[0] or the corals matrix?
        N = Pl * corals[sink].parameters("d") # don't know how to import the parameter
        #set up calculation for lsc from other reefs
        lsc_new.append((N * r_area) / T)
     print(year)
     for c in range(0,num_sites):
         #update lsc from above calculation
         corals[c].set_parameter("lsc", lsc_new[c])
         corals[c].set_times([year,year+1])
         corals[c].solve_time()
         print(corals[c].output[1,:])
         corals[c].set_start_conditions(corals[c].output[1,:].tolist())
         lastC[c] = corals[c].output[1,0]
         lastM[c] = corals[c].output[1,1]

 #    R1.set_parameter("lsc", c_matrix[0,0])
 #    ode()
 #    R1.solve_time(i, i+1)
    
