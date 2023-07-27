#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Tue Jul  4 11:42:58 2023

@author: kl909
"""
from model_collection import *

class greiner(CoralODELab):
    def __init__(self):
        CoralODELab.__init__(self,"greiner")
        self.num_parameters = 9
        self.parameters = {
            "r" : 0.55, #growth
            "d" : 0.24,# mortality 0.02 - 1.0
            "a" : 0.1,# coral overgrowth
            "g" : 0.77,# grazing (use fung?)
            "y" : 0.77, # turf overgrowth
            "lbc" : 0.0025, # divided elmhirst value of all coral recruitment 0.005
            "lsc" : 0.0025,
            "mlbc" : 0.0025,
            "mlsc" : 0.0025,
            
            }
        self.parameter_names = {
            "r" : "growth",
            "d" : "mortality", # 0.02 - 1.0
            "a" : "coral overgrowth",
            "g" : "grazing (use fung?)",
            "y" : "turf overgrowth",
            "lbc" : "local coral recruitment",
            "lsc" : "external coral recruitment",
            "mlbc" : "local algae recruitment",
            "mlsc" : "external algae recruitment",
           
            }
        self.parameter_ranges = {
            
            }
        self.citation = "Greiner, A., S. Darling, E., Fortin, M.-J., & Krkošek, M. (2022). The combined effects of dispersal and herbivores on stable states in coral reefs. Theoretical Ecology, 15(4), 321–335."
        
    def ode(self, z, t):
        r"""
        Setting up equations for Greiner 2023
        ..math:: 
            
            turf: T = 1 - z[0] - z[1]
            
            coral: \frac{dC_1}{dt} = &\underbrace{r(1-q_c) T_1 C_1}_{growth} - \underbrace{dC_1}_{mortality} - \underbrace{\alpha M_1 C_1}_{M \, overgrows \, C} \nonumber\\
                &+ \underbrace{rp_c C_2 T_1}_{recruitment \, from \, C_1 \, and \, C_2}
        
            macroalgae: \frac{dM_1}{dt} = \underbrace{\alpha M_1 C_1}_{M \, overgrows \, C} - \underbrace{g(MT)}_{grazing} + \underbrace{\gamma(1 - q_m)M_1 T_1}_{M_1 \, overgrows \, T_1} + \underbrace{\gamma p_m M_2 T_1}_{M_2 \, overgrows \, T_1}
            
            """
        
        T = 1 - z[0] - z[1]
       #coral z[0]
        growth = self.parameters['r']*(1-self.parameters['lbc'])*T*z[0]
        mortalityC = self.parameters['d']*z[0]
        Movergrowth = self.parameters['a']*z[1]*z[0]
        recruitment = self.parameters['r']*self.parameters['lsc']*T
        dCdt = growth - mortalityC - Movergrowth + recruitment
       
       # macroalgae (z(1))
        MMovergrowth = self.parameters['a']*z[1]*z[0]
        grazing = self.parameters['g']*(z[1]*T)
        growthM1 = self.parameters['y']*(1-self.parameters['mlbc'])*z[1]*T
        growthM2 = self.parameters['y']*self.parameters['mlsc'] *T
        dMdt = MMovergrowth - grazing + growthM1 + growthM2
       
        return[dCdt, dMdt]
    
if __name__ == "__main__":
    # only run if called as a script, not imported
    start = [0.8, 0.2]
    t = np.linspace(0,1, num = 2)
    coralModel = greiner()
    coralModel.set_times(t.tolist())
    coralModel.set_start_conditions(start)
    coralModel.solve_time()
    coralModel.plot_through_time()
    


    coralModel.set_parameter("g", 0.21)
    coralModel.solve_time()
    coralModel.plot_through_time()
    print(coralModel.model_name)
    print(coralModel.citation)

