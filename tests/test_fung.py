#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
import os
import sys
# make sure we use the devel version first
sys.path.insert(0,"../src/reef_modeller")

from fung import FungCTMm
from fung import FungCAm

class TestFungModels:
            
    def test_ode_ctm(self):
          # set up the equations and check the ode function
          # gives same answer as a "by-hand" calculation from the paper equations
          start = [0.1, 0.1, 0.1]
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
                "gm" : 0.1,
                "rm" : 0.1,
                "bm" : 0.1,
                "ymc" : 0.1,
                "ymt": 0.1
                  }
          coralModel = FungCTMm()
          coralModel.set_times(t)
          coralModel.set_parameters(parameters)
          coralModel.set_start_conditions(start)
          test_output = coralModel.ode(start,t[1])
          print(test_output)
          # worked out 
          expected_dC = 0.075029
          expected_dT = 0.060701
          expected_dM = 0.0062
          assert test_output[0] == pytest.approx(expected_dC)
          assert test_output[1] == pytest.approx(expected_dT)
          assert test_output[2] == pytest.approx(expected_dM)


    def test_solve_time_ctm(self):

        parameters = {
                "theta" : 0.7, #grazing pressure
                "dc" : 0.05, #coral mortality rate (yr^-1)
                "lbc" : 0.0009, #rate at which coral larvae, produced by local established brooding corals, recruit onto space (yr^-1)
                "lsc" : 0.00006, #rate at which exogenus spawning coral larvae recruit onto space (yr^-1)
                "rc" : 0.2, # lateral growth rate of corals over space (yr^-1)
                "gT" : 10, #maximum rate at which turf algae is grazed (yr^-1)
                "ac" : 0.25, #growth rate of corals over turf, relative to the rate over space
                "ec" : 0.1, #recruitment rate of corals onto turf, relative to the rate onto space 
                "sT" : 5, #growth rate of fine turf (occupying space) (yr^-1)
                "gm" : 0.5,
                "rm" : 0.35,
                "bm" : 0.9,
                "ymc" : 0.1,
                "ymt": 0.1
                }
        
        start = [0.2, 0.7, 0.1]
        t = [0,500]
        coralModel = FungCTMm()
        coralModel.set_times(t)
        coralModel.set_parameters(parameters)
        coralModel.set_start_conditions(start)
        coralModel.solve_time()
        test_output = coralModel.get_output()
        expected = [0.7134, 0.0503, 0.0]
        assert test_output[-1,0] == pytest.approx(expected[0], abs=1e-4)
        assert test_output[-1,1] == pytest.approx(expected[1], abs=1e-4)
        assert test_output[-1,2] == pytest.approx(expected[2], abs=1e-4)

            
    def test_ode_cam(self):
          # set up the equations and check the ode function
          # gives same answer as a "by-hand" calculation from the paper equations
          start = [0.1, 0.6]
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
                  }
          coralModel = FungCAm()
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
                }
        
        start = [0.2, 0.8]
        t = [0,500]
        coralModel = FungCAm()
        coralModel.set_times(t)
        coralModel.set_parameters(parameters)
        coralModel.set_start_conditions(start)
        coralModel.solve_time()
        test_output = coralModel.get_output()
        expected = [0.82773500, 0.0594409]
        assert test_output[-1,0] == pytest.approx(expected[0], 1e-4)
        assert test_output[-1,1] == pytest.approx(expected[1], 1e-4)

