#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 13:57:48 2023

@author: kl909
"""

from model_collection import *

class fungCTMm(CoralODELab):
    def __init__(self):
        CoralODELab.__init__(self,"fungCTMm")
        self.num_parameters = 14
        self.parameters = {
            "theta" : 0.2, #grazing pressure
            "dc" : 0.05, #coral mortality rate (yr^-1)
            "lbc" : 0.0009, #rate at which coral larvae, produced by local established brooding corals, recruit onto space (yr^-1)
            "lsc_sink" : 0.00006, #rate at which exogenus spawning coral larvae recruit onto space (yr^-1)
            "rc" : 0.2, # lateral growth rate of corals over space (yr^-1)
            "gT" : 10, #maximum rate at which turf algae is grazed (yr^-1)
            "ac" : 0.25, #growth rate of corals over turf, relative to the rate over space
            "ec" : 0.1, #recruitment rate of corals onto turf, relative to the rate onto space 
            "sT" : 5, #growth rate of fine turf (occupying space) (yr^-1)
            "vm" : 0.9,
            "gm" : 0.5,
            "rm" : 0.35,
            "bm" : 0.9,
            "ymc" : 0.1,
            "ymt" : 0.9,
            
            }
        self.parameter_names = {
            "theta" : "grazing pressure",
            "dc" : "coral mortality rate (yr^-1)",
            "lbc" : "rate at which coral larvae, produced by local established brooding corals, recruit onto space (yr^-1)",
            "lsc_sink" : "rate at which exogenus spawning coral larvae recruit onto space (yr^-1)",
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
            "lsc_sink" : [0.00006, 0.01], #rate at which exogenus spawning coral larvae recruit onto space (yr^-1)
            "rc" : [0.04, 0.2], # lateral growth rate of corals over space (yr^-1)
            "gT" : [5, 15], #maximum rate at which turf algae is grazed (yr^-1)
            "ac" : [0,1], #growth rate of corals over turf, relative to the rate over space
            "ec" : [0.05, 0.15], #recruitment rate of corals onto turf, relative to the rate onto space 
            "sT" : [2, 20], #growth rate of fine turf (occupying space) (yr^-1)
            "vm" : [0, 1],
            "gm" : [],
            "rm" : [0.05, 0.4],
            "bm" : [0.2, 0.9],
            "ymc" : [0, 0.9],
            }
        self.citation = "Fung, T., Seymour, R. M., & Johnson, C. R. (2011). Alternative stable states and phase shifts in coral reefs under anthropogenic stress. Ecology, 92(4), 967–982."
        
    def ode(self, z, t):
        r"""
        Setting up equations for Fung et al. 2011
        ..math::
            space: S = 1 - z[0] - z[1] - z[2]
            
            coral: \frac{dC}{dt} = &\underbrace{(l^s_c + l^b_c C)(S+\varepsilon_c T)} _{Recruitment}   
    + \underbrace{r_c(1-\beta_MM)(S+\alpha_c T)C}_{Growth} 
    - \underbrace{d_c C}_{mortality} \nonumber\\
   & - \underbrace{\gamma _{MC} r_m MC)}_{Macroalgae \, overgrowth}
    
            macroalgae: \frac{dM}{dt} = \underbrace{r_M M(S+\gamma_{MC} C+ {\gamma_{MT}} T)}_{Macroalgal \, growth} - \underbrace{g_M \theta M}_{Grazing \, on \, \\ macroalgae} 
            
            turf: \frac{dT}{dt} = &\underbrace{\zeta_T(1-\theta)S}_{Turf\, algal \,growth} - \underbrace{g_T\theta T}_{grazing \,on \,turf} - \underbrace{\varepsilon_C(l^s_c + l^b_c C)T}_{coral \,recruitment\, on \,turf} \nonumber\\
&- \underbrace{\alpha_c r_C (1-\beta_M M)TC}_{coral \,growth \,over \,turf} - \underbrace{\gamma_{MT} r_M MT)}_{macroalgal \, growth \, over \, turf}

        """
        S = 1 - z[0] - z[1] - z[2]
        
            #coral dC
        recruitmentC = (self.parameters['lsc_sink'] + self.parameters['lbc']*z[0])*(S+self.parameters['ec']*z[1])
        growthC = self.parameters['rc']*(1-self.parameters['bm']*z[2])*(S+self.parameters['ac']*z[1])*z[0]
        mortalityC = self.parameters['dc']*z[0]
        MgrowthC = self.parameters['ymc']*self.parameters['rm']*z[2]*z[0]
        
        dCdt = recruitmentC + growthC - mortalityC - MgrowthC
        
        #turf dT
        growthT = self.parameters['sT']*(1-self.parameters['theta'])*S
        grazingT = self.parameters['gT']*self.parameters['theta']*z[1]
        CrecrtuitmentT = self.parameters['ec']*(self.parameters['lsc_sink']+self.parameters['lbc']*z[0])*z[1] #coral recruitment on turf
        CgrowthT = self.parameters['ac']*self.parameters['rc']*(1-self.parameters['bm']*z[2])*z[1]*z[0] #%coral growth over turf
        MgrowthCT = self.parameters['ymt']*self.parameters['rm']*z[2]*z[1]
        
        dTdt = growthT - grazingT - CrecrtuitmentT - CgrowthT - MgrowthCT
        
          #macroalgae dM
        growthM = self.parameters['rm']*z[2]*(S+self.parameters['ymc']*z[0]+self.parameters['ymt']*z[1])
        grazingM = self.parameters['gm']*self.parameters['theta']*z[2]
        
        dMdt = growthM - grazingM
        
        return [dCdt, dTdt, dMdt]

if __name__ == "__main__":
    # only run if called as a script, not imported
    start = [0.8, 0.1, 0.1]
    t = np.linspace(0,100, num = 100)
    coralModel = fungCTMm() #call correct model here
    coralModel.set_times(t)
    coralModel.set_start_conditions(start)
    coralModel.solve_time()
    coralModel.plot_through_time()

    coralModel.set_parameter("g", 0.21)
    coralModel.solve_time()
    coralModel.plot_through_time()
    print(coralModel.model_name)
    print(coralModel.citation)            
