#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:15:03 2023

@author: kl909
"""

import pytest
import os
import sys
from reef_modeller.greiner import Greiner

class TestModelGreiner():

    def test_solve_time(self):
        # set up the equations such that the dc/dt and dm/dt are small
        # and the solver (which alters it's internal timestep) and a calculation
        # by hand are roughly the same to 4 DP
        # Griener et al 2022 fig 2a

        parameters = {
                "r" : 0.55, #growth
                "d" : 0.24,# mortality 0.02 - 1.0
                "a" : 0.1,# coral overgrowth
                "g" : 0.8,# grazing (use fung?)
                "y" : 0.77, # turf overgrowth
                "lbc" : 1, 
                "lsc" : 0.0, # so we don't have to worry about multiplying by C
                "mlbc" : 1,
                "mlsc" : 0,
                }
        
        start = [0.8, 0]
        t = [0,500]
        coralModel = Greiner()
        coralModel.set_times(t)
        coralModel.set_parameters(parameters)
        coralModel.set_start_conditions(start)
        coralModel.solve_time()
        test_output = coralModel.get_output()
        expected = [0.563636, 0.0]
        assert test_output[-1,0] == pytest.approx(expected[0])
        assert test_output[-1,1] == pytest.approx(expected[1])
        
    def test_ode(self):
          # set up the mumby equations and check the ode function
          # gives same answer as a "by-hand" calculation from the paper equations
          start = [0.1, 0.1]
          t = [0,1]
          parameters = {
                "r" : 0.1, #growth
                "d" : 0.1,# mortality 0.02 - 1.0
                "a" : 0.1,# coral overgrowth
                "g" : 0.1,# grazing (use fung?)
                "y" : 0.1, # turf overgrowth
                "lbc" : 0.9, # divided elmhirst value of all coral recruitment 0.005
                "lsc" : 0.1,
                "mlbc" : 0.9,
                "mlsc" : 0.1,
                  }
          coralModel = Greiner()
          coralModel.set_times(t)
          coralModel.set_parameters(parameters)
          coralModel.set_start_conditions(start)
          test_output = coralModel.ode(start,t[1])
          # worked out 
          expected_dC = 0.0042
          expected_dM = 0.005088889
          assert test_output[0] ==  pytest.approx(expected_dC)
          assert test_output[1] == pytest.approx(expected_dM)
        
