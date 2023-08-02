#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:29:01 2023

@author: kl909
"""

import greiner
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot

num_years = 500

reefs = {}
site_1 = greiner.greiner()
site_2 = greiner.greiner()
site_1.set_parameter("g",0.29)
site_2.set_parameter("g",0.29)
site_1.set_parameter("lsc",0.06)
site_2.set_parameter("lsc",0.06)
site_1.set_parameter("mlsc",0.06)
site_2.set_parameter("mlsc",0.06)

times = []
coral = []
macro = []
pc = pm = qm = qc = 0.00

site_1.set_start_conditions([0.31794001, 0.31794001])
site_2.set_start_conditions([0.31794001, 0.31794001])

times.append(0)
coral.append([0.31794001, 0.31794001])
macro.append([0.31794001, 0.31794001])

for year in range(0, num_years):
     site_1.set_parameter("lsc", pc * site_2.coral_cover)
     site_2.set_parameter("lsc", qc * site_1.coral_cover)
     site_1.set_parameter("mlsc", pm * site_2.macroalgae_cover)
     site_2.set_parameter("mlsc", qm * site_1.macroalgae_cover)     
     
     site_1.set_times([year,year+1])
     site_1.solve_time()
     site_2.set_times([year,year+1])
     site_2.solve_time()

     site_1.set_start_conditions([float(site_1.coral_cover), float(site_1.macroalgae_cover)])
     site_2.set_start_conditions([float(site_2.coral_cover), float(site_2.macroalgae_cover)])

     times.append(year+1)
     coral.append([site_1.coral_cover, site_2.coral_cover])
     macro.append([site_1.macroalgae_cover, site_2.macroalgae_cover])


print(times[-1], coral[-1], macro[-1])

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
# TODO whata bout saving the image?
plt.show()  
