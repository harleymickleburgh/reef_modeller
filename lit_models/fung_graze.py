#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 14:53:37 2023

@author: kl909
"""


from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt


# currently CAm params
# define a function to contain all inital conditions and the odes
theta = 0.7 #grazing pressure
dc = 0.02 #coral mortality rate (yr^-1)
lbc = 0.0009 #rate at which coral larvae, produced by local established brooding corals, recruit onto space (yr^-1)
lsc = 0.00006 #rate at which exogenus spawning coral larvae recruit onto space (yr^-1)
rc = 0.2 # lateral growth rate of corals over space (yr^-1)
gT = 10 #maximum rate at which turf algae is grazed (yr^-1)
ac = 0.25 #growth rate of corals over turf, relative to the rate over space
ec = 0.1 #recruitment rate of corals onto turf, relative to the rate onto space 
sT = 5 #growth rate of fine turf (occupying space) (yr^-1)
vm = 0.9
gm = 3.5
rm = 0.35
bm = 0.9
ymc = 0.1
ymt = 0.45

def fungCTm(z,t):
    # constants
    S = 1 - z[0] - z[1] # or S = 1 - C - T
   
   # define the odes
    dCdt = ((lsc_sink + lbc*z[0])*(S+ec*z[1])) + (rc*(S+ac*z[1])*z[0]) - (dc*z[0])
    dTdt = (sT*(1-theta)*S) - (gT*theta*z[1]) - (ec*(lsc_sink +lbc*z[0])*z[1]) - (ac*rc*z[1]*z[0])
   
    return [dCdt, dTdt]

def fungCAm(z,t):
    
    S = 1 - z[0] - z[1]
    
        #coral dC
    recruitmentC = (lsc + lbc*z[0])*(S+ec*(1 - vm)*z[1])
    growthC = rc*(1 - bm * vm * z[1])*(S + ac*(1 -vm)*z[1])*z[0]
    mortalityC = dc*z[0]
    MgrowthC = ymc*rm*vm*z[1]*z[0]
    dCdt = recruitmentC + growthC - mortalityC - MgrowthC
    
    # algae dM
    growthMA = rm*vm*z[1]*(S+ymc*z[0])
    growthT = sT*(1-theta)*S
    grazingAT = (gm*vm+gT*(1-vm))*theta*z[1]
    CrecruitmentT = ec*(1-vm)*(lsc+lbc*z[0])*z[1]
    CgrowthT = ac*rc*(1-vm)*(1 - bm*vm*z[1])*z[1]*z[0] 
    dMdt = growthMA + growthT - grazingAT - CrecruitmentT - CgrowthT
    
    return [dCdt, dMdt]

def fungCTMm(z,t):
    S = 1 - z[0] - z[1] - z[2]
    
        #coral dC
    recruitmentC = (lsc_sink + lbc*z[0])*(S+ec*z[1])
    growthC = rc*(1-bm*z[2])*(S+ac*z[1])*z[0]
    mortalityC = dc*z[0]
    MgrowthC = ymc*rm*z[2]*z[0]
    
    dCdt = recruitmentC + growthC - mortalityC - MgrowthC
    
    #turf dT
    growthT = sT*(1-theta)*S
    grazingT = gT*theta*z[1]
    CrecrtuitmentT = ec*(lsc_sink+lbc*z[0])*z[1] #coral recruitment on turf
    CgrowthT = ac*rc*(1-bm*z[2])*z[1]*z[0] #%coral growth over turf
    MgrowthCT = ymt*rm*z[2]*z[1]
    
    dTdt = growthT - grazingT - CrecrtuitmentT - CgrowthT - MgrowthCT
    
      #macroalgae dM
    growthM = rm*z[2]*(S+ymc*z[0]+ymt*z[1])
    grazingM = gm*theta*z[2]
    
    dMdt = growthM - grazingM
    
    return [dCdt, dTdt, dMdt]

  

# grazing pressure
graz_pressure = np.arange(0.05, 0.7, 0.05) 
Cval = []
Tval = []
Mval = []
#t = np.linspace(0,250)
i = 0


# intial conditons
for point in graz_pressure:
    zstart = [0.8, 0.2]
    t = np.linspace(0,500, num = 500)
    theta = point
    ode = odeint(fungCAm, zstart, t)
    C = ode[:,0]
    #T = ode[:,1]
    M = ode[:,1]
    Cval.append(C[-1])
    #Tval.append(T[-1])
    Mval.append(M[-1])
    i = + 1
    
    #Cval = C[-1]
   # Tval = T[-1]
#print(Cval, Tval, Mval)
# for each value of theta, collect the result of C at t 250 and result of T at t 250
# array for result of C at t 250
    # array for T at t 250
    # store result in new array
    
plt.plot(graz_pressure, Cval, graz_pressure, Mval)
plt.show()


