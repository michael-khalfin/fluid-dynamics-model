# -*- coding: utf-8 -*-

# MAP = DP + 1/3(SP – DP) or MAP = DP + 1/3(PP)
# Physiology, Mean Arterial Pressure

# (1) right radial artery
# diameter:  2.38 ± 0.56mm
# Anatomical study of forearm arteries with ultrasound for percutaneous coronary procedures
# pressure: 90.7 ± 12.3 mmHg
# Brachial and radial arterial pressure are not the same

# (2) right brachial artery
# diameter: 3.97 ± 0.51 mm
# Accurate quantitative measurements of brachial artery cross-sectional vascular area and vascular volume elastic modulus using automated oscillometric measurements: comparison with brachial artery ultrasound
# pressure: 92.3 ± 12.2 mmHg

# (3) right axillary artery
# pressure: 
# diameter: 6.38 ± 1.57 mm
# CT Angiography Analysis of Axillary Artery Diameter versus Common Femoral Artery Diameter: Implications for Axillary Approach for Transcatheter Aortic Valve Replacement in Patients with Hostile Aortoiliac Segment and Advanced Lung Disease

# (4) right subclavian artery
# diameter: 8.7 mm
# Anatomical Considerations and Clinical Implications of Subclavian Artery

# (5) right vertebral artery
# no micromotor
# diameter: 2.43 mm
# Variations in Diameters of Vertebro-basilar Tree in Patients with or with No Aneurysm

# (6) right posterior cerebral artery
# diameter = 2.5 mm
# no micromotor

# assume viscosity = 

# set parameters

import numpy as np  # for manipulating arrays
#import matplotlib.pyplot as plt
#from scipy.optimize import fsolve
from gekko import GEKKO

# set parameters
P_vals = np.array([90.7,92.3,80,80,80,80])
rho_vals = np.array([1060,1060,1060,1060,1060,1060])
g_val = 9.81
y0 = np.array([5,6,7,8,10,12])
precision = 1000
y_vals = np.zeros((len(y0)-1,precision))
for i in range(len(y0)-1):
    y_vals[i] = np.arange(y0[i], y0[i+1], (y0[i+1]-y0[i])/precision)

def initialVelocity(i):
    # using poiseullie equation
    q = ()

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

