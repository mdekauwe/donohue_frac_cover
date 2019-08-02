#!/usr/bin/env python

"""
Add the newly created patchfrac variable to the CABLE gridinfo file

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (01.08.2019)"
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
    out_fname = "/Users/mdekauwe/Desktop/gridinfo_mmy_MD_elev_orig_std_avg-sand_mask_MDK_patch.nc"
    patch_fname = "nc_files/patch_frac/patch_frac_0.5.nc"

    ds = xr.open_dataset(in_fname)
    ds_pch = xr.open_dataset(patch_fname)

    ds_out = ds.copy(deep=True)
    ds_out = ds_out.drop("patch")
    ds_out = ds_out.drop("patchfrac")
    ds_out = ds_out.drop("iveg")

    ds_out.to_netcdf(out_fname)
    ds_out.close()

    f = netCDF4.Dataset(out_fname, 'r+')

    nc_attrs = f.ncattrs()
    nc_dims = [dim for dim in f.dimensions]
    nc_vars = [var for var in f.variables]

    f.createDimension('patch', 17)

    patch = f.createVariable('patch', 'f4', ('patch'))
    patch.units = "patch fraction"
    patch.long_name = "patch"

    patchfrac = f.createVariable("patchfrac", 'f4', ('patch', 'latitude', 'longitude'))
    patchfrac.units = "[0-1]"
    patchfrac.missing_value = -999.0
    patchfrac.long_name = "Patch frac"

    iveg = f.createVariable("iveg", 'f4', ('patch', 'latitude', 'longitude'))
    iveg.units = "-"
    iveg.missing_value = -9999.0

    patch[:] = np.arange(1, 17+1)
    patchfrac[:,:,:] = ds_pch.patchfrac.values

    keep = ds_pch.patchfrac.values
    keep *= 0.0
    for i in range(17):
        keep[i,:,:] = i+1
    keep = np.where(patchfrac[1,:,:] >= 0.0, keep, -9999.0)

    #plt.imshow(keep[1,:,:])
    #plt.colorbar()
    #plt.show()
    #sys.exit()

    iveg[:,:,:] = keep
    f.close()


    ds.close()
    ds_pch.close()

if __name__ == "__main__":

    main()
