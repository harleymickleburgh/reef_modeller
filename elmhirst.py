#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 14:52:28 2023

@author: kl909
"""
from model_collection import *

class Elmhirst(CoralODELab):
    def __init__(self):
        CoralODELab.__init__(self,"Elmhirst")
        self.num_parameters = 7
        self.parameters = {
            "r" : 0.55, # growth
            "d" : 0.24, # mortality
            "a" : 0.1, # overgrowth of coral by M
            "s" : 0.005, # coral recruitment
            "g" : 0.2, #grazing 0 - 0.5
            "y" : 0.77, # M overgrowing T
            "e" : 0.005, # algae recruitment
            
            }
        self.parameter_names = {
            "r" : "growth",
            "d" : "mortality",
            "a" : "overgrowth of coral by M",
            "s" : "coral recruitment",
            "g" : "grazing", # 0 - 0.5
            "y" : "M overgrowing T",
            "e" : "algae recruitment",
            }
        self.parameter_ranges = {
            
            }
        self.citation = "Elmhirst, T., Connolly, S. R., & Hughes, T. P. (2009). Connectivity, regime shifts and the resilience of coral reefs. Coral Reefs , 28(4), 949–957. "
        
    def ode(self, z, t):
        T = 1 - z[0] - z[1]
        
        growth = z[0]*(self.parameters['r']*T)
        mortality = self.parameters['d']*z[0]
        overgrowthM = self.parameters['a']*z[1]*z[0]
        recruitment = self.parameters['s']*T
        dCdt = growth - mortality - overgrowthM + recruitment
        
        movergrowingC = self.parameters['a']*z[1]*z[0]
        grazing = z[1]*(self.parameters['g']/(z[0]-1)) 
        MovergrowsT = self.parameters['y']*z[1]*T
        Mrecruitment = self.parameters['e']*T
        dMdt = movergrowingC + grazing + MovergrowsT + Mrecruitment
        
        return( dCdt, dMdt)
    
if __name__ == "__main__":
    # only run if called as a script, not imported
    start = [0.8, 0.2]
    t = np.linspace(0,100, num = 100)
    coralModel = Elmhirst()
    coralModel.set_times(t)
    coralModel.set_start_conditions(start)
    coralModel.solve_time()
    coralModel.plot_through_time()

    coralModel.set_parameter("g", 0.21)
    coralModel.solve_time()
    coralModel.plot_through_time()
    print(coralModel.model_name)
    print(coralModel.citation)
        
