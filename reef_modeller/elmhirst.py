#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 15:09:45 2023

@author: kl909
"""

from reef_modeller.coral_ode_lab import *


class elmhirst(CoralODELab):
    def __init__(self):
        CoralODELab.__init__(self,"elmhirst")
        self.num_parameters = 7
        self.parameters = {
            "r" : 0.55, #growth
            "d" : 0.24,# mortality 0.02 - 1.0
            "a" : 0.1,# coral overgrowth
            "s" : 0.005, #coral recruitment
            "g" : 0.2,# grazing (use fung?)
            "y" : 0.77, # turf overgrowth
            "e" : 0.005, #algae recruitment
            
            
            }
        self.parameter_names = {
            "r" : "growth",
            "d" : "mortality", # 0.02 - 1.0
            "a" : "coral overgrowth",
            "s" : "coral recruitment",
            "g" : "grazing (use fung?)",
            "y" : "turf overgrowth",
            "e" : "algae recruitment",
           
            }
        self.parameter_ranges = {
            
            }
        self.citation = "Elmhirst, T., Connolly, S. R., & Hughes, T. P. (2009). Connectivity, regime shifts and the resilience of coral reefs. Coral Reefs , 28(4), 949–957."
        
    def ode(self, z, t):
        r"""
        setting up equations for Elmhirst et al. 2009
        .. math::
            turf: T = 1 - z[0] - z[1]
            coral: \frac{dC}{dt} = g(M,C) = \underbrace{C(rT)}_{growth} - \underbrace{dC}_{mortality} - \underbrace{\alpha MC}_{overgrowth \, by \, M} + \underbrace{\zeta T}_{recruitment}
            macroalgae: \frac{dM}{dt} = f(M,C) = \underbrace{\alpha MC}_{M \, overgrowing \, C} + \underbrace{M(\frac{g}{C-1}}_{grazing} + \underbrace{\gamma T)}_{M \, overgrows \, T} + \underbrace{\epsilon T}_{recruitment}

        """
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
        
        return[ dCdt, dMdt]
     
if __name__ == "__main__":
    # only run if called as a script, not imported
    start = [0.8, 0.2]
    t = np.linspace(0,100, num = 100)
    coralModel = elmhirst()
    coralModel.set_times(t)
    coralModel.set_start_conditions(start)
    coralModel.solve_time()
    coralModel.plot_through_time()


    coralModel.set_parameter("g", 0.21)
    coralModel.solve_time()
    coralModel.plot_through_time()
    print(coralModel.model_name)
    print(coralModel.citation)       
