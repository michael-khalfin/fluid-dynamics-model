# case study - percent error

import numpy as np
np.set_printoptions(suppress=True)

v = 1
area = .1
x = 15
vel = np.array([43.2,56.6,85.6,94.3,69.8])
y0 = np.array([218.1,101.3,101.5,78,38.8,52])

for i in range(0, len(vel)-2):
    vel[i] += (v/area)*x
    
t_arr = np.zeros(len(vel))
for i in range(0, len(vel)):
    t_arr[i] = y0[i] / vel[i]