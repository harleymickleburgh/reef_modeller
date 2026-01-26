import sys
sys.path.insert(0,"../src")
import reef_modeller.fung as fung

coral_model = fung.FungCTMm()
coral_model.set_parameters(theta=0.3824)
coral_model.find_eq_points()
coral_model.plot_phase_space()

coral_model.plot_basins_3d()

coral_model.plot_cross_section()
