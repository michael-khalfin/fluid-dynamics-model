# -*- coding: utf-8 -*-

# (1) right radial artery
# (2) right brachial artery
# (3) right axillary artery
# (4) right subclavian artery
# (5) right vertebral artery
# (6) right posterior cerebral artery

# import numpy and remove scientific notation
import numpy as np
np.set_printoptions(suppress=True)

import matplotlib.pyplot as plt
import scipy.optimize as opt
import math
from scipy.stats import ttest_1samp

def initialVel(P1, P2, diam, mu, L):
    """ 
    Parameters: 
    pressure = P1
    pressure = P2
    diam = diameter
    mu = viscosity
    L = length
    
    Returns:
    q = Initial velocity using Hagen-Pouisille Equation
    """
    a = diam/2
    pi = 3.14159
    q = ((P1-P2)*pi*a**4)/(8*mu*L)
    return q

def generateVel(P_arr, diam_arr, mu, y0_arr, precision, rho, g, y_vals):
    """ 
    Parameters:
    Pressures = P_arr
    diam_arr = diameters
    mu = viscosity
    rho = density
    g = acceleration due to gravity
    y0_arr = lengths of arteries
    y_vals = heights along the arteries
    precision = amount of subdivisions
    
    Returns:
    v_arr = Array with blood velocities
    """
    pi = 3.14159
    vals = len(y0_arr)
    v_arr = np.zeros((vals, precision))
    # iniitial blood velocities
    for i in range(0,vals):
        # to get the volumetric flow rate
        v_arr[i][0] = initialVel(P_arr[i],P_arr[i+1],diam_arr[i],mu,y0_arr[i])
        # to get the blood velocities
        v_arr[i][0] = v_arr[i][0]/(pi*(diam_arr[i]/2)**2)
    # fill in the rest of the blood velocities
    for i in range(0, vals):
        for j in range(1, precision):
            v_arr[i][j] = bernoulliSolver(g,y_vals[i][j-1],y_vals[i][j],v_arr[i][j-1])
    # convert to centimeters / second
    v_arr /= 10
    return v_arr

def findHeights(y0, precision):
    """
    Parameters:
    y0 = lengths of the arteries
    precision = amount of subdivisions
    
    Returns:
    y = Array with successive heights along arteries
    """
    vals = len(y0)
    y = np.zeros((vals, precision))
    for i in range(vals):
        y[i] = np.linspace(0,y0[i],precision)
    y = np.round(y,5)
    return y

def bernoulliSolver(g,y1,y2,u0):
    """
    Parameters:
    g = acceleration due to gravity
    y1 = first height
    y2 = second height
    u0 = initial speed
    
    Returns:
    u = Successive speed
    """
    
    def func(u):
        u = math.sqrt(abs(u0**2 + 2*g*y1 - 2*g*y2))
        return u
    u = opt.fsolve(func,u0+.01)
    return u

def addMotors(area,v,x,y_arr,v_arr):
    """
    Parameters:
    area = area of nanomotors to generate v
    v = speed of nanomotors
    x = new area being tested
    y_arr = height values
    v_arr = blood velocity values
    
    Returns:
    t = Time to reach endpoint
    0 if any of the velocities are 0 or negative
    """
    # relative velocity problem
    v_rel = v_arr.copy()
    for i in range(0, len(v_rel)-2):
        v_rel[i] += (v/area)*x
    
    # time for each small increase delta y
    t_arr = np.zeros(len(v_rel))
    for i in range(0, len(v_rel)):
        for j in range(0, len(v_rel[0])-1):
            if v_rel[i][j] <= 0:
                return 0
            t_arr[i] += (y_arr[i][j+1] - y_arr[i][j]) / v_rel[i][j]
    t = np.sum(t_arr)
    return t

