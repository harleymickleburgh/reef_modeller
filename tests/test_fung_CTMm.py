#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 13:25:58 2023

@author: kl909
"""

import pytest
import os
import sys
# make sure we use the devel version first
sys.path.insert(0,"../reef_modeller")
sys.path.insert(0,"reef_modeller")


from fungCTMm import *

class TestModelCollection:
    """Tests the model collection class"""
        
    def test_set_parameter(self):
        coralModel=fungCTMm()
        coralModel.set_parameter("theta" , 0.2)
        with pytest.raises(Exception):
            coralModel.set_parameter("theta", -0.21)

    def test_set_parameters(self):
        coralModel=fungCTMm()
        params = {
                "theta" : 0.2, #grazing pressure
                "dc" : 0.02, #coral mortality rate (yr^-1)
                "lbc" : 0.0009, #rate at which coral larvae, produced by local established brooding corals, recruit onto space (yr^-1)
                "lsc" : 0.00006, #rate at which exogenus spawning coral larvae recruit onto space (yr^-1)
                "rc" : 0.2, # lateral growth rate of corals over space (yr^-1)
                "gT" : 10, #maximum rate at which turf algae is grazed (yr^-1)
                "ac" : 0.25, #growth rate of corals over turf, relative to the rate over space
                "ec" : 0.1, #recruitment rate of corals onto turf, relative to the rate onto space 
                "sT" : 5, #growth rate of fine turf (occupying space) (yr^-1)
                "vm" : 0.9,
                "gm" : 3.5,
                "rm" : 0.35,
                "bm" : 0.9,
                "ymc" : 0.1,
                "ymt" : 0.1
                }
        coralModel.set_parameters(params)
        params["a"]= "banana"
        with pytest.raises(Exception):
            coralModel.set_parameters(params)
        params["a"]= -0.21
        with pytest.raises(Exception):
            coralModel.set_parameters(params)   
        params["a"]= 0.21
        params["banan"]= 0.21
        with pytest.raises(Exception):
            coralModel.set_parameters(params)
        params = "ikhbb"
        with pytest.raises(Exception):
            coralModel.set_parameters(params)        

    def test_set_start_conditions(self):
        coralModel=fungCTMm()
        start=[0.8,0.1, 0.1]
        coralModel.set_start_conditions(start)
        start = [-0.8, 0.2, 0.1]
        with pytest.raises(Exception):
            coralModel.set_start_conditions(start)
        start = [0.4, 0.4]
        with pytest.raises(Exception):
            coralModel.set_start_conditions(start)
        start = ["bob", "janet", 0.1]
        with pytest.raises(Exception):
            coralModel.set_start_conditions(start)
    
    def test_set_times(self):
        coralModel=fungCTMm()
        t = np.linspace(0,100, num = 100)
        coralModel.set_times(t.tolist())
        t = np.linspace(-10,100, num = 100)
        with pytest.raises(Exception):
            coralModel.set_times(t.tolist())
        t = np.linspace(100,10, num = 100)
        with pytest.raises(Exception):
            coralModel.set_times(t.tolist())
        #t = np.linspace("apple", 10, num = 100) # this one errors, because of np?
        # yes = linspace can't go from "apple" to 10
        t = ["apple", "banana", "orange"]
        with pytest.raises(Exception):
            coralModel.set_times(t.tolist())
            
    def test_ode(self):
          # set up the equations and check the ode function
          # gives same answer as a "by-hand" calculation from the paper equations
          start = [0.1, 0.6, 0.1]
          t = [0,1]
          parameters = {
                "theta" : 0.1, #grazing pressure
                "dc" : 0.1, #coral mortality rate (yr^-1)
                "lbc" : 0.1, #rate at which coral larvae, produced by local established brooding corals, recruit onto space (yr^-1)
                "lsc" : 0.1, #rate at which exogenus spawning coral larvae recruit onto space (yr^-1)
                "rc" : 0.1, # lateral growth rate of corals over space (yr^-1)
                "gT" : 0.1, #maximum rate at which turf algae is grazed (yr^-1)
                "ac" : 0.1, #growth rate of corals over turf, relative to the rate over space
                "ec" : 0.1, #recruitment rate of corals onto turf, relative to the rate onto space 
                "sT" : 0.1, #growth rate of fine turf (occupying space) (yr^-1)
                "vm" : 0.1,
                "gm" : 0.1,
                "rm" : 0.1,
                "bm" : 0.1,
                "ymc" : 0.1,
                "ymt": 0.1
                  }
          coralModel = fungCTMm()
          coralModel.set_times(t)
          coralModel.set_parameters(parameters)
          coralModel.set_start_conditions(start)
          test_output = coralModel.ode(start,t[1])
          # worked out 
          expected_dC = 0.03239876
          expected_dM = 0.01638324
          assert test_output[0] == pytest.approx(expected_dC)
          assert test_output[1] == pytest.approx(expected_dM)

    def test_solve_time(self):

        parameters = {
                "theta" : 0.7, #grazing pressure
                "dc" : 0.02, #coral mortality rate (yr^-1)
                "lbc" : 0.0009, #rate at which coral larvae, produced by local established brooding corals, recruit onto space (yr^-1)
                "lsc" : 0.00006, #rate at which exogenus spawning coral larvae recruit onto space (yr^-1)
                "rc" : 0.2, # lateral growth rate of corals over space (yr^-1)
                "gT" : 10, #maximum rate at which turf algae is grazed (yr^-1)
                "ac" : 0.25, #growth rate of corals over turf, relative to the rate over space
                "ec" : 0.1, #recruitment rate of corals onto turf, relative to the rate onto space 
                "sT" : 5, #growth rate of fine turf (occupying space) (yr^-1)
                "vm" : 0.9,
                "gm" : 3.5,
                "rm" : 0.35,
                "bm" : 0.9,
                "ymc" : 0.1,
                "ymt": 0.1
                }
        
        start = [0.2, 0.7, 0.1]
        t = [0,500]
        coralModel = fungCTMm()
        coralModel.set_times(t)
        coralModel.set_parameters(parameters)
        coralModel.set_start_conditions(start)
        coralModel.solve_time()
        test_output = coralModel.get_output()
        print(test_output)
        expected = [0.82773500, 0.0594409]
        assert test_output[-1,0] == pytest.approx(expected[0], 1e-4)
        assert test_output[-1,1] == pytest.approx(expected[1], 1e-4)

