#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 15:59:18 2023

@author: kl909
"""

from model_collection import *

class Mcmanus(CoralODELab):
    def __init__(self):
        CoralODELab.__init__(self,"Mcmanus")
        self.num_parameters = 7
        self.parameters = {
            "r" : 0.2, #growth
            "d" : 0.5,# mortality 0.02 - 1.0
            "a" : 1.0,# coral overgrowth
            "f" : 10, # no. of larvae per meter per year
            "s" : 0.01,# area of newly settled recruit
            "g" : 0.4,# grazing (use fung?)
            "y" : 1.1, # turf overgrowth
            "w" : 0.005, # spawning larvae (use lsc from fung?)
            "time" : 0.5, #duration of external coral recruitment 0-1
            
            }
        self.parameter_names = {
            "r" : "growth",
            "d" : "mortality", # 0.02 - 1.0
            "a" : "coral overgrowth",
            "f" : "no. of larvae per meter per year",
            "s" : "area of newly settled recruit",
            "g" : "grazing (use fung?)",
            "y" : "turf overgrowth",
            "w" : "spawning larvae (use lsc from fung?)",
            "time" : "duration of external coral recruitment",# 0-1
            }
        self.parameter_ranges = {
            
            }
        self.citation = "McManus, L. C., Watson, J. R., Vasconcelos, V. V., & Levin, S. A. (2019). Stability and recovery of coral-algae systems: the importance of recruitment seasonality and grazing influence. Theoretical Ecology, 12(1), 61–72."
        
    def ode(self, z, t):
        F = 1 - z[0] - z[1]
        
        growth = (self.parameters['r']*F) * z[0]
        mortality = self.parameters['d']*z[0]
        movergrowsc = self.parameters['a']*z[0]*z[1]
        recruitment = (self.parameters['f']*self.parameters['s'] + self.parameters['w'])*F # was (f*s*z[0] + w)*F
        dCdt = growth - mortality - movergrowsc + recruitment
        
        mmovergrowsc = self.parameters['a']*z[0]*z[1]
        grazing = self.parameters['g']*z[1]
        movergrowst = self.parameters['y']*z[1]*F
        dMdt = mmovergrowsc - grazing + movergrowst
       
        return[dCdt, dMdt]
    
if __name__ == "__main__":
    # only run if called as a script, not imported
    start = [0.8, 0.2]
    t = np.linspace(0,100, num = 100)
    coralModel = Mcmanus()
    coralModel.set_times(t)
    coralModel.set_start_conditions(start)
    coralModel.solve_time()
    coralModel.plot_through_time()


    coralModel.set_parameter("g", 0.21)
    coralModel.solve_time()
    coralModel.plot_through_time()
    print(coralModel.model_name)
    print(coralModel.citation)
        

