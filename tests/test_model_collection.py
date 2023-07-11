import unittest
import os
import sys
# make sure we use the devel version first
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__))+'/..')
from model_collection import *

class TestModelCollection(unittest.TestCase):
    """Tests the model collection class"""
    def setUp(self):
        return

    def tearDown(self):
        return

    def test_construction(self):
        self.assertRaises(Exception,CoralODELab)

    def test_set_times(self):
        model = CoralODELab("test")
        model.set_times([1,2])
    
    def test_set_start_conditions(self):
        model = CoralODELab("test")
        model.set_start_conditions("test")
    
    def test_solve_time(self):
        model = CoralODELab("test")
        model.solve_time("test")
        
    def test_plot_through_time(self):
        model = CoralODELab("test")
        model.plot_through_time("test")
    
    def test_set_parameter(self):
        model = CoralODELab("test")
        model.set_parameter("test")
    
    def test_set_parameters(self):
        model = CoralODELab("test")
        model.set_parameters("test")

if __name__ == '__main__':
    unittest.main()
