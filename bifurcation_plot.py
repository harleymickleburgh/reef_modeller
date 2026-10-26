
import sys
sys.path.insert(0,"../src")
import numpy as np
import matplotlib.pyplot as plt
import greiner

coral_model = greiner.greiner()
coral_model.plot_bifurcation("g")
