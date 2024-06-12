
import sys
sys.path.insert(0,"../")
import numpy as np
import matplotlib.pyplot as plt
import reef_modeller.greiner

coral_model = reef_modeller.greiner.greiner()
coral_model.find_eq_points()
coral_model.plot_phase_space()
