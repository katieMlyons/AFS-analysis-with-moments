#!/usr/bin/env python

import matplotlib
matplotlib.use('PDF')
import moments
import pylab
import matplotlib.pyplot as plt
import numpy as np
from numpy import array
from moments import Misc,Spectrum,Numerics,Manips,Integration,Demographics1D,Demographics2D
import sys

infile=sys.argv[1]

fs = moments.Spectrum.from_file(infile)
nalleles=fs.S()
print "N alleles: ",nalleles
ns=fs.sample_sizes
np.set_printoptions(precision=3)     

moments.Plotting.plot_1d_fs(fs)
plt.savefig('1dSFS_'+sys.argv[1]+'.pdf')
