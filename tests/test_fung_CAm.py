#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 13:25:58 2023

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
from fungCAm import *

class TestModelCollection(unittest.TestCase):
    """Tests the model collection class"""
    def setUp(self):
        return

    def tearDown(self):
        return

        
    def test_set_parameter(self):
        coralModel=fungCAm()
        coralModel.set_parameter("theta" , 0.2)
        with self.assertRaises(Exception):
            coralModel.set_parameter("theta", -0.21)

    def test_set_parameters(self):
        coralModel=fungCAm()
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
        coralModel=fungCAm()
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
        coralModel=fungCAm()
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
        # set up the fungCAm equations such that the dc/dt and dm/dt are small
        # and the solver (which alters it's internal timestep) and a calculation
        # by hand are roughly the same to 4 DP
        start = [0.1, 0.00001]
        t = [0,1]
        parameters = {
                "theta" : 0.4, #grazing pressure
                "dc" : 0.02, #coral mortality rate (yr^-1)
                "lbc" : 0.5, #rate at which coral larvae, produced by local established brooding corals, recruit onto space (yr^-1)
                "lsc" : 0.01, #rate at which exogenus spawning coral larvae recruit onto space (yr^-1)
                "rc" : 0.04, # lateral growth rate of corals over space (yr^-1)
                "gT" : 5, #maximum rate at which turf algae is grazed (yr^-1)
                "ac" : 0.01, #growth rate of corals over turf, relative to the rate over space
                "ec" : 0.05, #recruitment rate of corals onto turf, relative to the rate onto space 
                "sT" : 2, #growth rate of fine turf (occupying space) (yr^-1)
                "vm" : 0.01,
                "gm" : 0.2,
                "rm" : 0.05,
                "bm" : 0.2,
                "ymc" : 0.01,
                }
        
        coralModel = fungCAm()
        coralModel.set_times(t)
        coralModel.set_parameters(parameters)
        coralModel.set_start_conditions(start)
        coralModel.solve_time()
        output = coralModel.get_output()
        print(output)
        # worked out 
        # expectedC = start[0] - 4.28378806180052E-05
        # expectedM = start[1] - 1.29167633246533E-06
        # self.assertAlmostEqual(output[-1,0],expectedC,places=4)
        # self.assertAlmostEqual(output[-1,1],expectedM,places=4)
        

if __name__ == '__main__':
    unittest.main()
