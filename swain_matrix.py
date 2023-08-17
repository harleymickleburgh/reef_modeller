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



#set up start conditions
# row 1 is corals
#row 2 is algae
start_conditions = np.loadtxt("swain_start_noheads.csv",
                      delimiter=",", dtype=float)

start_conditions = np.divide(start_conditions,100)
np.shape(start_conditions)
#start_conditions = pd.read_csv("swain_reef_start.csv", sep=",", header=0, index_col=0 )
#start_conditions = (start_conditions / 100)



num_sites = start_conditions.shape[1]
n_years = 5


#create coral objects 
corals = []

for n in range(0,num_sites):
    corals.append(greiner.greiner()) #what did this do?


# lists to hold final outputs for coral and macroalgae
lastC = []
lastM = []
times = []


# set up starting conditions
tempM = []
tempC = []



tempC.append(start_conditions[0])
tempM.append(start_conditions[1])   

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
            #print(c_matrix[source])
            #begin calculating lsc
            Pl = Pl + (lastC[-1][source] * p_m * r_area * c_matrix[sink][source]) 
        N = Pl * corals[sink].parameters["d"]
        T = 1 - lastC[-1][sink] - lastM[-1][sink]
        lsc_new.append((N * r_area) / T)

     
# #       #now solve ode using new lsc
# #       tempC = []
# #       tempM = []
# #       for c in range(0,num_sites):
# #           #update lsc from above calculation
# #           corals[c].set_parameter("lsc", float(lsc_new[c])) # set lsc in regard to the other reefs
# #           corals[c].set_times([year,year+1])
# #           corals[c].solve_time() #ode solver
# #           #print(corals[c].output[1,:])
# #           corals[c].set_start_conditions(corals[c].output[1,:].tolist())
# #           tempC.append(corals[c].output[1,0])
# #           tempM.append(corals[c].output[1,1])

# #       lastC.append(tempC)
# #       lastM.append(tempM)

# # times.append(n_years)

# # # create 3 arrays:

# # # time = 1D array (like: [1, 2, 3, 4, 5]
# # # corals = 2D array:
# # #   0.1   0.23
# # #   0.1   0.23
# # #   ...   ..
# # #   0.23  0.23
# # # columns are same length as time, each column is a different site.
# # # macros is the same structure as corals.
# # print(times)
# # print(lastM)
# # print(lastC)
# # times = np.array(times)
# # lastC = np.array(lastC).transpose()
# # lastM = np.array(lastM).transpose()

# # fig_summary=plt.figure(figsize=(12.0,6),dpi=360)
# # ax=fig_summary.add_subplot(111)
# # colours = ['#377eb8', '#ff7f00', '#4daf4a',
# #             '#a65628', '#984ea3', '#f780bf',
# #               '#999999', '#e41a1c', '#dede00']

     

# # # loop over sites, plot the coral and macro lines for each site, looping over colours
# # for c in range(0,num_sites):
# #     print(lastC[c])
# #     ax.plot(times, lastC[:][c], label="Reef "+str(c)+" Coral", color=colours[c])
# #     ax.plot(times, lastM[:][c], label="Reef "+str(c)+" Macro", linestyle="--", color=colours[c])
    
# # ax.legend()
# # plt.show()


     

     
     


    
