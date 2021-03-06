#!/usr/bin/env python
import matplotlib
matplotlib.use('PDF')
import moments
import random
import pylab
import matplotlib.pyplot as plt
import numpy as np
from numpy import array
from moments import Misc,Spectrum,Numerics,Manips,Integration,Demographics1D,Demographics2D
import sys
infile=sys.argv[1]
params=[  float(sys.argv[2]),   float(sys.argv[3])]

import os
fs = moments.Spectrum.from_file(infile)
data = fs.fold()
nalleles=data.S()
print "N alleles: ",nalleles
ns=data.sample_sizes
np.set_printoptions(precision=3)     

#-------------------
# two epoch 2d model: null for s2m

def te2d(params , ns):
    nu,T = params
    sts = moments.LinearSystem_1D.steady_state_1D(ns[0]+ns[1])
    fs = moments.Spectrum(sts)
    fs.integrate([nu], T)
    fs = moments.Manips.split_1D_to_2D(fs, ns[0], ns[1])
    return fs
 
func=te2d
upper_bound = [100,10,0.3]
lower_bound = [1e-3,1e-3,1e-5]
params = moments.Misc.perturb_params(params, fold=1, upper_bound=upper_bound,
						  lower_bound=lower_bound)

poptg = moments.Inference.optimize_log(params, data, func,
							   lower_bound=lower_bound,
							   upper_bound=upper_bound,
							   verbose=False,maxiter=10)
model = func(poptg, ns)
ll_model = moments.Inference.ll_multinom(model, data)
theta = moments.Inference.optimal_sfs_scaling(model, data)

# index for this replicate    
ind=str(random.randint(0,999999))
print "te2dResf",ind,sys.argv[1],' ll: ', ll_model,' p: ', poptg, " t: ",theta, 
moments.Plotting.plot_2d_comp_multinom(model, data, vmin=1, resid_range=3)
                                                            
#plotting quad-panel figure wit AFS, model, residuals:
plt.savefig("te2df"+ind+"_"+sys.argv[1]+'.pdf')

