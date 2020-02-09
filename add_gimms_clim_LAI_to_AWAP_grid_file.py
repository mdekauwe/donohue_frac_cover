#!/usr/bin/env python

"""
Add the gimms LAI to the newly created iveg CABLE gridinfo file

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


def main(gimms_lai_clim_fname, grid_fname, out_grid_fname):

    source = xr.open_dataset(grid_fname)
    se_aus = xr.open_dataset(gimms_lai_clim_fname)

    # AWAP data is upside down, flip it
    for i in range(12):
        se_aus["LAI"][i,:,:] = np.flipud(se_aus["LAI"][i,:,:])

    # Rounding issue on the lat lon, so they won't match, just use the
    # AWAP grid vals.
    se_aus["latitude"] = source["latitude"]
    se_aus["longitude"] = source["longitude"]



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
    merged_LAI = xr.where(np.isfinite(se_aus.LAI), se_aus.LAI, source.LAI)

    # Copy the netcdf metadata to the new field (type, missing values)
    merged_LAI.encoding = source.LAI.encoding

    # Maintain the same land-sea pixels.
    #merged_LAI = xr.where(np.isnan(source.LAI), -1.0, merged_LAI)

    # Replace the source dataset's iveg field with the new version and save to
    # file
    source['LAI'] = merged_LAI


    source.to_netcdf(out_grid_fname)

if __name__ == "__main__":

    gimms_lai_clim_fname = "lai_climatology_AWAP_grid.nc"

    grid_path = "/Users/mdekauwe/Desktop"

    grid_fname = "SE_AU_AWAP_NVIS_iveg_csiro_soil_grid.nc"
    grid_fname = join(grid_path, grid_fname)
    out_grid_fname = "SE_AU_AWAP_NVIS_iveg_csiro_soil_gimms_lai_grid.nc"
    out_grid_fname = join(grid_path, out_grid_fname)
    main(gimms_lai_clim_fname, grid_fname, out_grid_fname)


    grid_fname = "SE_AU_AWAP_NVIS_iveg_openland_soil_grid.nc"
    grid_fname = join(grid_path, grid_fname)
    out_grid_fname = "SE_AU_AWAP_NVIS_iveg_openland_soil_gimms_lai_grid.nc"
    out_grid_fname = join(grid_path, out_grid_fname)
    main(gimms_lai_clim_fname, grid_fname, out_grid_fname)
