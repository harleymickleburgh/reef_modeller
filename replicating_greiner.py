#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:29:01 2023

@author: kl909
"""

import greiner
import numpy as np

num_years = 5

reefs = {}
reefs["reef_1"] = [0.8, 0.2]
reefs["reef_2"] = [0.8, 0.2]


start = []
for value in reefs.values():
    start = [value]
    start.append(start)
    #print(start[0])
    #value.set_start_conditions((start[0]))


for year in range(0, num_years):
    lsc_new = []
    mlsc_new = []
    for key in reefs.items():
        if key == "reef_1":
            lsc = reefs["reef_2"][0]
            lsc_new.append(lsc)
            mlsc = reefs["reef_2"][1]
            mlsc_new.append(mlsc)
        if key == "reef_2":
            lsc = reefs["reef_1"][0]
            lsc_new.append(lsc)
            mlsc = reefs["reef_1"][1]
            mlsc_new.append(mlsc)
        reefs[key].set_parameter("lsc", float(lsc_new[key]))
        reefs[key].set_parameter("mlsc", float(mlsc_new[key]))
        reefs[key].set_times([year,year+1])
        reefs[key].solve_time() #ode solver
        #print(corals[c].output[1,:])
        reefs[key].set_start_conditions(reefs[key].output[1,:].tolist())
            
            
            
            
 #    if reef value = reef 1, lsc = reef 2 value [0]
 #        and mlsc = reef 2 value [1]
 #     else
 #         lsc = reef 1 value [0]
 # and mlsc = reef 1 value [1]
 
 #     update the population in reefs for each reef
 #     = new start condition
     
     
    

#start conditions is a list 


#for y in num_years:
#     coralModel.set_start_conditions(start)
    
    
    

# reef 1 lsc = lsc * reef 2 coral
# reef 1 mlsc = mlsc * reef 2 algae

# reef 2 lsc = lsc * reef 1 coral
# reef 1 mlsc = mlsc * reef 1 algae

# save reef 1 coral cover
# save reef 1 algae cover

# save reef 2 coral cover
# save reef 2 algae cover



