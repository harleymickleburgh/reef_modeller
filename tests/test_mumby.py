#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 10:56:18 2023

@author: kl909
"""

import pytest
import os
import sys
# make sure we use the devel version first
sys.path.insert(0,"../src/reef_modeller/")
from mumby import Mumby

class TestModelCollection():
        
    def test_set_parameter(self):
        coralModel=Mumby()
        coralModel.set_parameter("g", 0.21)
        with pytest.raises(Exception):
            coralModel.set_parameter("g", -0.21)

    def test_set_parameters(self):
        coralModel=Mumby()
        params = {
                "a": 0.1,
                "g": 0.8,
                "y": 0.77,
                "r": 0.55,
                "d": 0.24
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
        coralModel=Mumby()
        start=[0.8,0.2]
        coralModel.set_start_conditions(start)
        start = [-0.8, 0.2]
        with pytest.raises(Exception):
            coralModel.set_start_conditions(start)
        start = [0.4, 0.4, 0.4]
        with pytest.raises(Exception):
            coralModel.set_start_conditions(start)
        start = ["bob", "janet"]
        with pytest.raises(Exception):
            coralModel.set_start_conditions(start)
    
    def test_set_times(self):
        coralModel=Mumby()
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

