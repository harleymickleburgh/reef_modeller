#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:29:01 2023

@author: kl909
"""

import greiner
import numpy as np

num_years = 5
num_sites = 2

reefs = {}
reefs["reef_1"] = [0.8, 0.1]
reefs["reef_2"] = [0.8, 0.1]


start = []
for value in reefs.values():
    start = [value]
    start.append(start[0])
    
print(start)


for year in range(0, num_years):
    lsc_new = []
    mlsc_new = []
    for key in reefs.items():
        if key == "reef_1":
            lsc = reefs.parameters["lsc"] * reefs["reef_2"][0]
            lsc_new.append(lsc)
            mlsc = reefs.parameters["mlsc"] * reefs["reef_2"][1]
            mlsc_new.append(mlsc)
            start = (start[0])
            reefs[key].set_parameter("lsc", lsc_new[key])
            reefs[key].set_parameter("mlsc", float(mlsc_new[key]))
        if key == "reef_2":
            lsc = reefs.parameters["lsc"] * reefs["reef_1"][0]
            lsc_new.append(lsc)
            mlsc = reefs.parameters["mlsc"] * reefs["reef_1"][1]
            mlsc_new.append(mlsc)
            start = (start[1])
            reefs[key].set_parameter("lsc", lsc_new[key])
            reefs[key].set_parameter("mlsc", float(mlsc_new[key]))
            
            
    for c in range(0,num_sites):    ### help
        reefs[c].set_times([year,year+1])
        reefs[c].solve_time() #ode solver
        #print(corals[c].output[1,:])
        reefs[c].set_start_conditions(start)
                                      
                                      
        reefs[c].set_start_conditions(reefs[c].output[1,:].tolist()) # this needs changing???
        
        # add new populations to dictionary 
        for value in reefs.values():
            value.append(output)
            
            
            
            
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



