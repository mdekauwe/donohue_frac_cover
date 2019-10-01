#!/usr/bin/env python

"""
Turn the flt files for fcov, fper & frec derived from Randall
Donohue’s decompositions of the GIMMS3g NDVI data monthly climatology
(1982-2013) into NetCDF files.

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (30.07.2019)"
__email__ = "mdekauwe@gmail.com"

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import glob
import netCDF4 as nc
import datetime
import os
import sys
import netCDF4 as nc
from calendar import monthrange

ny = 681
nx = 841
nmonths = 12

#"""
files = sorted(glob.glob("nc_files/lai/gimms3g*.nc"))
clim = np.zeros((nmonths,ny,nx))
month_count = np.zeros((nmonths,ny,nx))
sum_count = np.zeros((ny,nx))
sum_lai = np.zeros((ny,nx))
month = 0
for f in files:

    fn = os.path.basename(f)
    year = int(fn.split("-")[3][0:4])
    day = int(fn.split("-")[3][7:8])

    if year > 1981 and year < 2016:
        print(year, month, day)

        ds = xr.open_dataset(f)
        #"""
        if day == 1: # first of biweekly files

            lai = ds.lai[0,:,:]

            sum_lai = np.where(np.logical_or(np.isnan(lai),
                               lai < 0.0), 0.0, lai)
            sum_count = np.where(np.logical_or(np.isnan(lai),
                                 lai < 0.0), 0.0, 1.0)

        elif day == 6:

            lai = ds.lai[0,:,:]
            sum_lai = np.where(np.logical_or(np.isnan(lai),
                               lai < 0.0), 0.0, sum_lai+lai)
            sum_count = np.where(np.logical_or(np.isnan(lai),
                                 lai < 0.0), sum_count, sum_count+1.0)
            count = np.where(sum_count > 0.0, 1.0, 0.0)
            sum_lai = np.where(sum_count > 0.0, sum_lai / sum_count, 0.0)
            clim[month,:,:] += sum_lai
            month_count[month,:,:] += count
            month += 1

        if month == 12:
            month = 0

        #"""
        ds.close()
clim = np.where(np.logical_and(np.logical_or(np.isnan(clim),
                               clim < 0.0),
                               month_count> 0.0), -999.9, clim / month_count)


fp = open('test.dat', "wb")
clim.tofile(fp)
fp.close()

#sys.exit()
#"""
clim = np.fromfile('test.dat').reshape(nmonths,ny,nx)
clim = np.where(clim < -900.0, np.nan, clim)


#plt.imshow(clim[10,:,:])
#plt.colorbar()
##plt.show()
#sys.exit()

# create file and write global attributes
out_fname = "lai_climatology.nc"
f = nc.Dataset(out_fname, 'w', format='NETCDF4')
f.description = 'GIMMS3g LAI climatology data, created by Martin De Kauwe'
f.history = "Created by: %s" % (os.path.basename(__file__))
f.creation_date = "%s" % (datetime.datetime.now())
f.contact = "mdekauwe@gmail.com"

# set dimensions
f.createDimension('time', None)
f.createDimension('lat', ny)
f.createDimension('lon', nx)

times = np.arange(1, 13)

time = f.createVariable('time', 'f8', ('time',))
time.units = "months"
time.long_name = "time"
time.calendar = "standard"

lat = f.createVariable('lat', 'f8', ('lat',))
lat.units = "degrees_north"
lat.missing_value = -999.0
lat.long_name = "Latitude"

lon = f.createVariable('lon', 'f8', ('lon',))
lon.units = "degrees_east"
lon.missing_value = -999.0
lon.long_name = "Longitude"

varx = f.createVariable('LAI', 'f8', ('time', 'lat', 'lon',))
varx.units = "m2/m2"

meta = {'ncols': 841.0, 'cellsize': 0.05, 'nrows': 681.0,
        'xllcorner': 111.975, 'yllcorner': -44.025,
        'nodata_value': -999.0}

# 111.975 + (841. * 0.05)
# -44.025 + (681. * 0.05)
lats_top = meta['yllcorner'] + (meta['nrows'] * meta['cellsize'])
lats_bot = meta['yllcorner'] + (0 * meta['cellsize'])

lon_right = meta['xllcorner'] + (meta['ncols'] * meta['cellsize'])
lon_left = meta['xllcorner'] + (0 * meta['cellsize'])

lats = np.linspace(lats_bot, lats_top, int(meta['nrows']))
lons = np.linspace(lon_left, lon_right, int(meta['ncols']))

time[:] = times
lat[:] = lats
lon[:] = lons
varx[:,:,:] =  clim

f.close()
