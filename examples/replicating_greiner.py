#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:29:01 2023

@author: kl909
"""

import sys
sys.path.insert(0,"../")
import numpy as np
import matplotlib.pyplot as plt
import reef_modeller.greiner
from scipy.optimize import fsolve

n_sites = 2
num_years = 500

reefs = {}
reefs["site_1"] = reef_modeller.greiner.greiner()
reefs["site_2"] = reef_modeller.greiner.greiner()
reefs["site_1"].set_parameter("g",0.29)
reefs["site_2"].set_parameter("g",0.29)
reefs["site_1"].set_parameter("lsc",0.06)
reefs["site_2"].set_parameter("lsc",0.06)
reefs["site_1"].set_parameter("mlsc",0.06)
reefs["site_2"].set_parameter("mlsc",0.06)

times = []
coral = []
macro = []
pc = pm = qm = qc = 0.06

reefs["site_1"].set_start_conditions([0.08, 0.48])
reefs["site_2"].set_start_conditions([0.45, 0.08])

times.append(0)
coral.append([reefs["site_1"].coral_cover, reefs["site_2"].coral_cover])
macro.append([reefs["site_1"].macroalgae_cover, reefs["site_2"].macroalgae_cover])

for year in range(0, num_years):
     reefs["site_1"].set_parameter("lsc", pc * reefs["site_2"].coral_cover)
     reefs["site_2"].set_parameter("lsc", qc * reefs["site_1"].coral_cover)
     reefs["site_1"].set_parameter("mlsc", pm * reefs["site_2"].macroalgae_cover)
     reefs["site_2"].set_parameter("mlsc", qm * reefs["site_1"].macroalgae_cover)    
     reefs["site_1"].set_parameter("lbc", (1-pc))
     reefs["site_2"].set_parameter("lbc", (1-qc))
     reefs["site_1"].set_parameter("mlbc", (1-pm))
     reefs["site_1"].set_parameter("mlbc", (1-pm))
     
     reefs["site_1"].set_times([year,year+1])
     reefs["site_1"].solve_time()
     reefs["site_2"].set_times([year,year+1])
     reefs["site_2"].solve_time()

     reefs["site_1"].set_start_conditions([float(reefs["site_1"].coral_cover), float(reefs["site_1"].macroalgae_cover)])
     reefs["site_2"].set_start_conditions([float(reefs["site_2"].coral_cover), float(reefs["site_2"].macroalgae_cover)])

     times.append(year+1)
     coral.append([reefs["site_1"].coral_cover, reefs["site_2"].coral_cover])
     macro.append([reefs["site_1"].macroalgae_cover, reefs["site_2"].macroalgae_cover])

# separate out reef 1 and 2 coral and macroalgae
reef1coral= []
reef1macro= []
reef2coral= []
reef2macro= []
for value in coral:
    reef1coral.append(value[0])
    reef2coral.append(value[1])

for value in macro:
    reef1macro.append(value[0])
    reef2macro.append(value[1])

#plot graph 
plt.plot(times, reef1coral, label="Reef 1 Coral", color="#F88379")
plt.plot(times, reef1macro, label="Reef 1 Algae", color="#617D48")
plt.plot(times, reef2coral, '--', label="Reef 2 Coral", color="#F88379")
plt.plot(times, reef2macro, '--', label="Reef 2 Algae", color="#617D48")
plt.ylim(0,1)
plt.xlim(-1)
plt.legend()
plt.title("Replicating Greiner (dispersal 0.06)")
plt.xlabel('Time (years)')
plt.ylabel('Population')
plt.show()  
