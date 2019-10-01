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

for f in files:

    fn = os.path.basename(f)
    year = int(fn.split("-")[3][0:4])
    month = int(fn.split("-")[3][5:6])
    day = int(fn.split("-")[3][7:8])
    if year > 1981 and year < 2016:
        print(year, month, day)
        ds = xr.open_dataset(f)

        if day == 1: # first of biweekly files
            sum_lai = ds.lai[0,:,:]
        elif day == 6:
            sum_lai += ds.lai[0,:,:]
            sum_lai /= 2.0
            clim[month-1,:,:] += sum_lai
            month_count[month-1,:,:] += 1.0


        ds.close()
clim = np.where(np.isnan(clim), -999.9, clim / month_count)


fp = open('test.dat', "wb")
clim.tofile(fp)
fp.close()

#sys.exit()
#"""
clim = np.fromfile('test.dat').reshape(nmonths,ny,nx)
clim = np.where(clim < -900.0, np.nan, clim)

print(clim.shape)
plt.imshow(clim[1,:,:])
plt.colorbar()
plt.show()
sys.exit()

# create file and write global attributes
out_fname = "test.nc"
f = nc.Dataset(out_fname, 'w', format='NETCDF4')
f.description = 'GIMMS3g LAI climatology data, created by Martin De Kauwe'
f.history = "Created by: %s" % (os.path.basename(__file__))
f.creation_date = "%s" % (datetime.datetime.now())
f.contact = "mdekauwe@gmail.com"

# set dimensions
f.createDimension('time', None)
f.createDimension('y', ny)
f.createDimension('x', nx)

y = f.createVariable('y', 'f8', ('y',))
y.long_name = "y"
y.long_name = "y dimension"

x = f.createVariable('x', 'f8', ('x',))
x.long_name = "x"
x.long_name = "x dimension"

n_timesteps = 1
times = []
secs = 0.0
for i in range(1,13):
    times.append(secs)
    days_in_month = monthrange(2011,i)[1] # not a leapyear
    secs += 86400. * days_in_month

time = f.createVariable('time', 'f8', ('time',))
time.units = "seconds since %s-%s-%s 00:00:00" % (2011, 1, 1)
time.long_name = "time"
time.calendar = "standard"

latitude = f.createVariable('latitude', 'f8', ('y', 'x',))
latitude.units = "degrees_north"
latitude.missing_value = m-999.0
latitude.long_name = "Latitude"

longitude = f.createVariable('longitude', 'f8', ('y', 'x',))
longitude.units = "degrees_east"
longitude.missing_value = -999.0
longitude.long_name = "Longitude"

varx = f.createVariable(var, 'f8', ('time', 'y', 'x',))
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
lats = np.repeat(lats, int(meta['ncols']))
lats = lats.reshape(int(meta['nrows']), int(meta['ncols']))

lons = np.linspace(lon_left, lon_right, int(meta['ncols']))
lons = np.tile(lons, int(meta['nrows']))
lons = lons.reshape(int(meta['nrows']), int(meta['ncols']))

# write data to file
x[:] = np.arange(1, int(meta['ncols'])+1)
y[:] = np.arange(1, int(meta['nrows'])+1)
time[:] = times
latitude[:,:] = lats
longitude[:,:] = lons
varx[:,:,:] =  clim

f.close()
