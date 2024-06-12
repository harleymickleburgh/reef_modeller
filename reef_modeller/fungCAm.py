#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 11:56:24 2023

@author: kl909
"""

from reef_modeller.coral_ode_lab import *

class fungCAm(CoralODELab):
    def __init__(self):
        CoralODELab.__init__(self,"fungCAm")
        self.num_parameters = 14
        self.parameters = {
            "theta" : 0.7, #grazing pressure
            "dc" : 0.02, #coral mortality rate (yr^-1)
            "lbc" : 0.0009, #rate at which coral larvae, produced by local established brooding corals, recruit onto space (yr^-1)
            "lsc" : 0.00006, #rate at which exogenus spawning coral larvae recruit onto space (yr^-1)
            "rc" : 0.2, # lateral growth rate of corals over space (yr^-1)
            "gT" : 10, #maximum rate at which turf algae is grazed (yr^-1)
            "ac" : 0.25, #growth rate of corals over turf, relative to the rate over space
            "ec" : 0.1, #recruitment rate of corals onto turf, relative to the rate onto space 
            "sT" : 5, #growth rate of fine turf (occupying space) (yr^-1)
            "vm" : 0.9, #proportion of total algal cover that is macroalgal cover
            "gm" : 3.5, #maximum rate at which macroalgae is grazed (yr^-1)
            "rm" : 0.35, #lateral growth rate of macroalgae over space
            "bm" : 0.9, #coral growth is inhibited by presence of nearbymacroalgae
            "ymc" : 0.1, #lateral growth rate of macroalgae over corals,relative to the rate over space
            
            }
        self.parameter_names = {
            "theta" : "grazing pressure",
            "dc" : "coral mortality rate (yr^-1)",
            "lbc" : "rate at which coral larvae, produced by local established brooding corals, recruit onto space (yr^-1)",
            "lsc" : "rate at which exogenus spawning coral larvae recruit onto space (yr^-1)",
            "rc" : "lateral growth rate of corals over space (yr^-1)",
            "gT" : "maximum rate at which turf algae is grazed (yr^-1)",
            "ac" : "growth rate of corals over turf, relative to the rate over space",
            "ec" : "recruitment rate of corals onto turf, relative to the rate onto space",
            "sT" : "growth rate of fine turf (occupying space) (yr^-1)",
            "vm" : "proportion of total algal cover that is macroalgal cover",
            "gm" : "maximum rate at which macroalgae is grazed",
            "rm" : "lateral growth rate of macroalgae over space",
            "bm" : "coral growth is inhibited by presence of nearbymacroalgae, represented as depression ofrCby the factor",
            "ymc" : "lateral growth rate of macroalgae over corals,relative to the rate over space",
            
            }
        
        self.parameter_ranges = {
            "theta" : [0.4, 1], #grazing pressure
            "dc" : [0.02, 0.1], #coral mortality rate (yr^-1)
            "lbc" : [0.0009, 0.5], #rate at which coral larvae, produced by local established brooding corals, recruit onto space (yr^-1)
            "lsc" : [0.00006, 0.01], #rate at which exogenus spawning coral larvae recruit onto space (yr^-1)
            "rc" : [0.04, 0.2], # lateral growth rate of corals over space (yr^-1)
            "gT" : [5, 15], #maximum rate at which turf algae is grazed (yr^-1)
            "ac" : [0,1], #growth rate of corals over turf, relative to the rate over space
            "ec" : [0.05, 0.15], #recruitment rate of corals onto turf, relative to the rate onto space 
            "sT" : [2, 20], #growth rate of fine turf (occupying space) (yr^-1)
            "vm" : [0, 1],
            "gm" : [(0.1*5), (0.1*15)],
            "rm" : [0.05, 0.4],
            "bm" : [0.2, 0.9],
            "ymc" : [0, 0.9],
            }
        self.citation = "Fung, T., Seymour, R. M., & Johnson, C. R. (2011). \
                         Alternative stable states and phase shifts in coral \
                         reefs under anthropogenic stress. Ecology, 92(4), 967–982."
        
    def ode(self, z, t):
        S = 1 - z[0] - z[1]
        
            #coral dC
        recruitmentC = (self.parameters['lsc'] + self.parameters['lbc']*z[0]) * \
                       (S+self.parameters['ec']*(1 - self.parameters['vm'])*z[1])
        growthC = self.parameters['rc']*(1 - self.parameters['bm'] * self.parameters['vm'] * z[1]) * \
                  (S + self.parameters['ac']*(1 -self.parameters['vm'])*z[1])*z[0]
        mortalityC = self.parameters['dc']*z[0]
        MgrowthC = self.parameters['ymc']*self.parameters['rm']*self.parameters['vm']*z[1]*z[0]
        dCdt = recruitmentC + growthC - mortalityC - MgrowthC
        
        # algae dM
        growthMA = self.parameters['rm']*self.parameters['vm']*z[1]*(S+self.parameters['ymc']*z[0])
        growthT = self.parameters['sT']*(1-self.parameters['theta'])*S
        grazingAT = (self.parameters['gm']*self.parameters['vm']+self.parameters['gT']*(1-self.parameters['vm']))*self.parameters['theta']*z[1]
        CrecruitmentT = self.parameters['ec']*(1-self.parameters['vm'])*(self.parameters['lsc']+self.parameters['lbc']*z[0])*z[1]
        CgrowthT = self.parameters['ac']*self.parameters['rc']*(1-self.parameters['vm'])*(1 - self.parameters['bm']*self.parameters['vm']*z[1])*z[1]*z[0] 
        dMdt = growthMA + growthT - grazingAT - CrecruitmentT - CgrowthT
        
        return [dCdt, dMdt]
            
if __name__ == "__main__":
    # only run if called as a script, not imported
    start = [0.1, 0.6]
    coralModel = fungCAm()
    coralModel.set_start_conditions(start)

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.optimize import fsolve


    thetas = []
    corals = []
    algae = []
    for theta in np.arange(0.2, 0.71, 0.01):
        coralModel.set_start_conditions(start)        
        coralModel.set_parameter("theta",theta)
        eq = fsolve(coralModel.ode, start, args=(0))
        thetas.append(theta)
        corals.append(eq[0])
        algae.append(eq[1])
        

    fig, ax = plt.subplots()
    ax.plot(thetas, corals, label="Coral", color=coralModel._coral_colour)
    ax.plot(thetas, algae, label="Algae", color=coralModel._malgae_colour)


    ax.set(xlabel='Grazing', ylabel='Perc Cover')
    ax.grid()

    plt.show()
