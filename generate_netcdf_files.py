#!/usr/bin/env python

"""
Turn the flt files into NetCDF files.

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (04.08.2018)"
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

    output_dir = "nc_files"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    meta = {'ncols': 841.0, 'cellsize': 0.05, 'nrows': 681.0,
            'xllcorner': 111.975, 'yllcorner': -44.025,
            'nodata_value': -999.0}

    for fname in files:

        data = np.fromfile(fname, dtype=np.float32)
        data = data.reshape(int(meta['nrows']), int(meta['ncols']))

        pre, ext = os.path.splitext(os.path.basename(fname))
        out_fname = "%s/%s.nc" % (output_dir,pre)

        # create file and write global attributes
        f = nc.Dataset(out_fname, 'w', format='NETCDF4')
        f.description = 'EucFACE met data, created by Martin De Kauwe'
        f.history = "Created by: %s" % (os.path.basename(__file__))
        f.creation_date = "%s" % (datetime.datetime.now())
        f.contact = "mdekauwe@gmail.com"

        print(out_fname)
        sys.exit()
        """

        """

    """
    fname = "raw/9999010199990131_fper_gimms3g_clim.flt"
    data = np.fromfile(fname, dtype=np.float32)
    data = data.reshape(int(meta['nrows']), int(meta['ncols']))
    data = np.where(data < 0.0, np.nan, data)
    plt.imshow(data, origin="upper")
    plt.colorbar()
    plt.show()
    """

if __name__ == "__main__":

    var = "fper"
    files = glob.glob("raw/*_%s_gimms3g_clim.flt" % (var))
    main(files, var)
