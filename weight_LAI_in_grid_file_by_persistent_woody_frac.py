#!/usr/bin/env python

"""
Weight the LAI in the newly created iveg PFTs CABLE gridinfo file by the gimms
fraction of persistent tree cover.

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (10.02.2020)"
__email__ = "mdekauwe@gmail.com"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import os
import sys
from os.path import join

def main(tree_frac_fname, grid_fname, out_grid_fname):


    ds_per = xr.open_dataset(tree_frac_fname)
    fper = ds_per.fper[0,:,:]

    source = xr.open_dataset(grid_fname)

    #se_aus = xr.open_dataset('lai_climatology_AWAP_grid.nc')
    #lai = se_aus.LAI.values.copy()
    #for i in range(12):
    #    lai[i,:,:] *= fper
    #    se_aus.LAI[i,:,:] = lai[i,:,:]

    # AWAP data is upside down, flip it
    #for i in range(12):
    #    se_aus["LAI"][i,:,:] = np.flipud(se_aus["LAI"][i,:,:])

    # apply fper to copernicus

    lai = source.LAI.values.copy()

    for i in range(12):
        lai[i,:,:] *= fper

    #plt.imshow(np.mean(lai, axis=0))
    #plt.imshow(fper)
    #plt.colorbar()
    ##plt.imshow(fper)
    #plt.show()
    #sys.exit()
        #source.LAI[i,:,:] = lai[i,:,:]



    # AWAP data is upside down, flip it
    #for i in range(12):
    #    se_aus["LAI"][i,:,:] = np.flipud(se_aus["LAI"][i,:,:])

    # Rounding issue on the lat lon, so they won't match, just use the
    # AWAP grid vals.
    #se_aus["latitude"] = source["latitude"]
    #se_aus["longitude"] = source["longitude"]



    #plt.imshow(se_aus["LAI"][0,:,:])
    #plt.show()
    #sys.exit()
    # First had to do
    # cdo sellonlatbox,112,154,-44,-10 data/SE_aus_veg_types_AWAP_grid.nc data/SE_aus_veg_types_AWAP_fixed_grid.nc


    # This is the original values
    #source.iveg.plot(vmin=0, vmax=22)

    # Netcdf metadata with the type and fill value
    source.LAI.encoding
    #print (source.LAI.encoding)

    # Merge the two fields
    # Where se_aus.iveg is defined (found using numpy.isfinite) use the values
    # from se_aus.iveg
    # Elsewhere use the original values from source.iveg

    #se_aus = se_aus.drop("time")

    #merged_LAI = xr.where(np.isfinite(se_aus.LAI), se_aus.LAI, source.LAI)
    merged_LAI = xr.where(np.isfinite(lai), lai, source.LAI)

    # Copy the netcdf metadata to the new field (type, missing values)
    merged_LAI.encoding = source.LAI.encoding

    # Maintain the same land-sea pixels.
    #merged_LAI = xr.where(np.isnan(source.LAI), -1.0, merged_LAI)

    # Replace the source dataset's iveg field with the new version and save to
    # file
    source['LAI'] = merged_LAI

    source.to_netcdf(out_grid_fname)

if __name__ == "__main__":

    # from gimms3g_AWAP_grid/nc_files/fper
    # made by running combine_and_average_cover_fracs.sh
    tree_frac_fname = "mean_fper.nc"
    #tree_frac_fname = "/Users/mdekauwe/Desktop/mean_fper.nc"

    # CSIRO soil, copernicus lai
    grid_path = "/Users/mdekauwe/Desktop"
    #grid_fname = "SE_AU_AWAP_NVIS_iveg_csiro_soil_grid.nc"
    grid_fname = "gridinfo_AWAP_CSIRO_AU_NAT_new_iveg.nc"
    grid_fname = join(grid_path, grid_fname)

    out_grid_path = "/Users/mdekauwe/Desktop/SE_AUS_AWAP_grid_mask_files/grid"
    out_grid_fname = "SE_AU_AWAP_NVIS_iveg_csiro_soil_coper_lai_grid.nc"
    out_grid_fname = join(out_grid_path, out_grid_fname)
    main(tree_frac_fname, grid_fname, out_grid_fname)

    """
    # CSIRO soil, gimms lai
    grid_path = "/Users/mdekauwe/Desktop"
    grid_fname = "SE_AU_AWAP_NVIS_iveg_csiro_soil_gimms_lai_grid.nc"
    grid_fname = join(grid_path, grid_fname)

    out_grid_path = "/Users/mdekauwe/Desktop/SE_AUS_AWAP_grid_mask_files/grid"
    out_grid_fname = "SE_AU_AWAP_NVIS_iveg_csiro_soil_gimms_lai_grid.nc"
    out_grid_fname = join(out_grid_path, out_grid_fname)
    main(tree_frac_fname, grid_fname, out_grid_fname)


    # openland soil, copernicus lai
    grid_path = "/Users/mdekauwe/Desktop/"
    grid_fname = "SE_AU_AWAP_NVIS_iveg_openland_soil_grid.nc"
    grid_fname = join(grid_path, grid_fname)

    out_grid_path = "/Users/mdekauwe/Desktop/SE_AUS_AWAP_grid_mask_files/grid"
    out_grid_fname = "SE_AU_AWAP_NVIS_iveg_openland_soil_coper_lai_grid.nc"
    out_grid_fname = join(out_grid_path, out_grid_fname)
    main(tree_frac_fname, grid_fname, out_grid_fname)

    # openland soil, gimms lai
    grid_path = "/Users/mdekauwe/Desktop/"
    grid_fname = "SE_AU_AWAP_NVIS_iveg_openland_soil_gimms_lai_grid.nc"
    grid_fname = join(grid_path, grid_fname)

    out_grid_path = "/Users/mdekauwe/Desktop/SE_AUS_AWAP_grid_mask_files/grid"
    out_grid_fname = "SE_AU_AWAP_NVIS_iveg_openland_soil_gimms_lai_grid.nc"
    out_grid_fname = join(out_grid_path, out_grid_fname)
    main(tree_frac_fname, grid_fname, out_grid_fname)
    """
