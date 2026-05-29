#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from types import SimpleNamespace
from .CoralODELab import CoralODELab

class FungCTMm(CoralODELab):
    def __init__(self):
        CoralODELab.__init__(self,"fungCTMm")
        self.num_eq = 3
        self.num_parameters = 14
        self.parameters = {
            "theta" : 0.7, #grazing pressure
            "dc" : 0.05, #coral mortality rate (yr^-1)
            "lbc" : 0.0009, #rate at which coral larvae, produced by local established brooding corals, recruit onto space (yr^-1)
            "lsc" : 0.00006, #rate at which exogenus spawning coral larvae recruit onto space (yr^-1)
            "rc" : 0.3, # lateral growth rate of corals over space (yr^-1)
            "gT" : 7, #maximum rate at which turf algae is grazed (yr^-1)
            "ac" : 0.025, #growth rate of corals over turf, relative to the rate over space
            "ec" : 0.1, #recruitment rate of corals onto turf, relative to the rate onto space 
            "sT" : 10, #growth rate of fine turf (occupying space) (yr^-1)
            "gm" : 0.5,
            "rm" : 0.35,
            "bm" : 0.9,
            "ymc" : 0.02,
            "ymt" : 0.97,    
            }
        self.p = SimpleNamespace(**self.parameters)
    
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
            "gm" : "maximum rate at which macroalgae is grazed",
            "rm" : "lateral growth rate of macroalgae over space",
            "bm" : "coral growth is inhibited by presence of nearbymacroalgae, represented as depression ofrCby the factor",
            "ymc" : "lateral growth rate of macroalgae over corals, relative to the rate over space",
            "ymt" : "lateral growth rate of macroalgae over turf, relative to the rate over space" 
            }
        
        self.parameter_range = {
            "theta" : [0, 1], #grazing pressure
            "dc" : [0.02, 0.1], #coral mortality rate (yr^-1)
            "lbc" : [0.0009, 0.5], #rate at which coral larvae, produced by local established brooding corals, recruit onto space (yr^-1)
            "lsc" : [0.00006, 0.01], #rate at which exogenus spawning coral larvae recruit onto space (yr^-1)
            "rc" : [0.04, 0.2], # lateral growth rate of corals over space (yr^-1)
            "gT" : [5, 15], #maximum rate at which turf algae is grazed (yr^-1)
            "ac" : [0,1], #growth rate of corals over turf, relative to the rate over space
            "ec" : [0.05, 0.15], #recruitment rate of corals onto turf, relative to the rate onto space 
            "sT" : [2, 20], #growth rate of fine turf (occupying space) (yr^-1)
            "gm" : [0, 1],
            "rm" : [0.05, 0.4],
            "bm" : [0.2, 0.9],
            "ymc" : [0, 0.9],
            "ymt" : [0, 0.9]
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
   & - \underbrace{\gamma_{MC} r_m MC)}_{Macroalgae \, overgrowth}
    
            macroalgae: \frac{dM}{dt} = \underbrace{r_M M(S+\gamma_{MC} C+ {\gamma_{MT}} T)}_{Macroalgal \, growth} - \underbrace{g_M \theta M}_{Grazing \, on \, \\ macroalgae} 
            
            turf: \frac{dT}{dt} = &\underbrace{\zeta_T(1-\theta)S}_{Turf\, algal \,growth} - \underbrace{g_T\theta T}_{grazing \,on \,turf} - \underbrace{\varepsilon_C(l^s_c + l^b_c C)T}_{coral \,recruitment\, on \,turf} \nonumber\\
