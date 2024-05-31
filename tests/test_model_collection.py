import pytest
import os
import sys
# make sure we use the devel version first
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__))+'/..')
sys.path.insert(0,"../reef_modeller")
from model_collection import *

class TestModelCollection():

    def test_construction(self):
        pytest.raises(Exception,CoralODELab)

    def test_set_times(self):
        model = CoralODELab("test")
        model.set_times([1,2])
    
    def test_set_start_conditions(self):
        model = CoralODELab("test")
        model.set_start_conditions([0,1])
            
    def test_plot_through_time(self):
        model = CoralODELab("test")
        model.plot_through_time()
