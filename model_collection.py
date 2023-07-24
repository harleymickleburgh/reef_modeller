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

    def _check_value(self,number):

        if (type(number) == list):
            for l in number:
                if (not (type(l) == float or type(l) == int)):
                    raise Exception("Value entered in list is not an integer or float")
                if l < 0:
                    raise Exception("Value entered in list is negative, please insert positive number")
        elif (type(number) == float or type(number) == int):
            print(type(number))
            if number < 0:
                raise Exception("Value entered is negative, please insert positive number") 
        else:
            raise Exception("Value entered is not an integer or float") 



    def _check_length(self, my_list, expected_length, exact=False):

        if (not exact and len(my_list)<expected_length):
            raise Exception("Entered wrong number of parameters") # jon check
        if (exact and not (len(my_list) == expected_length)):
            raise Exception("Entered wrong number of parameters") # jon check

        return

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
        Set how many years the model will run for, enter first and last year, e.g (0,10) for 10 years
        
        :param times: number of years model is being run for
        :type times: list[float]
        
        """

        self._check_length(times,2)
        self._check_value(times)
        if (not sorted(times) == times):
            raise Exception("Times should be in ascending order")

        self.times = times
          

    def set_start_conditions(self, start_conditions):
        """
        S et the intial population cover of z(0) and z(1). Values must add up to 1
        
        :param start_conditions: list of values for the start of the model. 1 per equation
        :type start_conditions: list[float]
        
        """

        self._check_length(start_conditions,2,exact=True)
        self._check_value(start_conditions)
        
        if (sum(start_conditions) > 1):
            raise Exception("Sum of starting conditions should be between 0 and 1")

        self.start_conditions = start_conditions
            
            

    def solve_time(self):
        """
        Solves the ODE over the times specified by the user. Stores output in self.output

        :return: nothing
        
        """
        # run the scipy ode integrator
        self.output = odeint(self.ode, self.start_conditions, self.times)

        #not sure what this function does again --> dont think the user does anything here?

    def plot_through_time(self):
        """
        Plotting graph for population change (y axis) and time (x axis)
         
        """

        if (len(self.output) < 1):
            return

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
        
       # print(self.output[:,0], self.output[:,1])

    def set_parameter(self,name,value):
        """
        Set a single parameter by name

        :param name: name of the parameter to set
        :type name: string
        :param value: value of the parameter to set
        :type value: float


        """
        # add check that the name is in the paramter set
        try:
            self.parameters[name]
        except KeyError:
            raise Exception("Parameter name is not in the options list. See docs")

        self._check_value(value)

        self.parameters[name] = value
    
        #TODO if value not within range, fail (not set up ranges for all though) ("value is outside range")

    def set_parameters(self,new_parameters):
        """
        Set all parameters via a dictionary

        :param new_parameters: set of parameter values
        :type new_parameters: dictionary of names/value pairs
        """

        values = new_parameters.values()
        print(values)
        self._check_length(values,self.num_parameters,exact=True)
        self._check_value(list(values))
        keys = new_parameters.keys()
        expected_keys = self.parameters.keys()
        if (not (sorted(new_parameters.keys()) == sorted(self.parameters.keys()))):
            raise Exception("Parameters names do not match the options list. See docs")

        self.parameters = new_parameters
 
            
       # if value not within range, fail (not set up ranges for all though) ("value is outside range"):

    def get_output(self):
        return self.output
            
    # above are "set_" methods (setters). You normal have the "get_" equivalent (getter).
    # This means a user doesn't need to know the variable names in your class, they can call
    # the function instead. You, as API programmer, then also get to control what can be
    # set/get. 


