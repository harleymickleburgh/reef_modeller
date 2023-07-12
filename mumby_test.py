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
from mumby import *

class TestModelCollection(unittest.TestCase):
    """Tests the model collection class"""
    def setUp(self):
        return

    def tearDown(self):
        return

        
    def test_set_parameter(self):
        coralModel=Mumby()
        coralModel.set_parameter("g", 0.21)
        with self.assertRaises(Exception):
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
        coralModel=Mumby()
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
        coralModel=Mumby()
        t = np.linspace(0,100, num = 100)
        coralModel.set_times(t.tolist())
        t = np.linspace(-10,100, num = 100)
        with self.assertRaises(Exception):
            coralModel.set_times(t.tolist())
        t = np.linspace(100,10, num = 100)
        with self.assertRaises(Exception):
            coralModel.set_times(t.tolist())
        t = np.linspace("apple", 10, num = 100) # this one errors, because of np?
        with self.assertRaises(Exception):
            coralModel.set_times(t.tolist())
        
        

if __name__ == '__main__':
    unittest.main()