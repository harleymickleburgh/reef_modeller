#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
import os
import sys
from reef_modeller.mcmanus import Mcmanus

class TestModelMcmanus():
  
    def test_ode(self):
        # set up the manus equations and check the ode function
        # gives same answer as a "by-hand" calculation from the paper equations
        start = [0.5, 0.2]
        t = [0,1]
        parameters = {
            "r" : 0.1,
            "d" : 0.1,
            "a" : 0.1,
            "f" : 0.1,
            "s" : 0.1,
            "g" : 0.1,
            "g1": 0.1,
            "y" : 0.1,
            "w" : 0.1,
            "time" : 1,
            "alpha" : 1,
            }
        coralModel = Mcmanus()
        coralModel.set_times(t)
        coralModel.set_parameters(parameters)
        coralModel.set_start_conditions(start)
        test_output = coralModel.ode(start,t[1])
        # worked out 
        expected_dC = -0.0135
        expected_dM = -0.004
        assert test_output[0] == pytest.approx(expected_dC)
        assert test_output[1] == pytest.approx(expected_dM)

        # swap some params and try again
        coralModel.set_parameters(g1 = 0.5)
        coralModel.set_parameters(alpha = 0.5)
        coralModel.set_times(t)
        coralModel.set_start_conditions(start)
        test_output = coralModel.ode(start,t[1])
        expected_dC = -0.0135
        expected_dM = -0.060568542
        assert test_output[0] == pytest.approx(expected_dC)
        assert test_output[1] == pytest.approx(expected_dM)


