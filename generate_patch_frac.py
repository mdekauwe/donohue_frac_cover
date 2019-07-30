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

    fper_fname = "nc_files/fper/mean_fper.nc"
    frec_fname = "nc_files/frec/mean_frec.nc"

    fper = xr.open_dataset(fper_fname)
    frec = xr.open_dataset(frec_fname)

    tree = fper.fper[0,:,:]
    grass = frec.frec[0,:,:]
    bare = 1.0 - tree - grass


    # Check sums to less than 1
    #total = frec.frec[0,:,:] + fper.fper[0,:,:]
    #total = np.where(total > 1.0, total, np.nan)
    #plt.imshow(total)
    #plt.colorbar()
    #plt.show()

    plt.imshow(bare)
    plt.colorbar()
    plt.show()

    ncols = 841
    nrows = 681

    # create file and write global attributes
    out_fname = "patch_frac.nc"
    f = nc.Dataset(out_fname, 'w', format='NETCDF4')
    f.description = 'patchfrac for CABLE, created by Martin De Kauwe'

    f.history = "Created by: %s" % (os.path.basename(__file__))
    f.creation_date = "%s" % (datetime.datetime.now())
    f.contact = "mdekauwe@gmail.com"

    # set dimensions
    f.createDimension('time', None)
    f.createDimension('z', 1)
    f.createDimension('y', nrows)
    f.createDimension('x', ncols)


    z = f.createVariable('z', 'f8', ('z',))
    z.long_name = "z"
    z.long_name = "z dimension"

    y = f.createVariable('y', 'f8', ('y',))
    y.long_name = "y"
    y.long_name = "y dimension"

    x = f.createVariable('x', 'f8', ('x',))
    x.long_name = "x"
    x.long_name = "x dimension"

    time = f.createVariable('time', 'f8', ('time',))
    time.units = "seconds since 1999 00:00:00"
    time.long_name = "time"
    time.calendar = "standard"

    latitude = f.createVariable('latitude', 'f8', ('y', 'x',))
    latitude.units = "degrees_north"
    latitude.missing_value = -999.
    latitude.long_name = "Latitude"

    longitude = f.createVariable('longitude', 'f8', ('y', 'x',))
    longitude.units = "degrees_east"
    longitude.missing_value = -999.
    longitude.long_name = "Longitude"


    # write data to file
    x[:] = ncols
    y[:] = nrows
    z[:] = 1
    time[:] = fper.time.values
    latitude[:,:] = fper.latitude.values
    longitude[:,:] = fper.longitude.values


    f.close()

if __name__ == "__main__":

    main()
