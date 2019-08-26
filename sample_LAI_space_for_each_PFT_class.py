#!/usr/bin/env python

"""
Sample new PFT space to get the LAI ranges...

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (04.08.2019)"
__email__ = "mdekauwe@gmail.com"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import netCDF4 as nc
import os
import sys


fname = "nc_files/lai/lai_max.nc"
ds = xr.open_dataset(fname)
lai = np.max(ds.lai, axis=0)
lai = lai.values
fname = "../NVIS_australia/data/SE_aus_veg_types_AWAP_grid.nc"
ds = xr.open_dataset(fname)
iveg = ds.iveg.values

# hack shapes to be the same size just to sample LAI. We will need to properly
# match grids later when we want to use this
iveg = iveg[0:681,0:841]
iveg = np.flipud(iveg)


lai = np.where(np.isnan(iveg), np.nan, lai)

#plt.imshow(iveg)
#plt.imshow(lai)
#plt.colorbar()
#plt.show()


#print( "18 :", np.nanmin(lai[iveg == 18]), np.nanmax(lai[iveg == 18]) )
#print( "19 :", np.nanmin(lai[iveg == 19]), np.nanmax(lai[iveg == 19]) )
#print( "20 :", np.nanmin(lai[iveg == 20]), np.nanmax(lai[iveg == 20]) )
#print( "21 :", np.nanmin(lai[iveg == 21]), np.nanmax(lai[iveg == 21]) )
#print( "22 :", np.nanmin(lai[iveg == 22]), np.nanmax(lai[iveg == 22]) )


n18l,n18u = ( np.nanmean(lai[iveg == 18])-np.nanstd(lai[iveg == 18]),
              np.nanmean(lai[iveg == 18])+np.nanstd(lai[iveg == 18]) )
n19l,n19u = ( np.nanmean(lai[iveg == 19])-np.nanstd(lai[iveg == 19]),
              np.nanmean(lai[iveg == 19])+np.nanstd(lai[iveg == 19]) )
n20l,n20u = ( np.nanmean(lai[iveg == 20])-np.nanstd(lai[iveg == 20]),
              np.nanmean(lai[iveg == 20])+np.nanstd(lai[iveg == 20]) )
n21l,n21u = ( np.nanmean(lai[iveg == 21])-np.nanstd(lai[iveg == 21]),
              np.nanmean(lai[iveg == 21])+np.nanstd(lai[iveg == 21]) )
n22l,n22u = ( np.nanmean(lai[iveg == 22])-np.nanstd(lai[iveg == 22]),
              np.nanmean(lai[iveg == 22])+np.nanstd(lai[iveg == 22]) )
print( "18 ", round(n18l, 2), "-", round(n18u, 2) )
print( "19 ", round(n19l, 2), "-", round(n19u, 2) )
print( "20 ", round(n20l, 2), "-", round(n20u, 2) )
print( "21 ", round(n21l, 2), "-", round(n21u, 2) )
print( "22 ", round(n22l, 2), "-", round(n22u, 2) )

"""
18  4.78 - 6.94
19  3.46 - 6.19
20  1.43 - 4.75
21  1.27 - 3.39
22  0.34 - 1.67
"""
#lai = np.where(iveg !=22, np.nan, lai)
#
#plt.imshow(lai)
#plt.colorbar()
#plt.show()
