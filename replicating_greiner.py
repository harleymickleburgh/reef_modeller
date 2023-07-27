#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:29:01 2023

@author: kl909
"""

import greiner
import numpy as np


reef1 = 0
reef2 = 0

start = [0.8, 0.2]



# reef1.set_start_conditions([0.1,0.1])
# reef2.set_start_conditions([0.1,0.1])


num_years = 10

for y in num_years:
     coralModel.set_start_conditions(start)
    
    
    

# reef 1 lsc = lsc * reef 2 coral
# reef 1 mlsc = mlsc * reef 2 algae

# reef 2 lsc = lsc * reef 1 coral
# reef 1 mlsc = mlsc * reef 1 algae

# save reef 1 coral cover
# save reef 1 algae cover

# save reef 2 coral cover
# save reef 2 algae cover



