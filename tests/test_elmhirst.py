#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
import os
import sys
# make sure we use the devel version first
sys.path.insert(0,"../src/reef_modeller/")

from elmhirst import Elmhirst

class TestModelElmhirst():

    def test_solve_time(self):
        # by hand are roughly the same to 4 DP
        # Griener et al 2022 fig 2a

        parameters = {
                "r" : 0.55, #growth
                "d" : 0.24,# mortality 0.02 - 1.0
                "a" : 0.1,# coral overgrowth
                "g" : 0.8,# grazing (use fung?)
                "y" : 0.77, # turf overgrowth
                "s" : 0.005,
                "e" : 0.005
                }
        
        start = [0.8, 0]
        t = [0,500]
        coralModel = Elmhirst()
        coralModel.set_times(t)
        coralModel.set_parameters(parameters)
        coralModel.set_start_conditions(start)
        coralModel.solve_time()
        test_output = coralModel.get_output()
        expected = [0.563636, 0.0]
        assert test_output[-1,0] == pytest.approx(expected[0])
        assert test_output[-1,1] == pytest.approx(expected[1])
        
    def test_ode(self):
          start = [0.1, 0.1]
          t = [0,1]
          parameters = {
                "r" : 0.1, #growth
                "d" : 0.1,# mortality 0.02 - 1.0
                "a" : 0.1,# coral overgrowth
                "g" : 0.1,# grazing (use fung?)
                "y" : 0.1, # turf overgrowth
                "s" : 0.1,
                "e" : 0.1
                  }
          coralModel = Elmhirst()
          coralModel.set_times(t)
          coralModel.set_parameters(parameters)
          coralModel.set_start_conditions(start)
          test_output = coralModel.ode(start,t[1])
          # worked out 
          expected_dC = 0.0042
          expected_dM = 0.005088889
          assert test_output[0] ==  pytest.approx(expected_dC)
          assert test_output[1] == pytest.approx(expected_dM)
        
