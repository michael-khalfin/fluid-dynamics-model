# -*- coding: utf-8 -*-

# (1) right radial artery
# diameter: 2.38 ± 0.56 mm
# Anatomical study of forearm arteries with ultrasound for percutaneous coronary procedures

# (2) right brachial artery

# (3) right axillary artery

# (4) right subclavian artery

# (5) right vertebral artery
# no micromotor

# (6) right posterior cerebral artery
# https://www.researchgate.net/publication/304081397_THE_INNER_DIAMETER_OF_ARTERIES_OF_THE_CIRCLE_OF_WILLIS_REGARDING_GENDER_AND_AGE_ON_MAGNETIC_RESONANCE_ANGIOGRAPHY
# diameter = 1.94 mm
# no micromotor

# set parameters

import numpy as np  # for manipulating arrays
#import matplotlib.pyplot as plt
#from scipy.optimize import fsolve
from gekko import GEKKO

# set parameters
P_vals = np.array([80,80,80,80,80,80])
rho_vals = np.array([1060,1060,1060,1060,1060,1060])
g_val = 9.81
y0 = np.array([5,6,7,8,10,12])
precision = 1000
y_vals = np.zeros((len(y0)-1,precision))
for i in range(len(y0)-1):
    y_vals[i] = np.arange(y0[i], y0[i+1], (y0[i+1]-y0[i])/precision)

def bernoulliSolver():
    rho = rho_vals[0]
    g = g_val
    y = y_vals[0][0]
    y2 = y_vals[0][1]
    y3 = y_vals[0][2]
    
    m = GEKKO()             # create GEKKO model
    P = m.Var(value=1)      # define new variable, initial value=1
    C = m.Var(value=1)      # define new variable, initial value=1
    u = m.Var(value=1)      # define new variable, initial value=1
    #m.Equations([P+.5*rho*u**2+rho*g*y==C, P+.5*rho*u**2+rho*g*y2==C, P+.5*rho*u**2+rho*g*y3==C]) # equations
    m.Equations([P+.5*1060*u**2+1060*9.81*5==C, P+.5*1060*u**2+1060*9.81*5.01==C, P+.5*1060*u**2+1060*9.81*5.02==C]) # equations
    m.solve(disp=False)     # solve
    print([P.value[0],C.value[0],u.value[0]]) # print solution
    #expr = P + .5 * rho * (u**2) + rho * g * h

