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
import netCDF4 as nc
import datetime
import os
import sys

def main():

    fname = "nc_files/patch_frac/patch_frac.nc"
    ds = xr.open_dataset(fname)
    frac = ds.patchfrac[0,:,:]
    for i in range(0, 17):
        print( i, np.nanmin(ds.patchfrac[i,:,:]),  np.nanmax(ds.patchfrac[i,:,:]), np.nanmean(ds.patchfrac[i,:,:]))

    fracs = ds.patchfrac[1,:,:] + ds.patchfrac[5,:,:] + ds.patchfrac[13,:,:]
    print(  np.nanmin(fracs),  np.nanmax(fracs), np.nanmean(fracs) )
    #fracs = np.where(fracs <0.0, fracs, np.nan)
    plt.hist(fracs.values.flatten())
    #plt.colorbar()
    plt.show()

if __name__ == "__main__":

    main()
