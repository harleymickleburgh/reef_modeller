#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jh1889
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from reef_modeller.CoralODELab import *

class ReefModel():

    def __init__(self):
        connectivity_matrix = None
        model_type = None
        n_sites = None
        reef_model = None
        years = None

    def load_connectivity_matrix(self, filename):
        return
        # connectivity matrix is a csv file. Header (i.e. columns) are the *source*
        # rows are the *sinks" - check with Katie
        # colnames will be used as the reef name, as will row names. Cell A1 (i.e. 
        # top left, should therefore be blank
        #
        #            , Reef 1 source, Reef 2 source, Reef 3 source
        # Reef 1 sink,       0.01,         0.12,         0.43
        # Reef 2 sink,       0.00,         0.4,          0.01
        # Reef 3 sink,       0.00,         0.00,         0.8
        #

        # load with pandas

        # check rownames == colnames

        # check all number are between 0 and 1

        # set DF to self.connectivity_matrix

        # set number of sites based on nRows

    def visualise_connectivity_matrix(self, filename=None):
        return
        # make a graph, with colourbar and sensible name options

        # save to file or .show()


    def set_up_coral_model(self, type_of_model, parameters=None):
        return
        # pass a string of "greiner", "fungCAm", fungCMTm" etc
        # 
        # create a dictionary of coral ODE models, one per site

        # if parameters passed in as a dict, set those up

    def set_years(self, years):
        return
        # how many years should you run

    def set_start_conditions(self, conditions=None):
        return
        # if conditions passed in, check they of right length
        # numb reef sites and dimension of model

        # if not, generate random starting conditions (another function on the coral_ode_lab)

    def run_model(self):

        # check everything is loaded and ready to go

        # run for years, running one year at a time, altering the larvae each time
        #lsc_new = [] # list to hold updated lsc value
        #times.append(times[-1] + 1)
        #for sink in range(0,num_sites): 
        #    Pl = 0
        #    for source in range(0,num_sites):
        #        #print(c_matrix[sink])
        #        #begin calculating lsc
        #        Pl = Pl + (lastC[-1][source] * p_m * r_area * c_matrix[sink][source]) 
        #        # print(Pl)
        #        N = Pl * corals[sink].parameters["dc"]
        #        T = 1 - lastC[-1][sink] - lastM[-1][sink]
        #        lsc_new.append((N * r_area) / T)
        #        lsc_new.append(Pl)

        # set param

        # solve 1 year

        # store output
        return

    def plot_model_output(self, list_of_sites=None):
        return
        # check we have output

        # plot for list of sites, or all 

        # if n lines > 10 (?) then don't add legend and make the all the same colour.

    def save_model(self, filename):
        return
        # can we save it?

    def load_model(self, filename):
        return
        # can we load it?

    
