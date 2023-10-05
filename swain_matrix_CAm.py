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

import fungCAm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



#set up matrix of connectivity
c_matrix = np.loadtxt("swain_matrix.csv",
                       delimiter=",", dtype=float)

c_matrix = np.divide(c_matrix,100)
np.shape(c_matrix)

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
n_years = 3


#create coral objects 
corals = []
# set up starting conditions
tempM = []
tempC = []

for n in range(0,num_sites):
    corals.append(fungCAm.fungCAm()) #what did this do?


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


for year in range(0,n_years):
      lsc_new = [] # list to hold updated lsc value
      times.append(times[-1] + 1)
      for sink in range(0,num_sites): 
        Pl = 0
        for source in range(0,num_sites):
            #print(c_matrix[sink])
            #begin calculating lsc
            Pl = Pl + (lastC[-1][source] * p_m * r_area * c_matrix[sink][source]) 
            # print(Pl)
        N = Pl * corals[sink].parameters["dc"]
        T = 1 - lastC[-1][sink] - lastM[-1][sink]
        lsc_new.append((N * r_area) / T)
        lsc_new.append(Pl)
        #print(lsc_new)
        
        #now solve ode using new lsc
      tempC = []
      tempM = []

     
        #now solve ode using new lsc

      for c in range(0,num_sites):
        #update lsc from above calculation
        #print(lsc_new[c])
        corals[c].set_parameter("theta" , 0.9) #grazing pressure
        corals[c].set_parameter("dc" , 0.02) #coral mortality rate (yr^-1)
        corals[c].set_parameter("lbc" , 0.00005) #rate at which coral larvae, produced by local established brooding corals, recruit onto space (yr^-1)
        #corals[c].set_parameter("lsc" , 0.00006) #rate at which exogenus spawning coral larvae recruit onto space (yr^-1)
        corals[c].set_parameter("rc" , 0.2) # lateral growth rate of corals over space (yr^-1)
        corals[c].set_parameter("gT" , 10) #maximum rate at which turf algae is grazed (yr^-1)
        corals[c].set_parameter("ac" , 0.8) #growth rate of corals over turf, relative to the rate over space
        corals[c].set_parameter("ec" , 0.1) #recruitment rate of corals onto turf, relative to the rate onto space 
        corals[c].set_parameter("sT" , 5) #growth rate of fine turf (occupying space) (yr^-1)
        corals[c].set_parameter("vm" , 0) #proportion of total algal cover that is macroalgal cover
        corals[c].set_parameter("gm" , 0.9) #maximum rate at which macroalgae is grazed
        corals[c].set_parameter("rm" , 0.05) #lateral growth rate of macroalgae over space
        corals[c].set_parameter("bm" , 0.2) #coral growth is inhibited by presence of nearbymacroalgae
        corals[c].set_parameter("ymc" , 0.01) #lateral growth rate of macroalgae over corals,relative to the rate over space
        corals[c].set_parameter("ymt" , 0.1) #lateral growth rate of macroalgae over turf,relative to the rate over space
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


output = pd.DataFrame(columns=["Reef ID", "Year", "Coral %", "Macroalgae %"])
#print(output)


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


plt.xticks(np.arange(min(times), max(times)+1, 1))
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0%}'.format(x) for x in current_values])
ax.legend()
plt.title("Reef population change")
plt.xlabel('Years')
plt.ylabel('Population %')
plt.xlim(2006, 2009)
# plt.axvline(x = 2009, color = 'r', ls=':', lw=1)
# plt.axvline(x = 2011, color = 'r', ls=':', lw=1)
# plt.axvline(x = 2015, color = 'r', ls=':', lw=1)
# plt.axvline(x = 2017, color = 'r', ls=':', lw=1)
# plt.axvline(x = 2016, color = 'r', ls=':', lw=1)
# plt.axvline(x = 2018, color = 'r', ls=':', lw=1)
# plt.axvline(x = 2019, color = 'r', ls=':', lw=1)
# plt.axvline(x = 2020, color = 'r', ls=':', lw=1)



plt.show()