&- \underbrace{\alpha_c r_C (1-\beta_M M)TC}_{coral \,growth \,over \,turf} - \underbrace{\gamma_{MT} r_M MT)}_{macroalgal \, growth \, over \, turf}

        """
        S = 1.0 - sum(z)
        C = z[0]
        T = z[1]
        M = z[2]


        #coral dC
        recruitmentC = (self.p.lsc + self.p.lbc * C) * (S + self.p.ec * T)
        growthC = self.p.rc * (1 - self.p.bm * M) * (S + self.p.ac * T) * C
        mortalityC = self.p.dc * C
        MgrowthC = self.p.ymc * self.p.rm * M * C
        
        dCdt = recruitmentC + growthC - mortalityC - MgrowthC
        
        #turf dT
        growthT = self.p.sT * (1 - self.p.theta) * S
        grazingT = self.p.gT * self.p.theta * T
        CrecrtuitmentT = self.p.ec * (self.p.lsc + self.p.lbc * C) * T # coral recruitment on turf
        CgrowthT = self.p.ac * self.p.rc * (1 - self.p.bm * M) * T * C # coral growth over turf
        MgrowthCT = self.p.ymt * self.p.rm * M * T
        
        dTdt = growthT - grazingT - CrecrtuitmentT - CgrowthT - MgrowthCT
        
        #macroalgae dM
        growthM = self.p.rm * M * (S + self.p.ymc * C + self.p.ymt * T)
        grazingM = self.p.gm * self.p.theta * M
        
        dMdt = growthM - grazingM
        
        return [dCdt, dTdt, dMdt]

    def analytical_jacobian(self, state):
        """
        Calculates the exact analytical Jacobian matrix for the Fung et al. model.
        Assumes state vector is ordered as [Coral, Turf, Macroalgae].
        """
        import numpy as np
        
        C, T, M = state
        S = 1.0 - C - T - M
        
        # Unpack parameters (adjust these string keys to match your self.p dictionary)
        l_s_c = self.p.lsc
        l_b_c = self.p.lbc
        eps_c = self.p.ec
        r_c = self.p.rc
        beta_M = self.p.bm
        alpha_c = self.p.ac
        d_c = self.p.dc
        gamma_MC = self.p.ymc
        r_m = self.p.rm
        g_M = self.p.gm
        gamma_MT = self.p.ymt
        zeta_T = self.p.sT
        theta = self.p.theta
        g_T = self.p.gT
        
        # 1. dC/dt derivatives
        dC_dC = l_b_c * (S + eps_c * T) - (l_s_c + l_b_c * C) + \
                r_c * (1 - beta_M * M) * (S + alpha_c * T - C) - \
                d_c - gamma_MC * r_m * M
                
        dC_dT = (l_s_c + l_b_c * C) * (eps_c - 1) + \
                r_c * (1 - beta_M * M) * C * (alpha_c - 1)
                
        dC_dM = -(l_s_c + l_b_c * C) - \
                r_c * C * (beta_M * (S + alpha_c * T) + (1 - beta_M * M)) - \
                gamma_MC * r_m * C
        
        # 2. dT/dt derivatives
        dT_dC = -zeta_T * (1 - theta) - eps_c * l_b_c * T - \
                alpha_c * r_c * (1 - beta_M * M) * T
                
        dT_dT = -zeta_T * (1 - theta) - g_T * theta - \
                eps_c * (l_s_c + l_b_c * C) - \
                alpha_c * r_c * (1 - beta_M * M) * C - \
                gamma_MT * r_m * M
                
        dT_dM = -zeta_T * (1 - theta) + \
                alpha_c * r_c * beta_M * T * C - \
                gamma_MT * r_m * T
        
        # 3. dM/dt derivatives
        dM_dC = r_m * M * (gamma_MC - 1)
        dM_dT = r_m * M * (gamma_MT - 1)
        dM_dM = r_m * (S + gamma_MC * C + gamma_MT * T - M) - g_M * theta
        
        # Return as 3x3 array ordered [C, T, M]
        return np.array([
            [dC_dC, dC_dT, dC_dM],
            [dT_dC, dT_dT, dT_dM],
            [dM_dC, dM_dT, dM_dM]
        ])


class FungCAm(CoralODELab):
    def __init__(self):
        CoralODELab.__init__(self,"fungCAm")
        self.num_parameters = 14
        self.num_eq = 2
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
        self.p = SimpleNamespace(**self.parameters)

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
        
        self.parameter_range = {
            "theta" : [0.0, 1], #grazing pressure
            "dc" : [0.02, 0.1], #coral mortality rate (yr^-1)
            "lbc" : [0.0009, 0.5], #rate at which coral larvae, produced by local established brooding corals, recruit onto space (yr^-1)
            "lsc" : [0.00006, 0.01], #rate at which exogenus spawning coral larvae recruit onto space (yr^-1)
            "rc" : [0.04, 0.2], # lateral growth rate of corals over space (yr^-1)
            "gT" : [5, 15], #maximum rate at which turf algae is grazed (yr^-1)
            "ac" : [0,1], #growth rate of corals over turf, relative to the rate over space
            "ec" : [0.05, 0.15], #recruitment rate of corals onto turf, relative to the rate onto space 
            "sT" : [2, 20], #growth rate of fine turf (occupying space) (yr^-1)
            "vm" : [0, 1],
            "gm" : [0.5, 1.5],
            "rm" : [0.05, 0.4],
            "bm" : [0.2, 0.9],
            "ymc" : [0, 0.9],
            }
        self.citation = "Fung, T., Seymour, R. M., & Johnson, C. R. (2011). \
                         Alternative stable states and phase shifts in coral \
                         reefs under anthropogenic stress. Ecology, 92(4), 967–982."
        
    def ode(self, z, t):
        S = 1 - sum(z)
        C = z[0]
        A = z[1]

        #coral dC
        recruitmentC = (self.p.lsc + self.p.lbc * C) * \
                       (S + self.p.ec * (1 - self.p.vm) * A)
        growthC = self.p.rc * (1 - self.p.bm * self.p.vm * A) * \
                  (S + self.p.ac * (1 -self.p.vm) * A) * C
        mortalityC = self.p.dc * C
        MgrowthC = self.p.ymc * self.p.rm * self.p.vm * A * C
        dCdt = recruitmentC + growthC - mortalityC - MgrowthC
        
        # algae dM
        growthMA = self.p.rm * self.p.vm * A * (S + self.p.ymc * C)
        growthT = self.p.sT * (1 - self.p.theta) * S
        grazingAT = (self.p.gm * self.p.vm + self.p.gT * (1 - self.p.vm)) * self.p.theta * A
        CrecruitmentT = self.p.ec * (1 - self.p.vm) * (self.p.lsc + self.p.lbc * C) * A
        CgrowthT = self.p.ac * self.p.rc * (1 - self.p.vm) * (1 - self.p.bm * self.p.vm * A) * A * C 
        dAdt = growthMA + growthT - grazingAT - CrecruitmentT - CgrowthT
 
        return [dCdt, dAdt]
