#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This class is the underlaying class for all ODE models
   It has the minimum params, etc set and functions to solve and
   plot data
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import fsolve

class CoralODELab: # pylint: disable=invalid-name
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
        self.num_eq = 0
        self.citation = ""
        self.parameter_names = {}
        self.parameter_range = {}
        self.coral_cover = 0
        self.macroalgae_cover = 0
        self.turfalgae_cover = 0
        self.p = False

        # internal variables
        self._coral_colour  = "#F88379"
        self._malgae_colour = "#617D48"
        self._algae_colour  = "#617D48"
        self._talgae_colour = "#5FC87E"
        self._space_colour  = "#9aa69d"

    def _check_value(self,number):

        if isinstance(number,list):
            for l in number:
                if not isinstance(l, (float, int)):
                    raise TypeError("Value entered in list is not an integer or float")
                if l < 0:
                    raise ValueError("Value entered in list is negative, \
                                    please insert positive number")
        elif isinstance(number, (float, int)):
            if number < 0:
                raise ValueError("Value entered is negative, please insert positive number")
        else:
            raise TypeError("Value entered is not an integer or float")


    def _check_length(self, my_list, expected_length):

        if len(my_list) != expected_length:
            raise TypeError("Entered wrong number of parameters")


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

        raise NotImplementedError

    def set_times(self,times):
        """
        Set how many years the model will run for, enter first and last year, 
        e.g (0,10) for 10 years
        
        :param times: number of years model is being run for
        :type times: list[float]
        
        """

        self._check_length(times,2)
        self._check_value(times)
        if not sorted(times) == times:
            raise ValueError("Times should be in ascending order")

        self.times = np.arange(times[0], times[1]+1, 1)


    def set_start_conditions(self, start_conditions):
        """
        Set the intial population cover of z(0) and z(1) (and z(2)). Values must add up to 1
        
        :param start_conditions: list of values for the start of the model. 1 per equation
        :type start_conditions: list[float]
        
        """

        self._check_length(start_conditions,self.num_eq)
        self._check_value(start_conditions)

        if sum(start_conditions) > 1:
            raise ValueError("Sum of starting conditions should be between 0 and 1")

        self.start_conditions = start_conditions
        self.coral_cover = start_conditions[0]
        self.macroalgae_cover = start_conditions[1]
        if self.num_eq == 3:
            self.turfalgae_cover = start_conditions[2]

    def solve_time(self, start=None):
        """
        Solves the ODE over the times specified by the user. Stores output in self.output

        :return: self.output
        
        """
        if start is None:
            start = self.start_conditions
        # run the scipy ode integrator
        self.output = odeint(self.ode, start, self.times)

        # set a limit of outputs to be between 0 and 1
        self.output = np.clip(self.output, 0, 1)

        self.coral_cover = self.output[-1][0]
        self.macroalgae_cover = self.output[-1][1]
        if self.num_eq == 3:
            self.turfalgae_cover = self.output[-1][2]

        return self.output


    def plot_through_time(self, filename=None):
        """
        Plotting graph for population change (y axis) and time (x axis)
         
        """

        if len(self.output) < 1:
            return

        # plot the results
        plt.plot(self.times, self.output[:,0], label="Coral", color=self._coral_colour)
        if self.num_eq == 2:
            plt.plot(self.times, self.output[:,1], label="Algae", color=self._malgae_colour)
        elif self.num_eq == 3:
            plt.plot(self.times, self.output[:,1], label="Turf algae", color=self._talgae_colour)
            plt.plot(self.times, self.output[:,2], label="Macroalgae", color=self._malgae_colour)

        plt.ylim(0,1)
        plt.xlim(-1)
        plt.legend()
        plt.title(self.model_name)
        plt.xlabel('Time (years)')
        plt.ylabel('% cover')
        if filename is None:
            plt.show()
        else:
            #save figure
            pass

    def plot_bifurcation(self, parameter):
        """
        Create a bifurcation plot, with coral on the y axis 
        and the parameter on the x axis. 
        """

        # get parameter range
        param_range = np.linspace(self.parameter_range[parameter][0],
                                  self.parameter_range[parameter][1], 151)

        all_roots = []
        types = []
        # loop through param range
        for p in param_range:
            self.set_parameters(**{parameter: p})
            # find roots and remove unstable ones (saddles and stable)
            roots, type_root = self.find_eq_points()
            all_roots.append(roots)
            types.append(type_root)

        # will have to plot as points
        for rr, tr, p in zip(all_roots, types, param_range):
            for r, t in zip(rr, tr):
                if t == -1:
                    plt.plot(p, r[0], 'sr', markersize=3)
                elif t == 0:
                    plt.plot(p, r[0], 'sb', markersize=3)
                else:
                    plt.plot(p, r[0], 'sm', markersize=3)
        #plt.ylim(0,1)
        plt.xlim(param_range[0], param_range[-1])
        plt.xlabel(parameter)
        plt.ylabel('% cover')
        plt.show()


    def find_eq_points(self):
        """
        find the location of the equilibirum points in phase space.
        These can be unstable or stable saddle points in the phase plot
        """
        coral_counter = 0
        start_conditions = []
        # create set of starting conditions
        # bounds will always be [0, 1] and can only sum to 1
        for coral in np.linspace(0.1,1,20):
            for algae in np.linspace(0.1, 1-coral-1e-6, 20-coral_counter):
                start_conditions.append([coral,algae/2,algae/2])
            coral_counter += 1

        all_roots = []
        stability = []
        for init in start_conditions:
            # workout the stability points
            roots, infodict, ier, mesg = fsolve(self.ode, init, args=(0), full_output = True)
            if ier not in [1, 2, 3, 4]:
                raise RuntimeError(f"Solver failed with message: {mesg}")
            matrixr=np.zeros((self.num_eq, self.num_eq))  # dim= number of linear equations
            matrixr[np.triu_indices(self.num_eq)]=infodict["r"]  # to unpack "r" into matrix
            Jacobian=(infodict["fjac"].T).dot(matrixr) # needs .T to get Q
            if np.isnan(Jacobian).any():
                stability.append(-1)
                continue
            eigenvalues=np.array(np.linalg.eigvals(Jacobian))
            all_roots.append(roots)
            # work out stability of that root
            if isinstance(eigenvalues[0], complex):
                if np.any(eigenvalues.real >= 0):
                    stability.append(-1)
                else:
                    stability.append(1)
            else:
                if np.all(eigenvalues > 0):
                    stability.append(-1)
                elif np.all(eigenvalues < 0):
                    stability.append(1)
                else:
                    stability.append(0)

        all_roots = np.array(all_roots)
        # make small numbers zero in the roots
        tol = 1e-10
        all_roots[abs(all_roots) < tol] = 0.0
        all_roots = all_roots.round(decimals=8)
        stability = np.array(stability)

        unique_roots = np.unique(all_roots,axis=0)
        #remove any where the root < 0
        unique_roots = unique_roots[np.all(unique_roots >= 0, axis=1)]
        root_stability_type = []
        # the stability is the minimum for all stabilities for each unqie root
        for root in unique_roots:
            indicies = np.where(np.all(root == all_roots,axis=1))
            stab_for_root = np.min(stability[np.array(indicies[0])])
            root_stability_type.append(stab_for_root)

        return(unique_roots, root_stability_type)

    def plot_phase_space(self):
        """
        Plot the phase space of coral and algae. Arrows show the direction
        of the phase space. Points indicate saddle points
        """

        coral_counter = 0
        start_conditions = []
        # create set of starting conditions
        # bounds will always be [0, 1] and can only sum to 1
        for coral in np.linspace(0.1,1,20):
            for algae in np.linspace(0.1, 1-coral-1e-6, 20-coral_counter):
                start_conditions.append([coral,algae])
            coral_counter += 1

        # solve for 100 years and create solution
        self.set_times([0, 100])
        dx = 0.001
        sol=[ self.solve_time(start=init) for init in start_conditions]
        for solution in sol:
            plt.plot(solution[:,0], solution[:,1],"k",alpha=0.5,linewidth=0.5)
            plt.arrow(solution[1,0], solution[1,1],
                      dx*(solution[2,0]-solution[1,0]),
                      dx*(solution[2,1]-solution[1,1]),
                      shape='full', lw=0, color="k", alpha=0.5,
                      length_includes_head=True, head_width=.015)
        roots, type_root = self.find_eq_points()
        for rr, tr in zip(roots, type_root):
            if tr == -1:
                plt.plot(rr[0], rr[1], 'or', markersize=7)
            elif tr == 0:
                plt.plot(rr[0], rr[1], 'ob', markersize=7)
            else:
                plt.plot(rr[0], rr[1], 'om', markersize=7)
        plt.ylim(0,1)
        plt.xlim(0,1)
        plt.xlabel('Coral')
        plt.ylabel('Algae')
        plt.show()

    def set_parameters(self, new_params=None, **kwargs):
        """
        Update parameters via a dictionary or keyword arguments.
        Usage: 
            model.set_parameters({'rc': 0.8})
            model.set_parameters(rc=0.8, theta=0.2)
        """
        # Combine dictionary and keyword arguments
        # note keyword arguments "win"
        updates = new_params if isinstance(new_params, dict) else {}
        updates.update(kwargs)

        # now update
        for key, value in updates.items():
            if hasattr(self.p, key):
                # check value:
                if not self.parameter_range[key][0] <= value <= self.parameter_range[key][1]:
                    print(f"Warning: Parameter '{key}' has a value outside the range. \
                            Setting anyway")
                setattr(self.p, key, value)
            else:
                print(f"Warning: Parameter '{key}' not found in model.")

    def get_output(self):
        """
        Return the output from the model
        """
        return self.output
