#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:15:03 2023

@author: kl909
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 10:56:18 2023

@author: kl909
"""

import unittest
import os
import sys
# make sure we use the devel version first
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__))+'/..')
from greiner import *

class TestModelCollection(unittest.TestCase):
    """Tests the model collection class"""
    def setUp(self):
        return

    def tearDown(self):
        return

        
    def test_set_parameter(self):
        coralModel=greiner()
        coralModel.set_parameter("g", 0.21)
        with self.assertRaises(Exception):
            coralModel.set_parameter("g", -0.21)

    def test_set_parameters(self):
        coralModel=greiner()
        params = {
                "r" : 0.55, #growth
                "d" : 0.24,# mortality 0.02 - 1.0
                "a" : 0.1,# coral overgrowth
                "g" : 0.77,# grazing (use fung?)
                "y" : 0.77, # turf overgrowth
                "lbc" : 0.0025, # divided elmhirst value of all coral recruitment 0.005
                "lsc" : 0.0025,
                "mlbc" : 0.0025,
                "mlsc" : 0.0025,
                }
        coralModel.set_parameters(params)
        params["a"]= "banana"
        with self.assertRaises(Exception):
            coralModel.set_parameters(params)
        params["a"]= -0.21
        with self.assertRaises(Exception):
            coralModel.set_parameters(params)   
        params["a"]= 0.21
        params["banan"]= 0.21
        with self.assertRaises(Exception):
            coralModel.set_parameters(params)
        params = "ikhbb"
        with self.assertRaises(Exception):
            coralModel.set_parameters(params)        

    def test_set_start_conditions(self):
        coralModel=greiner()
        start=[0.8,0.2]
        coralModel.set_start_conditions(start)
        start = [-0.8, 0.2]
        with self.assertRaises(Exception):
            coralModel.set_start_conditions(start)
        start = [0.4, 0.4, 0.4]
        with self.assertRaises(Exception):
            coralModel.set_start_conditions(start)
        start = ["bob", "janet"]
        with self.assertRaises(Exception):
            coralModel.set_start_conditions(start)
    
    def test_set_times(self):
        coralModel=greiner()
        t = np.linspace(0,100, num = 100)
        coralModel.set_times(t.tolist())
        t = np.linspace(-10,100, num = 100)
        with self.assertRaises(Exception):
            coralModel.set_times(t.tolist())
        t = np.linspace(100,10, num = 100)
        with self.assertRaises(Exception):
            coralModel.set_times(t.tolist())
        #t = np.linspace("apple", 10, num = 100) # this one errors, because of np?
        # yes = linspace can't go from "apple" to 10
        t = ["apple", "banana", "orange"]
        with self.assertRaises(Exception):
            coralModel.set_times(t.tolist())

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
        coralModel = greiner()
        coralModel.set_times(t)
        coralModel.set_parameters(parameters)
        coralModel.set_start_conditions(start)
        coralModel.solve_time()
        test_output = coralModel.get_output()
        expected = [0.563636, 0.0]
        self.assertAlmostEqual(test_output[-1,0],expected[0],5)
        self.assertAlmostEqual(test_output[-1,1],expected[1],5)
        
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
          coralModel = greiner()
          coralModel.set_times(t)
          coralModel.set_parameters(parameters)
          coralModel.set_start_conditions(start)
          test_output = coralModel.ode(start,t[1])
          # worked out 
          expected_dC = 0.0042
          expected_dM = 0.005088889
          self.assertAlmostEqual(test_output[0],expected_dC)
          self.assertAlmostEqual(test_output[1],expected_dM)
        

if __name__ == '__main__':
    unittest.main()
