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

    :param model_name: Name given to this model
    :type name: string
    :param output: holder for the output of the solver
    :type output: list[float]
    :param times: number of years model is being run for
    :type times: list[float]
    :param start_conditions: inital population of z(0) (coral) and z(1) (algae) adding up to 1
    :type start_conditions: list[float]
    :param parameters: variable names and value
    :type parameters: dictionary[string:int]
    :param num_parameters: total number of parameters in model
    :type num_parameters: [int]
    :param citation: full citation of paper model was extracted from
    :type param: [string]
    :param parameter_names: definition of each parameter symbol
    :type parameter_names: dictionary[string:string]
    :param parameter_range: values each parameter can be observed at
    :type parameter_range: dict[string: range]
    
    """
   

    def __init__(self, model):
        """Constructor method
        """
        self.model_name = model
        self.output = []
        self.times = []
        self.start_conditions = []
        self.parameters = {}
        self.num_parameters = 0
        self.citation = ""
        self.parameter_names = {}
        self.parameter_range = {}

        # internal variables
        self._coral_colour = "#F88379"
        self._malgae_colour = "#617D48"
        self._talgae_colour = "#5FC87E"

    # this forces you to create an ode function
    # in every class that inherits this one
    def ode(self, z, t): # ode gets changed to whatever model is being run
        """
        Solve the ODE equation set.

        Return array of the dX/dt value for each ODE. Used by scipy.odeint

        :param z: List of starting conditions. One per ODE
        :type z: list[float]
        :param t: list of years ODE is run for
        :type t: list[float]
        :raise: Exception if ODEs not implemented
        :return: delta values
        :rtype: list[float]
        
        """
        
        raise Exception("Not Implemented")

    def set_times(self,times):
        """
        Set how many years the model will run for 
        
        :param times: number of years model is being run for
        :type times: list[float]
        
        """

        self.times = times


    def set_start_conditions(self, start_conditions):
        """
        Set the intial population cover of z(0) and z(1). Values must add up to 1
        
        :param start_conditions: list of values for the start of the model. 1 per equation
        :type start_conditions: list[float]
        
        """
        self.start_conditions = start_conditions

    def solve_time(self):
        """
        Solves the ODE over the times specified by the user. Stores output in self.output

        :return: nothing
        
        """
        # run the scipy ode integrator
        self.output = odeint(self.ode, self.start_conditions, self.times)


    def plot_through_time(self):
        """
        Plotting graph for population change (y axis) and time (x axis)
        
        """
        # plot the results
        plt.plot(self.times, self.output[:,0], label="Coral", color=self._coral_colour)
        plt.plot(self.times, self.output[:,1], label="Algae", color=self._malgae_colour)
        plt.ylim(0,1)
        plt.xlim(-1)
        plt.legend()
        plt.title(self.model_name)
        plt.xlabel('Time (years)')
        plt.ylabel('Population')
        # TODO whata bout saving the image?
        plt.show()  
        # TODO what happens when there are three components? How could we manage that?

    def set_parameter(self,name,value):
        """
        Set a single parameter by name

        :param name: name of the parameter to set
        :type name: string
        :param value: value of the parameter to set
        :type value: float


        """
        # add check that the name is in the paramter set
        self.parameters[name] = value

    def set_parameters(self,new_parameters):
        """
        Set all parameters via a dictionary

        :param new_parameters: set of parameter values
        :type new_parameters: dictionary of names/value pairs
        """

        # TODO Add some checks that the keys are as you expect
        # the number of values is correct, etc
        self.parameters = parameters

    # above are "set_" methods (setters). You normal have the "get_" equivalent (getter).
    # This means a user doesn't need to know the variable names in your class, they can call
    # the function instead. You, as API programmer, then also get to control what can be
    # set/get. 


