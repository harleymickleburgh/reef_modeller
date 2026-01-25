
import sys
sys.path.insert(0,"../src")
import numpy as np
import matplotlib.pyplot as plt
import greiner

coral_model = greiner.greiner()
coral_model.set_parameter("g",0.3824)
coral_model.find_eq_points()
coral_model.plot_phase_space()
