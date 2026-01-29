#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 15:59:18 2023

@author: kl909
"""
from .CoralODELab import CoralODELab
from types import SimpleNamespace

class Mcmanus(CoralODELab):
    def __init__(self):
        CoralODELab.__init__(self,"Mcmanus")
        self.num_parameters = 7
        self.num_eq = 2
        self.parameters = {
            "r" : 0.2, #growth
            "d" : 0.5,# mortality 0.02 - 1.0
            "a" : 1.0,# coral overgrowth
            "f" : 10, # no. of larvae per meter per year
            "s" : 0.01,# area of newly settled recruit
            "g" : 0.4,# grazing
            "g1": 0.7, # grazing when coral == 1
            "y" : 1.1, # turf overgrowth
            "w" : 0.005, # spawning larvae
            "time" : 1, #duration of external coral recruitment 0-1
            "alpha" : 1, #set's grazng type
            }
        self.p = SimpleNamespace(**self.parameters)         
        self.parameter_names = {
            "r" : "growth",
            "d" : "mortality", # 0.02 - 1.0
            "a" : "coral overgrowth",
            "f" : "no. of larvae per meter per year",
            "s" : "area of newly settled recruit",
            "g" : "baseline grazing",
            "g1": "max grazing rate",
            "y" : "turf overgrowth",
            "w" : "spawning larvae term",
            "time" : "duration of external coral recruitment",# 0-1
            "alpha": "grazing term form"
            }
        self.parameter_range = {
            "r" : [0, 1],
            "d" : [0.02, 1.0],
            "a" : [0, 2],
            "f" : [0, 100],
            "s" : [0.01,1],
            "g" : [0.001, 2],
            "g1": [0.001, 5],
            "y" : [0, 2],
            "w" : [0, 20],
            "time" : [0,1], 
            "alpha" : [0.5, 2],
            }
        self.citation = "McManus, L. C., Watson, J. R., Vasconcelos, V. V., & Levin, S. A. (2019). Stability and recovery of coral-algae systems: the importance of recruitment seasonality and grazing influence. Theoretical Ecology, 12(1), 61-72."
        
    def ode(self, z, t):
        r"""
        setting up equations for Mcmanus et al. 2019.
        ..math::
            free space: F = 1 - z[0] - z[1] 
            coral: \frac{dC}{dt} = \underbrace{rTC}_{growth} - \underbrace{dC}_{mortality} - \underbrace{\alpha M C}_{M \, overgrows \, C} + \underbrace{(f \delta C + w(t)) T}_{recruitment}
            macroalgae:  \frac{dM}{dt} = \underbrace{\alpha M C}_{M \, overgrows \, C} - \underbrace{g(C)M}_{grazing} + \underbrace{\gamma M T}_{M \, overgrows \, T}

        """
        F = 1 - sum(z)
        C = z[0]
        M = z[1]

        # for linear, alpha = 1, concave, 0<alpha<1, convex alpha>1, constant g1==g 
        g = self.p.g + (self.p.g1 - self.p.g) * C**self.p.alpha

        growth = self.p.r * C * F
        mortality = self.p.d * C
        movergrowsc = self.p.a * C * M
        recruitment = ((self.p.f * self.p.s * C) + self.p.w) * F
        dCdt = growth - mortality - movergrowsc + recruitment
        
        mmovergrowsc = self.p.a * C * M
        grazing = g * M
        movergrowsf = self.p.y * F * M
        dMdt = mmovergrowsc - grazing + movergrowsf
       
        return[dCdt, dMdt]
