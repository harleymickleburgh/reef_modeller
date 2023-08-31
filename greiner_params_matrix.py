
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


########################
# set up model

#import matrix of connectivity
c_panda = pd.read_csv("con_matrix.csv", header = 0)
c_panda = c_panda.iloc[:,1:]
c_panda = c_panda.div(100)
c_matrix = c_panda.to_numpy() #convert to numpy for iterations


#import start conditions
# row 1 is corals
#row 2 is algae
start_conditions_og = pd.read_csv("swain_reef_start.csv", header = 0)
start_conditions_og = start_conditions_og.iloc[:,1:] # remove column 1
start_conditions_og = start_conditions_og.div(100) # divide numbers by 100
#convert df into list
start_conditions = []
for column in start_conditions_og.columns:
    li = start_conditions_og[column].tolist()
    start_conditions.append(li)
    
    
#import parameters for each reef
parameters = pd.read_csv("greiner_params.csv", header = 0)
parameters = parameters.iloc[:,1:]
#print(parameters)

#get list of reef names from matrix
reef_list = c_panda.columns.values.tolist()
#print(reef_list)

# set up number of reef sites and number of years
num_sites = len(start_conditions[0])
n_years = 3


#create coral objects 
corals = []
#set up starting conditions
tempM = []
tempC = []

for n in range(0,num_sites):
    corals.append(greiner.greiner()) #what did this do?


# lists to hold final outputs for coral and macroalgae
lastC = []
lastM = []
times = [2006] #first year of data


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

################################################
# begin recruitment calculation

# prep lsc calculations
p_m = 1 
r_area = 4.08/10000. #cm^2 area of settled recruit (fung appendix B)
# for sink in range(0,num_sites): 
#     for source in range(0,num_sites):
#         print(reef_list[sink], reef_list[source], c_matrix[sink][source])


for year in range(0,n_years):
      lsc_new = [] # list to hold updated lsc value
      times.append(times[-1] + 1)
      for sink in range(0,num_sites): 
        Pl = 0
        for source in range(0,num_sites):
            Pl = Pl + (c_matrix[sink][source] * lastC[-1][source])
            Pl = Pl + (lastC[-1][source] * p_m * r_area * c_matrix[sink][source]) 
        lsc_new.append(Pl)
        #print(lsc_new)
        
        #now solve ode using new lsc
      tempC = []
      tempM = []

     
#######################################
# begin solver

      for c in range(0,num_sites):
       #update lsc from above calculation
       #print(lsc_new[c])
       corals[c].set_parameter("g", 0.9)
       corals[c].set_parameter("d", 0.02)
       #corals[c].set_parameter("lbc", 0.5)
       corals[c].set_parameter("lsc", float(lsc_new[c])) # set lsc in regard to the other reefs
       corals[c].set_times([year,year+1])
       corals[c].solve_time() #ode solver
       #print(corals[c].output[1,:])
       corals[c].set_start_conditions(corals[c].output[1,:].tolist())
       tempC.append(corals[c].output[1,0])
       tempM.append(corals[c].output[1,1])

      lastC.append(tempC)
      lastM.append(tempM)



times = np.array(times)
lastC = np.array(lastC).transpose()
lastM = np.array(lastM).transpose()

#########################################
#plotting 


fig_summary=plt.figure(figsize=(12.0,6),dpi=360)
ax=fig_summary.add_subplot(111)
# horseshoe = '#377eb8'
#chineman = '#ff7f00'
#wade = '#4daf4a'
#jenkins = '#a65628'
colours = ['#377eb8', '#ff7f00', '#4daf4a',
            '#a65628', '#984ea3', '#f780bf',
              '#999999', '#e41a1c', '#dede00']
