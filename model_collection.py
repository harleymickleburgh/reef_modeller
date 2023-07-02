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
    """This is a top-level class to use as an inherit class for all other models. We use it
    to solve ODE sets to describe the interactions of coral-algae on reefs. 

    :param model_name: Name given to this mode
    :type name: string
    :param output: holder for the output of the solve
    :type output: list[float]
    """
    # TODO finish me

    def __init__(self, model):
        """Constructor method
        """
        self.model_name = model
        self.output = []
        self.times = []
        self.start_conditions = []
        self.parameters = {}
        self.num_paramers = 0
        self.citaiton = ""
        self.parameter_names = {}
        self.parameter_range = {}

        # internal variables
        self._coral_colour = "#F88379"
        self._malgae_colour = "#617D48"
        self._talgae_colour = "#5FC87E"

    # this forces you to create an ode function
    # in every class that inherits this one
    def ode(self, z, t):
        """
        Solve the ODE equation set.

        Return array of the dX/dt value for each ODE. Used by scipy.odeint

        :param z: List of starting conditions. One per ODE
        :type z: list[float]
        :raise: Exception if ODEs not implemented
        :return: delta values
        :rtype: list[float]
        
        """
        
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
        plt.plot(self.times, self.output[:,0], label="Coral", color=self._coral_colour)
        plt.plot(self.times, self.output[:,1], label="Algae", color=self._malgae_colour)
        plt.ylim(0,1)
        plt.xlim(-1)
        plt.legend()
        # TODO whata bout saving the image?
        plt.show()  
        # TODO what happens when there are three components? How could we manage that?

    def set_parameter(self,name,value):
        # add check that the name is in the paramter set
        self.parameters[name] = value

    def set_parameters(self,new_parameters):
        # TODO Add some checks that the keys are as you expect
        # the number of values is correct, etc
        self.parameters = parameters

    # above are "set_" methods (setters). You normal have the "get_" equivalent (getter).
    # This means a user doesn't need to know the variable names in your class, they can call
    # the function instead. You, as API programmer, then also get to control what can be
    # set/get. 


# TODO. Move this into it's own file. 
# do 
# import model_collection
# then you can keep the code and models a lot cleaner.
class Mumby(CoralODELab):

    def __init__(self):
        CoralODELab.__init__(self,"Mumby")
        self.num_parameters = 5
        self.parameters = {
                "a": 0.1,
                "g": 0.18976,
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
    print(coralModel.model_name)
    print(coralModel.citation)


     
