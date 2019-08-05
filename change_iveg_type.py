#!/usr/bin/env python

"""
Change iveg for SE Aus to be a different type.

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (04.08.2019)"
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
import shutil
import netCDF4

def main():

    in_fname = "/Users/mdekauwe/Desktop/gridinfo_mmy_MD_elev_orig_std_avg-sand_mask.nc"
    out_fname = "/Users/mdekauwe/Desktop/gridinfo_mmy_MD_elev_orig_std_avg-sand_mask_EBF_patch.nc"

    ds = xr.open_dataset(in_fname)

    iveg_changed = ds.iveg.values.astype(int)
    iveg_changed = np.where(iveg_changed > 0, 2, iveg_changed)

    #iveg_changed = np.where(ds.iveg == 9.0, 2.0, ds.iveg ) # EBF
    #iveg_changed = np.where(ds.iveg == 5.0, 2.0, -9999.0) # EBF
    #iveg_changed = np.where(ds.iveg > 0.0, 2.0, -9999.0) # EBF
    #iveg_changed = np.where(ds.iveg > 0.0, 6.0, -9999.0) # C3G

    ds_out = ds.copy(deep=True)
    ds_out = ds_out.drop("iveg")

    ds_out.to_netcdf(out_fname)
    ds_out.close()

    f = netCDF4.Dataset(out_fname, 'r+')

    nc_attrs = f.ncattrs()
    nc_dims = [dim for dim in f.dimensions]
    nc_vars = [var for var in f.variables]

    iveg = f.createVariable("iveg", 'i4', ('latitude', 'longitude'))
    iveg.units = "-"
    iveg.missing_value = -1

    iveg[:,:] = iveg_changed
    f.close()

    ds.close()

if __name__ == "__main__":

    main()
