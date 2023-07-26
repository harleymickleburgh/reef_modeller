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

#names = ["Bob", "Fred"]

for n in range(0,num_sites):
    corals.append(greiner.greiner())
    
print(corals)


#set up matrix
#c_matrix = np.zeros((num_sites,num_sites))
c_matrix = np.identity(2)
print(c_matrix)

# set up starting conditions
for c in corals:
    c.set_start_conditions([0.1,0.1])

for year in range(0,n_years):
     #c.set_parameter("lsc", 0.6)
     print(year)
     for c in corals:
         c.set_parameter("lsc", 0.6)
         c.set_times([year,year+1])
         c.solve_time()
         print(c.output[1,:])
         c.set_start_conditions(c.output[1,:].tolist())
 #    R1.set_parameter("lsc", c_matrix[0,0])
 #    ode()
 #    R1.solve_time(i, i+1)
    