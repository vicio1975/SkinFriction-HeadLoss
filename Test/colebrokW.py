# -*- coding: utf-8 -*-
"""


@author: vsamm
"""

import numpy as np
import matplotlib.pyplot as plt

EPS=0.01
ratio = 15
dc = EPS*2*ratio

Re = 200000
RE = np.arange(500,5000000,1000)
LAMBDA = np.zeros(RE.size)
LAMBDA2 = np.zeros(RE.size)   

for i,Re in enumerate(RE): 
    turbTerm =  EPS/(3.71*dc) #turbulent term
    lambInf = 0.25 * (np.log10(turbTerm)**2)**-1
    lamI = lambInf #First value for the friction coefficient
    errLam = 999 
    tol  = 1e-14
    its = 0
    while (errLam > tol):
        lamTerm = 2.51/(Re*(lamI**0.5))   
        lamII = 0.25 * (np.log10(turbTerm + lamTerm)**2)**-1 
        errLam = np.abs((lamI - lamII)/lamI)
        lamI = lamII
        its += 1
    
    LAMBDA[i]=lamI
    
for i,Re in enumerate(RE):  
    #Six params#
    l1 = 0.02 #residual stress from laminar to turbulent transition
    t1 = 3000 #Reynolds is number at first transition

    l2 = np.abs(l1-(1/(-2*np.log10(EPS/(3.7065*dc))))**2)
    t2 = (0.77505/(EPS/dc)**2) - (10.984/(EPS/dc)) + 7953.8     

    y0 = 64/Re  #laminar flow
    y1 = l1 / (1 + np.e**((t1-Re)/100))
    y2 = l2 / (1 + np.e**(((t2-Re)/600)*EPS/dc)) 
    
    lamb_ = y0 + y1 + y2
    
    LAMBDA2[i]=lamb_

print(ratio)
print(LAMBDA[-1])       
print(LAMBDA2[-1]) 
   
plt.xlabel("Re[-]")
plt.ylabel("friction factor")
plt.plot(RE,LAMBDA,"-b",label="ColebrookWhite")
plt.plot(RE,LAMBDA2,"-r",label="Six-Parameters")
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.show()