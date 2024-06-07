from coral_ode_lab import *

from scipy.optimize import fsolve


class Mumby(CoralODELab):

    def __init__(self):
        CoralODELab.__init__(self,"Mumby")
        self.num_parameters = 5
        self.parameters = {
                "a": 0.1,
                "g": 0.3,
                "y": 0.77,
                "r": 0.55,
                "d": 0.24
                }
        self.parameter_names = {
                "a": "overgrowth",
                "g": "grazing",
                "y": "growth rate, algae",
                "r": "recruitment, coral",
                "d": "mortatility, coral"
                }
        self.parameter_ranges = {
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
        T = 1 - z[0] - z[1]
         
        #coral (z(1))
        recruitmentC = self.parameters['r']*T*z[0]
        mortalityC = self.parameters['d']*z[0]
        Movergrowth = self.parameters['a']*z[1]*z[0]
        dCdt = recruitmentC - mortalityC - Movergrowth
        
        # macroalgae (z(2))
        MMovergrowth = self.parameters['a']*z[1]*z[0]
        grazing = (self.parameters['g']*z[1]) / (z[1] + T)
        growthM = self.parameters['y']*z[1]*T
        dMdt = MMovergrowth - grazing + growthM
        
    
        return[dCdt, dMdt]

       
if __name__ == "__main__":
    # only run if called as a script, not imported
    start = [0.2, 0.8]
    coralModel = Mumby()
    coralModel.set_start_conditions(start)

    eq = fsolve(coralModel.ode, start, args=(0))

    print(eq)
     
