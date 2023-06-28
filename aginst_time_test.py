# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot
import phaseportrait

# define a function to contain all inital conditions and the odes
def CTm(z,t): 
    # constants
    theta = 0.2 #grazing pressure
    dc = 0.08 # coral mortality rate (yr^-1)
    lbc = 0.25  # rate at which coral larvae, produced by local established brooding corals, recruit onto space (yr^-1)
    lsc_sink = 0.005  #rate at which exogenus spawning coral larvae recruit onto space (yr^-1)
    rc = 0.12 #lateral growth rate of corals over space (yr^-1)
    gT = 10 #maximum rate at which turf algae is grazed (yr^-1)
    ac = 0.5 # growth rate of corals over turf, relative to the rate over space
    ec = 0.1 # recruitment rate of corals onto turf, relative to the rate onto space 
    sT = 11 # growth rate of fine turf (occupying space) (yr^-1)
    
   
   # assign each ode to a vector element
  # C = z[0]
  # T = z[1]
    S = 1 - z[0] - z[1] # or S = 1 - C - T
   
   # define the odes
    dCdt = ((lsc_sink + lbc*z[0])*(S+ec*z[1])) + (rc*(S+ac*z[1])*z[0]) - (dc*z[0])
    dTdt = (sT*(1-theta)*S) - (gT*theta*z[1]) - (ec*(lsc_sink +lbc*z[0])*z[1]) - (ac*rc*z[1]*z[0])
   
    return [dCdt, dTdt]


def CAm(z,t):
    theta = 0.2 #grazing pressure
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
    #ymt = 0.45
    
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
    
    



def mumby(z,t):
     a = 0.1 #overgrowth
     g = 0.1 #0 - 0.5; grazing
     y = 0.77 #growth rate
     r = 0.55 #recruitment
     d = 0.24 #mortality

     
     T = 1 - z[1] - z[0]
     
         #coral (z(1))
     recruitmentC = r * T * z[0]
     mortalityC = d*z[0]
     Movergrowth = a*z[1]*z[0]
     dCdt = recruitmentC - mortalityC - Movergrowth
    
    # macroalgae (z(2))
     Movergrowth = a*z[1]*z[0]
     grazing = (g*z[1]) / (z[1] + T)
     growthM = y*z[1]*T
     dMdt = Movergrowth - grazing + growthM
    
     return[dCdt, dMdt]
     


#### THIS DOESN'T CONTAIN THE EXTERNAL LARVAE EQUATION OR THE GRAZING AS FUNCTION OF CORAL EQUATION

def mcmanus(z,t):
    r = 0.2#growth
    d = 0.5# mortality 0.02 - 1.0
    a = 1.0# coral overgrowth
    f = 10 # no. of larvae per meter per year
    s = 0.01# area of newly settled recruit
    g = 0.4# grazing (use fung?)
    y = 1.1 # turf overgrowth
    w = 0.005 # spawning larvae (use lsc from fung?)
    time = 0.5 #duration of external coral recruitment 0-1
 
    F = 1 - z[0] - z[1]
    
    growth = (r*F) * z[0]
    mortality = d*z[0]
    movergrowsc = a*z[0]*z[1]
    recruitment = (f*s + w)*F # was (f*s*z[0] + w)*F
    dCdt = growth - mortality - movergrowsc + recruitment
    
    mmovergrowsc = a*z[0]*z[1]
    grazing = g*z[1]
    movergrowst = y*z[1]*F
    dMdt = mmovergrowsc - grazing + movergrowst
   
    return[dCdt, dMdt]

def elmhirst(z,t):
    T = 1 - z[0] - z[1]
    
    growth = z[0]*(r*T)
    mortality = d*z[0]
    overgrowthM = a*z[1]*z[0]
    recruitment = s*T
    dCdt = growth - mortality - overgrowthM + recruitment
    
    movergrowingC = a*z[1]*z[0]
    grazing = z[1]*(g/(z[0]-1)) 
    MovergrowsT = y*z[1]*T
    Mrecruitment = e*T
    dMdt = movergrowingC + grazing + MovergrowsT + Mrecruitment
    
    return( dCdt, dMdt)
    




def greiner(z,t):
     r = 0.55 # Rate coral recruits settle on turf algae (/time)
     d = 0.24
     a = 0.1
     g = 0.77 #0.01 ≤g≤ 0.99
     y = 0.77 #Rate macroalgae recruits settle on turf algae (/time)
     lbc = 0.0025 # divided elmhirst value of all coral recruitment 0.005
     lsc = 0.0025
     mlbc = 0.0025
     mlsc = 0.0025
     T = 1 - z[0] - z[1]
    
     growth = r*(1-lbc)*T*z[0]
     mortalityC = d*z[0]
     Movergrowth = a*z[1]*z[0]
     recruitment = r*lsc*z[0]*T
     dCdt = growth - mortalityC - Movergrowth + recruitment
    
    # macroalgae (z(2))
     MMovergrowth = a*z[1]*z[0]
     grazing = g*(z[1]*T)
     growthM1 = y*(1-mlbc)*z[1]*T
     growthM2 = y*mlsc * z[1]*T
     dMdt = MMovergrowth - grazing + growthM1 + growthM2
    
     return[dCdt, dMdt]
    
# intial conditons
zstart = [0.8, 0.2]

# test the defined odes
#print(odes(z = zstart,t= 0))


# declare a time vector (time window)
t = np.linspace(0,500, num = 500)

# call the ode
x = odeint(greiner, zstart, t)
C = x[:,0]
M = x[:,1]


#PhasePlane = phaseportrait.PhasePortrait2D(C, M, Title='Simple pendulum', xlabel=r"$\Theta$", ylabel=r"$\dot{\Theta}$")
#PhasePlane.plot()


# plot the results
plt.plot(t, C)
plt.plot(t, M)
plt.ylim(0,1)
plt.xlim(-1)
plt.show()



   
   
