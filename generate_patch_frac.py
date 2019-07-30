#!/usr/bin/env python

"""
Using the fcov, fper & frec derived from Randall Donohue’s decompositions of the
GIMMS3g NDVI data monthly climatology (1982-2013), generate the patchfrac
variable for CABLE

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (30.07.2019)"
__email__ = "mdekauwe@gmail.com"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import xarray as xr
import datetime
import os
import sys

def main():

    fper_fname = "nc_files/fper/mean_fper.nc"
    frec_fname = "nc_files/frec/mean_frec.nc"

    fper = xr.open_dataset(fper_fname)
    frec = xr.open_dataset(frec_fname)

    tree = fper.fper[0,:,:]
    grass = frec.frec[0,:,:]
    bare = 1.0 - tree - grass


    # Check sums to less than 1
    #total = frec.frec[0,:,:] + fper.fper[0,:,:]
    #total = np.where(total > 1.0, total, np.nan)
    #plt.imshow(total)
    #plt.colorbar()
    #plt.show()

    plt.imshow(bare)
    plt.colorbar()
    plt.show()


if __name__ == "__main__":

    main()
