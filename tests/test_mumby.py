#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
import os
import sys
# make sure we use the devel version first
sys.path.insert(0,"../src/reef_modeller/")
from mumby import Mumby

class TestModelMumby():
  
    def test_ode(self):
        # set up the mumby equations and check the ode function
        # gives same answer as a "by-hand" calculation from the paper equations
        start = [0.5636363, 0.00001]
        t = [0,1]
        parameters = {
                "a": 0.1,
                "g": 0.1,
                "y": 0.1,
                "r": 0.229,
                "d": 0.1
                }
        coralModel = Mumby()
        coralModel.set_times(t)
        coralModel.set_parameters(parameters)
        coralModel.set_start_conditions(start)
        test_output = coralModel.ode(start,t[1])
        # worked out 
        expected_dC = -4.28378806180052E-05
        expected_dM = -1.29167633246533E-06
        assert test_output[0] == pytest.approx(expected_dC)
        assert test_output[1] == pytest.approx(expected_dM)


    def test_solve_time(self):
        # test the equations solver to a known steady steate taken from the paper
        # run for a long time (500 years!) to make sure we get there.
        parameters = {
                "a": 0.08,
                "g": 0.5,
                "y": 0.77,
                "r": 0.55,
                "d": 0.24
                }
        start = [0.1, 0.6]
        t = [0,500]
        coralModel = Mumby()
        coralModel.set_times(t)
        coralModel.set_parameters(parameters)
        coralModel.set_start_conditions(start)
        coralModel.solve_time()
        test_output = coralModel.get_output()
        expected = [0.56363635, 0.0000000]
        assert test_output[-1,0] == pytest.approx(expected[0])
        assert test_output[-1,1] == pytest.approx(expected[1])

