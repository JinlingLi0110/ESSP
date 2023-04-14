import numpy as np
import pandas as pd
import gurobipy as grb

#--------------------------------------------------------------------------------------------#
#----------------------------------------Parameters------------------------------------------#
#--------------------------------------------------------------------------------------------#

#different Investment budgets( RMB)
C_max = 30000

#cost of ESS( RMB)
C_cost = 500

#Substation capacity(MVA)
S = 100

#ESS capacity(MWh)
S_ess = 1

#The amplitude of the voltage output from the substation(V)
U0 = 110

#maximum of voltage,minimum of voltage(V)
U_max = 121
U_min = 99

#Upper/lower limit of charge and discharge power(W)
P_max = 0.66
P_min = 0.54

#SOC
E_min = 0.1
E_initial = 0.5
E_max = 1.1
alpha = 0.9 

#number of moment(T)/mode
T = 24
NODE = 31
data = 3650
#The objective function scale factor
g_min = 0.04
g_max = 0.1
h = 0.05
f = 1

#maximum of the buttery
max_of_the_ESS = 60


#add the parameter matrix

#branch(ij)--resistance,reactance,Apparent power matrix

r_max = grb.GRB.INFINITY
r_ij = np.array([[r_max,0.097995,0.565714,r_max,r_max,r_max,r_max,0.094285,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,1.285714,r_max,r_max,1.285714,r_max,0.019836,r_max,r_max,r_max,r_max,r_max,2.204081,r_max,r_max,r_max],
                 [r_max,r_max,r_max,0.592653,0.565714,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,0.323265,0.484897,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,0.188571,0.700408,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,0.160824,0.077142,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,0.455265,0.125632,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,0.337224,0.66,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,1.170734,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,2.755102,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,1.285714,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,0.165306,1.322448,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,0.350448,0.079346,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,0.423183,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,0.18,1.102040,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,0.246122],
                  [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max]])