def addSpeeds(area,v,y_arr,v_arr):
    """
    Parameters:
    area = area of nanomotors to generate v
    v = new speed of nanomotors being tested
    y_arr = height values
    v_arr = blood velocity values
    
    Returns:
    t = Time to reach endpoint
    0 if any of the velocities are 0 or negative
    """
    # relative velocity problem
    v_rel = v_arr.copy()
    for i in range(0, len(v_rel)-2):
        v_rel[i] += (v/area)
    
    # time for each small increase delta y
    t_arr = np.zeros(len(v_rel))
    for i in range(0, len(v_rel)):
        for j in range(0, len(v_rel[0])-1):
            if v_rel[i][j] <= 0:
                return 0
            t_arr[i] += (y_arr[i][j+1] - y_arr[i][j]) / v_rel[i][j]
    t = np.sum(t_arr)
    return t
    
if __name__ == "__main__":
    # set parameters for initial calculations
    mu_val = 4.5
    rho_val = 1060
    g_val = -9.81
    P_vals = np.array([90.7,92.3,94,96,98,96,94])
    P_vals = 133322.39 * P_vals
    y0_vals = np.array([218.1,101.3,101.5,78,38.8,52])
    diam_vals = np.array([2.38,3.97,6.38,7.8,3.02,1.94])
    precision_val = 1000
    
    # set parameters for testing
    motor_area = .1
    motor_speed = 1
    test_vals = 30
    
    # initial calculations
    y_vals = findHeights(y0_vals, precision_val)
    v_vals = generateVel(P_vals, diam_vals, mu_val, y0_vals, precision_val,rho_val,g_val,y_vals)
    
    # A : testing amount of nanomotors
    
    # figuring out initial amount of mm for forward flow at all times
    motor_min = .1
    time = 0
    while time <= 0:
        time = addMotors(motor_area, motor_speed, motor_min, y_vals, v_vals)
        motor_min += .1
        
    # generate numpy array of nanomotor test values
    motor_amt = np.linspace(np.ceil(motor_min), 100, test_vals)
    motor_amt = np.ceil(motor_amt)
    
    # test nanomotors
    test_times = np.zeros(len(motor_amt))
    for i in range(0, len(motor_amt)):
        test_times[i] = addMotors(motor_area, motor_speed, motor_amt[i], y_vals, v_vals)
    test_times = np.round(test_times, 2)
    print(test_times)
    
    # plot test times
    fig = plt.figure(figsize=(8,8))
    ax1 = fig.add_subplot(2,1,1)
    ax1.set_xlabel('Amount of Nanomotors (mm)')
    ax1.set_ylabel('Total Time (s)')
    ax1.set_title('Effect of Varying Amount of Nanomotors on Total Time')
    ax1.scatter(motor_amt,test_times)
    
    # statistical analysis
    stat, p = ttest_1samp(test_times[1:],test_times[0])
    print('Statistics=%.10f, p=%.10f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
        print('Same distributions (fail to reject H0)')
    else:
        print('Different distributions (reject H0)')
    
    # B : testing speed of nanomotors
    
    # figuring out initial aspeed of nanomotor for forward flow at all times
    time = 0
    while time <= 0:
        time = addSpeeds(motor_area, motor_speed, y_vals, v_vals)
        motor_speed += .1
        
    # generate numpy array of speed test values
    speed_vals = np.linspace(np.ceil(motor_speed), 100, test_vals)
    speed_vals = np.ceil(speed_vals)
    
    # test nanomotors
    test_times = np.zeros(len(speed_vals))
    for i in range(0, len(speed_vals)):
        test_times[i] = addSpeeds(motor_area, speed_vals[i], y_vals, v_vals)
    test_times = np.round(test_times, 2)
    print(test_times)
    
    # plot test times
    fig = plt.figure(figsize=(8,8))
    ax1 = fig.add_subplot(2,1,1)
    ax1.set_xlabel('Speed of Nanomotors (cm/s)')
    ax1.set_ylabel('Total Time (s)')
    ax1.set_title('Effect of Varying Speed of Nanomotors on Total Time')
    ax1.scatter(motor_amt,test_times)
