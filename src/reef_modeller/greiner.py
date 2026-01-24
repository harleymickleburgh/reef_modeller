#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from CoralODELab import CoralODELab
from types import SimpleNamespace

class Greiner(CoralODELab):
    def __init__(self):
        CoralODELab.__init__(self,"Greiner")
        self.num_eq = 2
        self.num_parameters = 9
        self.parameters = {
            "r" : 0.55,    # growth
            "d" : 0.24,    # mortality 0.02 - 1.0
            "a" : 0.1,     # coral overgrowth
            "g" : 0.29,    # grazing (use fung?)
            "y" : 0.77,    # turf overgrowth
            "lbc" : 1.0,   # divided elmhirst value of all coral recruitment 0.005
            "lsc" : 0.00,  # external coral recruitment
            "mlbc" : 1.0,  # local algae recruitment
            "mlsc" : 0.00, # external algae recruitment
            }
        self.p = SimpleNamespace(**self.parameters) 
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
            "r" : [0.55,0.55],  # growth
            "d" : [0.24,0.24],  # mortality 0.02 - 1.0
            "a" : [0.1,0.1],    # coral overgrowth
            "g" : [0.01,0.99],    # grazing (use fung?)
            "y" : [0.77,0.77],  # turf overgrowth
            "lbc" : [0,1.0],    # divided elmhirst value of all coral recruitment 0.005
            "lsc" : [0.0,1.0],  # external coral recruitment
            "mlbc" : [0.0,1.0], # local algae recruitment
            "mlsc" : [0.0,1.0], # external algae recruitment

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
        
        T = 1 - sum(z)
        C = z[0]
        M = z[1]

        # this is internal recruitment, aka brooding corals
        growth = self.p.r * self.p.lbc * T * C
        mortalityC = self.p.d * C
        Movergrowth = self.p.a * M * C
        # External recruitment: note lsc term needs multiplying by C outside here
        # this includes self-seeding from floating gametes/larvae
        # that means the parameter lsc is actually the connectivity matrix x current C
        recruitment = self.p.r * self.p.lsc * T
        dCdt = growth - mortalityC - Movergrowth + recruitment
       
        # macroalgae (z(1))
        MMovergrowth = self.p.a * M * C
        if -1e-8 < M + T < 1e-8:
            grazing = 0 # or we get a divide by zero...
        else:
            grazing = (self.p.g * M) / (M + T)
        # this is internal recruitment, aka growth
        growthM1 = self.p.y * self.p.mlbc * M * T
        # External recruitment: note mlsc term need multiplying by z[1] outside here
        # that means the parameter mlsc is actually the connectivity matrix x current M
        # this includes self-seeding recruitment from floating gametes
        growthM2 = self.p.y * self.p.mlsc * T
        dMdt = MMovergrowth - grazing + growthM1 + growthM2
       
        return[dCdt, dMdt]
    
if __name__ == "__main__":
    # only run if called as a script, not imported
    start = [0.8, 0.2]
    t = np.linspace(0,55, num = 2)
    coralModel = greiner()
    coralModel.set_times(t.tolist())
    coralModel.set_start_conditions(start)
    coralModel.solve_time()
    coralModel.plot_through_time()
    
    


    # coralModel.set_parameter("g", 0.21)
    # coralModel.solve_time()
    # coralModel.plot_through_time()
    # print(coralModel.model_name)
    # print(coralModel.citation)

