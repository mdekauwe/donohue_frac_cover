#!/usr/bin/env python
"""
Scale the LAI climatology by the persistent woody frac

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (03.12.2019)"
__email__ = "mdekauwe@gmail.com"


import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import cartopy.crs as ccrs
import cartopy
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import sys

fname = "/Users/mdekauwe/Desktop/mean_fper.nc"
ds_per = xr.open_dataset(fname)
fper = np.flipud(ds_per.fper[0,:,:]) # other way round from LAI

fname = "lai_climatology_AWAP_grid.nc"
ds = xr.open_dataset(fname)
lai = ds.LAI.values.copy()


for i in range(12):
    lai[i,:,:] *=fper
    ds.LAI[i,:,:] = lai[i,:,:]

#lai *= ds_per.fper
plt.imshow(ds.LAI[0,:,:], origin="upper")
plt.colorbar()
plt.show()
