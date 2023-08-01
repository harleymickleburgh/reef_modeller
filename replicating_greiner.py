#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:29:01 2023

@author: kl909
"""

import greiner
import numpy as np

num_years = 500

reefs = {}
site_1 = greiner.greiner()
site_2 = greiner.greiner()
site_1.set_parameter("g",0.8)
site_2.set_parameter("g",0.8)
site_1.set_parameter("lsc",0.0)
site_2.set_parameter("lsc",0.0)
site_1.set_parameter("mlsc",0.0)
site_2.set_parameter("mlsc",0.0)

times = []
coral = []
macro = []
pc = pm = qm = qc = 0.00

site_1.set_start_conditions([0.0, 0.8])
site_2.set_start_conditions([0.0, 0.8])

times.append(0)
coral.append([0.0,0.8])
macro.append([0.0,0.8])

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


print(times, coral, macro)
