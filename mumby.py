from .CoralODELab import CoralODELab
from types import SimpleNamespace

class Mumby(CoralODELab):

    def __init__(self):
        CoralODELab.__init__(self,"Mumby")
        self.num_parameters = 5
        self.num_eq = 2
        self.parameters = {
                "a": 0.1,
                "g": 0.3,
                "y": 0.77,
                "r": 0.55,
                "d": 0.24
                }
        self.p = SimpleNamespace(**self.parameters)        
        self.parameter_names = {
                "a": "overgrowth",
                "g": "grazing",
                "y": "growth rate, algae",
                "r": "recruitment, coral",
                "d": "mortatility, coral"
                }
        self.parameter_range = {
                "a": [0.01, 0.5],
                "g": [0.001, 0.5],
                "y": [0.1, 1],
                "r": [0.1, 0.9],
                "d": [0.01, 0.5]
                }
        self.citation = "Mumby, P.J., Hastings, A. and Edwards, H.J. (2007), Thresholds and the resilience of Caribbean coral reefs, Nature, Vol. 450 No. 7166, pp. 98–101."
    
    def ode(self, z, t):
        r"""
        Setting up the equations from Mumby et al. 2007 for turf, coral and macroalgae
        ..math::
        Turf = T
        Coral: \frac{dC}{dt} = \underbrace{rTC}_{recruitment \, growth} - \underbrace{dC}_{mortality} - \underbrace{\alpha MC}_{overgrowth\, by \,M}
        
        Macroalgae: \frac{dM}{dt} = \underbrace{\alpha MC}_{M \, overgrows \, C} - \underbrace{\frac{gM}{M+T}}_{grazed \, M \, becomes \, T} + \underbrace{\gamma MT}_{M \, spreads \, over \, T}
       
       
           """
        T = 1 - sum(z)
        C = z[0]
        M = z[1]
         
        #coral
        recruitmentC = self.p.r * T * C
        mortalityC = self.p.d * C
        Movergrowth = self.p.a * M * C
        dCdt = recruitmentC - mortalityC - Movergrowth
        
        # macroalgae
        MMovergrowth = self.p.a * M * C
        grazing = (self.p.g * M) / (M + T)
        growthM = self.p.y * M * T
        dMdt = MMovergrowth - grazing + growthM
        
    
        return[dCdt, dMdt]

