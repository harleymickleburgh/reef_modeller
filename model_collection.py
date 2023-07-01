#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 14:11:11 2023

@author: kl909
"""
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot

class CoralODELab:
    def __init__(self, model):
        self.model_name = model
        self.output = []
        self.times = []
        self.start_conditions = []
        self.parameters = {}
        self.num_paramers = 0

    # this forces you to create an ode function
    # in every class that inherits this one
    def ode(self):
        raise Exception("Not Implemented")

    def set_times(self,times):
        self.times = times

    def set_start_conditions(self, start_conditions):
        self.start_conditions = start_conditions

    def solve_time(self):
        # run the scipy ode integrator
        self.output = odeint(self.ode, self.start_conditions, self.times)

    def plot_through_time(self):
        # plot the results
        plt.plot(self.times, self.output[:,0], label="Coral")
        plt.plot(self.times, self.output[:,1], label="Algae")
        plt.ylim(0,1)
        plt.xlim(-1)
        plt.legend()
        plt.show()  

    def set_parameter(self,name,value):
        self.parameters[name] = value

    def set_parameters(self,new_parameters):
        self.parameters = parameters



class Mumby(CoralODELab):

    def __init__(self):
        CoralODELab.__init__(self,"Mumby")
        self.num_parameters = 5
        self.parameters = {
                "a": 0.1,
                "g": 0.18976,
                "y": 0.77,
                "r": 0.55,
                "d": 0.24}
    
    def ode(self, z, t):
     
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
    start = [0.8, 0.2]
    t = np.linspace(0,100, num = 100)
    coralModel = Mumby()
    coralModel.set_times(t)
    coralModel.set_start_conditions(start)
    coralModel.solve_time()
    coralModel.plot_through_time()

    coralModel.set_parameter("g", 0.21)
    coralModel.solve_time()
    coralModel.plot_through_time()


     
