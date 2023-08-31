#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 11:38:28 2023

@author: kl909
"""

import pandas as pd
from matplotlib import pyplot as plt
import csv
import numpy as np



df = pd.read_csv("swain_reef_sample.csv", delimiter=",")
#df.fillna(df.mean(numeric_only=True).round(1), inplace=True)
df = df.interpolate() # fill with missing data with rolling mean of previous and following data

#convert long csv data to wide 
wide1 = df.pivot(index='year', columns='reef_name', values = ['coral_cover','algae_cover']).reset_index()
#print(wide)

wide2 = wide1

fig_summary=plt.figure(figsize=(12.0,6),dpi=360)
ax=fig_summary.add_subplot(111)
colours = ['#ff7f00', '#377eb8', '#a65628',
            '#4daf4a', '#984ea3', '#f780bf',
              '#999999', '#e41a1c', '#dede00']

# horseshoe = '#377eb8'
#chineman = '#ff7f00'
#wade = '#4daf4a'
#jenkins = '#a65628'
    
cplot = wide1.plot.line(ax=ax, x='year', y = 'coral_cover', color=colours)
mplot = wide2.plot.line(ax=ax, x='year', y = 'algae_cover', linestyle='--', color=colours)
plt.title("Reef population change")
plt.xlabel('Years')
plt.ylabel('Population %')
plt.xlim(2006, 2009)
plt.ylim(0, 50)

#for i in range(len(cplot)):
#   cplot[i].set_color(colours[i])
#   mplot[i].set_color(colours[i])


plt.axvline(x = 1998, color = 'r', ls=':', lw=1)
plt.axvline(x = 1999, color = 'r', ls=':', lw=1)
plt.axvline(x = 2000, color = 'r', ls=':', lw=1)
plt.axvline(x = 2001, color = 'r', ls=':', lw=1)
plt.axvline(x = 2002, color = 'r', ls=':', lw=1)
plt.axvline(x = 2003, color = 'r', ls=':', lw=1)
plt.axvline(x = 2009, color = 'r', ls=':', lw=1)
plt.axvline(x = 2011, color = 'r', ls=':', lw=1)
plt.axvline(x = 2015, color = 'r', ls=':', lw=1)
plt.axvline(x = 2017, color = 'r', ls=':', lw=1)
plt.axvline(x = 2018, color = 'r', ls=':', lw=1)
plt.axvline(x = 2019, color = 'r', ls=':', lw=1)
plt.axvline(x = 2020, color = 'r', ls=':', lw=1)
plt.axvline(x = 2016, color = 'r', ls=':', lw=1)
plt.show()
