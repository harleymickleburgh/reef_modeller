#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coral-Algae ODE model based no Elmhirst et al 2009
"""
from types import SimpleNamespace
from CoralODELab import CoralODELab

class Elmhirst(CoralODELab):
    """
    Main class that set everything up
    """
    def __init__(self):
        CoralODELab.__init__(self,"elmhirst")
        self.num_parameters = 7
        self.num_eq = 2
        self.parameters = {
            "r" : 0.55, #growth
            "d" : 0.24,# mortality 0.02 - 1.0
            "a" : 0.1,# coral overgrowth
            "s" : 0.005, #coral recruitment
            "g" : 0.2,# grazing. beta in paper
            "y" : 0.77, # turf overgrowth
            "e" : 0.005, #algae recruitment
        }
        self.p = SimpleNamespace(**self.parameters)
        self.parameter_names = {
            "r" : "growth",
            "d" : "mortality", # 0.02 - 1.0
            "a" : "coral overgrowth",
            "s" : "coral recruitment",
            "g" : "grazing",
            "y" : "turf overgrowth",
            "e" : "algae recruitment",         
            }
        self.parameter_range = {
            "r" : [0,1],
            "d" : [0,1],
            "a" : [0,1],
            "s" : [0,1],
            "g" : [0,1],
            "y" : [0,1],
            "e" : [0,1],  
            }
        self.citation = "Elmhirst, T., Connolly, S. R., & Hughes, T. P. (2009). \
                Connectivity, regime shifts and the resilience of coral reefs. \
                Coral Reefs , 28(4), 949–957."

    def ode(self, z, t):
        r"""
        Setting up equations for Elmhirst et al. 2009
        .. math::
            turf: T = 1 - M - C
            coral: \frac{dC}{dt} = g(M,C) = \underbrace{C(rT)}_{growth} - 
            \underbrace{dC}_{mortality} - 
            \underbrace{\alpha MC}_{overgrowth \, by \, M} +
            \underbrace{\zeta T}_{recruitment}

            macroalgae: \frac{dM}{dt} = f(M,C) = \underbrace{\alpha MC}_{M \, overgrowing \, C} - 
            \underbrace{M(\frac{g}{M + T}_{grazing} + 
            \underbrace{\gamma T)}_{M \, overgrows \, T} + 
            \underbrace{\epsilon T}_{recruitment}
        """
        T = 1 - sum(z)
        C = z[0]
        M = z[1]

        growth = C * (self.p.r * T)
        mortality = self.p.d * C
        overgrowth_m = self.p.a * M * C
        recruitment = self.p.s * T
        dCdt = growth - mortality - overgrowth_m + recruitment

        m_over_grows_c = self.p.a * M * C
        grazing = M * (self.p.g / (M + T))
        m_over_grows_t = self.p.y * M * T
        m_recruitment = self.p.e * T
        dMdt = m_over_grows_c - grazing + m_over_grows_t + m_recruitment

        return [dCdt, dMdt]
