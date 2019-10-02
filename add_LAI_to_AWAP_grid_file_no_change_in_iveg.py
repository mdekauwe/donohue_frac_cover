#!/usr/bin/env python

"""
Add the newly created iveg PFTs to the CABLE gridinfo file

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (01.08.2019)"
__email__ = "mdekauwe@gmail.com"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import os
import sys
from os.path import join

def main():

    path = "/Users/mdekauwe/Desktop/SE_AUS_AWAP_grid_mask_files/raw"
    source = xr.open_dataset(join(path,
                             'MD_elev_orig_std_avg-sand_AWAP_AU_mask.nc'))

    se_aus = xr.open_dataset('lai_climatology_AWAP_grid.nc')

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
    out_grid_fname = "/Users/mdekauwe/Desktop/SE_aus_std_iveg_AWAP_plus_LAI_grid.nc"

    # This is the original values
    #source.iveg.plot(vmin=0, vmax=22)

    # Netcdf metadata with the type and fill value
    source.LAI.encoding
    print (source.LAI.encoding)

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

    source.to_netcdf(os.path.join(path, out_grid_fname))

if __name__ == "__main__":

    main()
