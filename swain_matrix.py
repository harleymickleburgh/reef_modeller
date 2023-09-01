#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 11:20:52 2023

@author: kl909
"""

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



#set up matrix of connectivity
c_matrix = np.loadtxt("swain_matrix.csv",
                       delimiter=",", dtype=float)

c_matrix = np.divide(c_matrix,100)
np.shape(c_matrix)
#print(c_matrix)
#list of reef names
reef_list = ['Horseshoe Reef','Chinaman Reef', 'Wade Reef', 'Jenkins Reef']



#set up start conditions
# row 1 is corals
#row 2 is algae
start_conditions = np.loadtxt("swain_start_noheads.csv",
                      delimiter=",", dtype=float)

start_conditions = np.divide(start_conditions,100)
#start_conditions = start_conditions.tolist() #turn array into list of floats
#start_conditions = pd.read_csv("swain_reef_start.csv", sep=",", header=0, index_col=0 )
#start_conditions = (start_conditions / 100)


num_sites = len(start_conditions[0])
n_years = 200


#create coral objects 
corals = []
# set up starting conditions
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


# prep lsc calculations
p_m = 1 
r_area = 4.08/10000. #cm^2 area of settled recruit (fung appendix B)
# for sink in range(0,num_sites): 
#     for source in range(0,num_sites):
        #print(reef_list[sink], reef_list[source], c_matrix[sink][source])


for year in range(0,n_years):
      lsc_new = [] # list to hold updated lsc value
      times.append(times[-1] + 1)
      for sink in range(0,num_sites): 
        Pl = 0
        for source in range(0,num_sites):
        #     #print(c_matrix[sink])
        #     #begin calculating lsc
            Pl = Pl + (c_matrix[sink][source] * lastC[-1][source])
        #     Pl = Pl + (lastC[-1][source] * p_m * r_area * c_matrix[sink][source]) 
        #     # print(Pl)
        # N = Pl * corals[sink].parameters["d"]
        # T = 1 - lastC[-1][sink] - lastM[-1][sink]
        #lsc_new.append((N * r_area) / T)
        lsc_new.append(Pl)
        #print(lsc_new)
        
        #now solve ode using new lsc
      tempC = []
      tempM = []

 
        #now solve ode using new lsc

      for c in range(0,num_sites):
        #update lsc from above calculation
        #print(lsc_new[c])
        corals[c].set_parameter("g", 0.28)
        corals[c].set_parameter("lbc", 0.5)
        corals[c].set_parameter("mlbc", 0.4)
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

fig_summary=plt.figure(figsize=(12.0,6),dpi=360)
ax=fig_summary.add_subplot(111)
# horseshoe = '#377eb8'
#chineman = '#ff7f00'
#wade = '#4daf4a'
#jenkins = '#a65628'
colours = ['#377eb8', '#ff7f00', '#4daf4a',
            '#a65628', '#984ea3', '#f780bf',
              '#999999', '#e41a1c', '#dede00']

     

# loop over sites, plot the coral and macro lines for each site, looping over colours
for c in range(0,num_sites):
    #print(lastC[c])
    ax.plot(times, lastC[:][c], label= reef_list[c]+ " Coral", color=colours[c])
    ax.plot(times, lastM[:][c], label= reef_list[c]+ " Macro", linestyle="--", color=colours[c])

plt.xticks(np.arange(min(times), max(times)+1, 20))
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0%}'.format(x) for x in current_values])
ax.legend()
plt.title("Reef population change")
plt.xlabel('Years')
plt.ylabel('Population %')
#plt.xlim(2006, 2023)
# plt.axvline(x = 2009, color = 'r', ls=':', lw=1)
# plt.axvline(x = 2011, color = 'r', ls=':', lw=1)
# plt.axvline(x = 2015, color = 'r', ls=':', lw=1)
# plt.axvline(x = 2017, color = 'r', ls=':', lw=1)
# plt.axvline(x = 2016, color = 'r', ls=':', lw=1)
# plt.axvline(x = 2018, color = 'r', ls=':', lw=1)
# plt.axvline(x = 2019, color = 'r', ls=':', lw=1)
# plt.axvline(x = 2020, color = 'r', ls=':', lw=1)



plt.show()
