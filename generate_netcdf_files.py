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

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import netCDF4 as nc
import datetime
import os
import sys

def main(files, var):

    print(var)

    meta = {'ncols': 841.0, 'cellsize': 0.05, 'nrows': 681.0,
            'xllcorner': 111.975, 'yllcorner': -44.025,
            'nodata_value': -999.0}
    if var == "lai":
        meta['nodata_value'] = -9999

    output_dir = "nc_files"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_dir = "nc_files/%s" % (var)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for fname in files:

        data = np.fromfile(fname, dtype=np.float32)
        data = data.reshape(int(meta['nrows']), int(meta['ncols']))
        data = np.flipud(data)

        pre, ext = os.path.splitext(os.path.basename(fname))
        out_fname = "%s/%s.nc" % (output_dir,pre)

        # create file and write global attributes
        f = nc.Dataset(out_fname, 'w', format='NETCDF4')
        f.description = '%s: calculated from Randall Donohue’s decompositions of the GIMMS3g NDVI data monthly climatology (1982-2013), created by Martin De Kauwe' % (var)
        f.history = "Created by: %s" % (os.path.basename(__file__))
        f.creation_date = "%s" % (datetime.datetime.now())
        f.contact = "mdekauwe@gmail.com"

        # set dimensions
        f.createDimension('time', None)
        f.createDimension('z', 1)
        f.createDimension('y', int(meta['nrows']))
        f.createDimension('x', int(meta['ncols']))

        z = f.createVariable('z', 'f8', ('z',))
        z.long_name = "z"
        z.long_name = "z dimension"

        y = f.createVariable('y', 'f8', ('y',))
        y.long_name = "y"
        y.long_name = "y dimension"

        x = f.createVariable('x', 'f8', ('x',))
        x.long_name = "x"
        x.long_name = "x dimension"

        if var == "lai":
            year = fname[28:32]
            month = fname[32:34]
            day = fname[34:36]
        else:
            year = fname[11:15]
            month = fname[16:18]
            day = fname[18:20]

        n_timesteps = 1
        times = []
        secs = 0.0
        for i in range(n_timesteps):
            times.append(secs)
            secs += 1800.

        time = f.createVariable('time', 'f8', ('time',))
        time.units = "seconds since %s-%s-%s 00:00:00" % (year, month, day)
        time.long_name = "time"
        time.calendar = "standard"

        latitude = f.createVariable('latitude', 'f8', ('y', 'x',))
        latitude.units = "degrees_north"
        latitude.missing_value = meta['nodata_value']
        latitude.long_name = "Latitude"

        longitude = f.createVariable('longitude', 'f8', ('y', 'x',))
        longitude.units = "degrees_east"
        longitude.missing_value = meta['nodata_value']
        longitude.long_name = "Longitude"

        varx = f.createVariable(var, 'f8', ('time', 'y', 'x',))
        if var == "lai":
            varx.units = "m2/m2"
        else:
            varx.units = "[0-1]"
        varx.missing_value = meta['nodata_value']
        if var == "fper":
            varx.long_name = "fraction persistent vegetation (wood)"
        elif var == "fcov":
            varx.long_name = "fraction cover"
        elif var == "frec":
            varx.long_name = "fraction recurrent component (grass)"
        elif var == "lai":
            varx.long_name = "leaf area index"

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
        x[:] = int(meta['ncols'])
        y[:] = int(meta['nrows'])
        z[:] = 1
        time[:] = times
        latitude[:,:] = lats
        longitude[:,:] = lons
        varx[0,:,:] =  data.reshape(n_timesteps, int(meta['nrows']),
                                    int(meta['ncols']))

        f.close()


if __name__ == "__main__":

    var = "fper"
    files = glob.glob("raw/%s/*_%s_gimms3g_clim.flt" % (var, var))
    main(files, var)

    var = "fcov"
    files = glob.glob("raw/%s/*_%s_gimms3g_clim.flt" % (var, var))
    main(files, var)

    var = "frec"
    files = glob.glob("raw/%s/*_%s_gimms3g_clim.flt" % (var, var))
    main(files, var)

    var = "lai"
    files = glob.glob("raw/%s/*.flt" % (var))
    main(files, var)
