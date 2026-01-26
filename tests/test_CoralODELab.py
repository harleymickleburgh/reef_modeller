import pytest
import os
import sys
from reef_modeller.CoralODELab import *
from reef_modeller.mumby import Mumby

@pytest.fixture
def model(scope='class'):
    """Fixture to initialize the model for each test."""
    # Mock parameter ranges for the setter test
    m = Mumby()
    ranges = {k: [0, 1] for k in m.parameters.keys()}    
    m.parameter_ranges = ranges
    m.num_eq = 2
    return m

class TestCoralODELab():

    def test_construction(self):
        pytest.raises(Exception,CoralODELab)

    def test_set_times(self, model):
        model.set_times([1,2])
    
    def test_set_start_conditions(self, model):
        model.set_start_conditions([0,1])
            
    def test_set_parameters_valid(self, model):
        """Test that valid parameters are updated correctly."""
        model.set_parameters(d=0.8)
        assert model.p.d == 0.8
        model.set_parameters({"d":0.9})
        assert model.p.d == 0.9


    def test_set_parameters_out_of_range(self, model, capsys):
        """Test that out-of-range parameters trigger a warning."""
        model.set_parameters(d=5.0) # Outside [0, 1]
        captured = capsys.readouterr()
        assert "outside the range" in captured.out

    def test_stability_classification(self, model):
        """Test the eigenvalue classification logic."""
                
        # Case 1: Stable Node (All negative real)
        assert model.classify_stability(np.array([-1, -2, -0.5])) == "Stable Node"
        
        # Case 2: Saddle (Mixed signs)
        assert "Saddle" in model.classify_stability(np.array([-1, 0.5, -0.5]))
        
        # Case 3: Stable Focus (Negative real with imaginary)
        assert model.classify_stability(np.array([-1+1j, -1-1j, -2])) == "Stable Focus"

    def test_ode_dimensions(self, model):
        """Ensure ODE returns a list of the correct length."""
        derivative = model.ode([0.5, 0.2], 0)
        assert len(derivative) == model.num_eq