F_ij = np.array([[0,20.920000,2.050000,0,0,0,0,2.050000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2.790000,0,0,2.790000,0,2.050000,0,0,0,0,0,2.790000,0,0,0],
                 [0,0,0,2.050000,2.050000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,2.050000,2.050000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,2.050000,2.050000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,2.050000,2.030000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,2.050000,2.030000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,2.030000,2.050000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2.790000,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2.790000,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2.790000,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2.050000,2.050000,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2.050000,2.050000,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2.050000,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2.790000,2.790000,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2.790000],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

x_ij = np.array([[r_max,0.227696,0.661714,r_max,r_max,r_max,r_max,0.110285,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,1.148571,r_max,r_max,1.148571,r_max,0.027844,r_max,r_max,r_max,r_max,r_max,1.968979,r_max,r_max,r_max],
                 [r_max,r_max,r_max,0.693224,0.661714,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,0.378122,0.567183,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,0.220571,0.819265,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,0.188115,0.108285,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,0.532522,0.176351,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,0.473363,0.772,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,1.045856,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,2.461224,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,1.148571,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,0.232040,1.8566326,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,0.491926,0.111379,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,0.594024,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,0.1608,0.984489,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max],
                 [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,0.219869],
                  [r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max,r_max]])

#moment--node active power matrix
a = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
p_jtl0 = pd.read_excel("active_power.xlsx")
p_jtl01 = np.array(p_jtl0.values)
p_jtl001 = np.vstack([a,p_jtl01])
p_jtl = p_jtl001

#moment--node reactive power matrix
q_jtl0 = pd.read_excel("reactive_power.xlsx")
q_jtl01 = np.array(q_jtl0.values)
q_jtl001 = np.vstack([a,q_jtl01])
q_jtl = q_jtl001

#node--max of Reactive power compensation device
q_jnmax01 = np.array([
    [20],[0],[0],[0],[20],[20],[0],[20],[0],[0],[20],[0],[0],[0],[0],[20],[0],[0],[20],[20],[0],[20],[0],[0],[0],[0],[20],[0],[0],[0],[0]])
q_jnmax = q_jnmax01

#node--min of Reactive power compensation device
q_jnmin01 = np.array([
    [-20],[0],[0],[0],[-20],[-20],[0],[-20],[0],[0],[-20],[0],[0],[0],[0],[-20],[0],[0],[-20],[-20],[0],[-20],[0],[0],[0],[0],[-20],[0],[0],[0],[0]])
q_jnmin = q_jnmin01

#--------------------------------------------------------------------------------------------#
#---------------------------------------MIP Model--------------------------------------------#
#--------------------------------------------------------------------------------------------#

#create the model
ESSP = grb.Model("energy_storage_station_programming")

#decision variables
u_dis = ESSP.addVar(vtype = grb.GRB.BINARY)
u_ch = ESSP.addVar(vtype = grb.GRB.BINARY)
z = ESSP.addVars(NODE,1, lb = 0, ub = 600,vtype = grb.GRB.INTEGER, name = 'z')#place and capacity
p_jt = ESSP.addVars(NODE,T,lb = -grb.GRB.INFINITY,ub = grb.GRB.INFINITY, name = 'p_jt')#Injected active power
q_jt = ESSP.addVars(NODE,T,lb = -grb.GRB.INFINITY,ub = grb.GRB.INFINITY, name = 'q_jt')#Injected reactive power

#Active power flow on a branch
p_ijt = ESSP.addVars(NODE, NODE, T, lb = -grb.GRB.INFINITY,ub = grb.GRB.INFINITY)

#reactive power flow on a branch
q_ijt = ESSP.addVars(NODE, NODE, T, lb = -grb.GRB.INFINITY,ub = grb.GRB.INFINITY)

#The  discharge/charge power of the battery at the node
p_jmtdis = ESSP.addVars(NODE,T, name = 'p_jmtdis')
p_jmtch = ESSP.addVars(NODE,T, name = 'p_jmtch')

#The power of the reactive power compensation device at the node
q_jntg = ESSP.addVars(NODE,T,lb = -grb.GRB.INFINITY,ub = grb.GRB.INFINITY, name = 'q_jntg')

#Active cut load at the node
p_jtls = ESSP.addVars(NODE,T)

#reactive cut load at the node
q_jtls = ESSP.addVars(NODE,T)

#Node voltage amplitude
u_jt = ESSP.addVars(NODE,T,lb = U_min, ub = U_max)

#The node is in a state of charge
e_jmt = ESSP.addVars(NODE,T)


#add constraints

#cost constraints£¨4-9£©
#sum1 = 0
#for i in node2:
#    sum1 = sum1 + z[i] * buttery[i]
ESSP.addConstr(z.sum('*',0)*500 <= C_max)

#power balance constraints£¨4-13¡ª16£©

for t in range(T):
    ESSP.addConstr(p_jt[0,t] == p_ijt.sum(0,'*',t))
    ESSP.addConstr(q_jt[0,t] == q_ijt.sum(0,'*',t))

for i in range(NODE):
    for t in range(T):
        ESSP.addConstr((p_jmtdis[i,t]*u_dis - p_jmtch[i,t]*u_ch) - p_jtl[i,t] + p_jtls[i,t] == p_ijt.sum(i,'*',t) - p_ijt.sum('*',i,t))        
        
for i in range(NODE):
    for t in range(T):
        ESSP.addConstr(q_jntg[i,t] - q_jtl[i,t] + q_jtls[i,t] == q_ijt.sum(i,'*',t) - q_ijt.sum('*',i,t))

#Ohm's law constraints(4-17)
for t in range(T):
    for i in range(NODE):
        for j in range(NODE):
            ESSP.addConstr(u_jt[i,t] - u_jt[j,t] == (p_ijt[i,j,t]*r_ij[i,j] + q_ijt[i,j,t]*x_ij[i,j])/U0)

#Main substation transmission constraints(4-19¡ª22)
for t in range(T):
    ESSP.addConstr(-S <= p_jt[0,t])
    ESSP.addConstr(-S <= q_jt[0,t])
    ESSP.addConstr(-1.414*S <= p_jt[0,t] + q_jt[0,t])
    ESSP.addConstr(-1.414*S <= p_jt[0,t] - q_jt[0,t])
    ESSP.addConstr(p_jt[0,t] <= S)
    ESSP.addConstr(q_jt[0,t] <= S)
    ESSP.addConstr(p_jt[0,t] + q_jt[0,t] <= 1.414*S)
    ESSP.addConstr(p_jt[0,t] - q_jt[0,t] <= 1.414*S)

#Distribution line transmission power constraints£¨4-23¡ª26£©
for t in range(T):
    for i in range (NODE):
        for j in range(NODE):
            ESSP.addConstr(p_ijt[i,j,t] <= F_ij[i,j])
            ESSP.addConstr(q_ijt[i,j,t] <= F_ij[i,j])
            ESSP.addConstr(p_ijt[i,j,t] + q_ijt[i,j,t] <= 1.414*F_ij[i,j])
            ESSP.addConstr(p_ijt[i,j,t] - q_ijt[i,j,t] <= 1.414*F_ij[i,j])

for t in range(T):
    for i in range (NODE):
        for j in range(NODE):
            ESSP.addConstr(0 <= p_ijt[i,j,t] + F_ij[i,j])
            ESSP.addConstr(0 <= q_ijt[i,j,t] + F_ij[i,j] )
            ESSP.addConstr(0 <= p_ijt[i,j,t] + q_ijt[i,j,t] + F_ij[i,j]*1.414)
            ESSP.addConstr(0 <= p_ijt[i,j,t] - q_ijt[i,j,t] + F_ij[i,j]*1.414)

#Energy storage power station operation constraints(4-27¡ª31)
ESSP.addConstr(u_dis + u_ch == 1)
for t in range(T):
    for j in range (NODE):
        ESSP.addConstr(p_jmtch[j,t] <= P_max*z[j,0] )
        ESSP.addConstr(p_jmtdis[j,t] <= P_max*z[j,0] )
        ESSP.addConstr(e_jmt[j,t] <= E_max)
        ESSP.addConstr(P_min*z[j,0] <= p_jmtch[j,t] )
        ESSP.addConstr(P_min*z[j,0] <= p_jmtdis[j,t] )
        ESSP.addConstr(E_min <= e_jmt[j,t] )
for t in range(1,24,1):
    for j in range (NODE):
        ESSP.addConstr((e_jmt[j,t-1] - e_jmt[j,t])*z[j,0] == p_jmtdis[j,t]*u_dis/alpha - alpha*p_jmtch[j,t]*u_ch)

ESSP.addConstr(e_jmt[j,0] == e_jmt[j-1,T-1])
ESSP.addConstr(e_jmt[j,0] == E_initial)

#Emergency load shedding constraints£¨4-32,4-33£©
for t in range(T):
    for j in range(NODE):
        ESSP.addConstr(p_jtls[j,t] <= p_jtl[j,t] )
        ESSP.addConstr(q_jtls[j,t] <= q_jtl[j,t] )
        ESSP.addConstr(0 <= p_jtls[j,t])
        ESSP.addConstr(0 <= q_jtls[j,t])

#Reactive power compensation device constraints£¨4-34£©
for t in range(T):
    for j in range(NODE):
        ESSP.addConstr(q_jntg[j,t] <= q_jnmax[j,0])
        ESSP.addConstr(0 <= q_jntg[j,t] - q_jnmin[j,0])


#add objective
sum9 =(p_jmtdis.sum(0,'*') + p_jmtch.sum(0,'*'))*z[0,0]
for j in range(1,31,1):
    sum9 = sum9 + (p_jmtdis.sum(j,'*') + p_jmtch.sum(j,'*'))*z[j,0]

#sum10 =(p_jmtdis.sum(0,'*'))*z[0,0]
#for j in range(1,31,1):
#    sum10 = sum10 + (p_jmtdis.sum(j,'*'))*z[j,0]

sum10 = p_jt[0,0]
for i in range(6):
    sum10 = sum10 + p_jt[0,i]
for i in range(18,24,1):
    sum10 = sum10 + p_jt[0,i]

sum11 = p_jt[0,6]
for i in range(6,18,1):
    sum11 = sum11 + p_jt[0,i]

ESSP.setObjective(1*(z.sum('*','*'))*50 + g_min*365*sum10 + g_max*365*sum11+ h*sum9, grb.GRB.MINIMIZE)

#Penalty function
#10*3650 * (p_jtls.sum('*','*') + q_jtls.sum('*','*'))
# + 0.1*3650*sum10 
# + f*365 * (p_jtls.sum('*','*') + q_jtls.sum('*','*'))
#solving

ESSP.Params.NonConvex = 2
ESSP.optimize()
print(np.array(z.values))
#print(p_jtls.values)
#print(q_jtls.values)