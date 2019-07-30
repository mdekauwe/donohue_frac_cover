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

    output_dir = "patch_frac_files"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ncols = 841
    nrows = 681
    npfts = 17 # n_tiles -> cable_define_types
    fill = -999.0

    fper_fname = "nc_files/fper/mean_fper.nc"
    frec_fname = "nc_files/frec/mean_frec.nc"

    fper = xr.open_dataset(fper_fname)
    frec = xr.open_dataset(frec_fname)

    tree = fper.fper[0,:,:].values
    grass = frec.frec[0,:,:].values
    bare = 1.0 - tree - grass
    total = tree + grass + bare
    print(np.nanmin(total), np.nanmax(total))
    empty = np.where(total > 0.00000001, 0.0, total)

    # Check sums to less than 1
    #total = frec.frec[0,:,:] + fper.fper[0,:,:]
    #total = np.where(total > 1.0, total, np.nan)
    #plt.imshow(total)
    #plt.colorbar()
    #plt.show()

    # create file and write global attributes
    out_fname = os.path.join(output_dir, "patch_frac.nc")
    f = nc.Dataset(out_fname, 'w', format='NETCDF4')
    f.description = 'patchfrac for CABLE, created by Martin De Kauwe'

    f.history = "Created by: %s" % (os.path.basename(__file__))
    f.creation_date = "%s" % (datetime.datetime.now())
    f.contact = "mdekauwe@gmail.com"

    # set dimensions
    f.createDimension('y', nrows)
    f.createDimension('x', ncols)
    f.createDimension('patch', npfts)

    y = f.createVariable('y', 'f8', ('y',))
    y.long_name = "y"
    y.long_name = "y dimension"

    x = f.createVariable('x', 'f8', ('x',))
    x.long_name = "x"
    x.long_name = "x dimension"

    patch = f.createVariable('patch', 'f8', ('patch',))
    patch.long_name = "patch"
    patch.long_name = "patch dimensions"

    latitude = f.createVariable('latitude', 'f8', ('y', 'x',))
    latitude.units = "degrees_north"
    latitude.missing_value = fill
    latitude.long_name = "Latitude"

    longitude = f.createVariable('longitude', 'f8', ('y', 'x',))
    longitude.units = "degrees_east"
    longitude.missing_value = fill
    longitude.long_name = "Longitude"

    patchfrac = f.createVariable("patchfrac", 'f8', ('patch', 'y', 'x',))
    patchfrac.units = "[0-1]"
    patchfrac.missing_value = fill
    patchfrac.long_name = "Patch frac"

    # write data to file
    x[:] = np.arange(1, ncols+1)
    y[:] = np.arange(1, nrows+1)
    patch[:] = np.arange(1, npfts+1)
    latitude[:,:] = fper.latitude.values
    longitude[:,:] = fper.longitude.values
    patchfrac[0,:,:] = empty   #  evergreen_needleleaf
    patchfrac[1,:,:] = tree    #  evergreen_broadleaf
    patchfrac[2,:,:] = empty   #  deciduous_needleleaf
    patchfrac[3,:,:] = empty   #  deciduous_broadleaf
    patchfrac[4,:,:] = empty   #  shrub
    patchfrac[5,:,:] = grass   #  C3
    patchfrac[6,:,:] = empty   #  C4
    patchfrac[7,:,:] = empty   #  Tundra
    patchfrac[8,:,:] = empty   #  C3 crops
    patchfrac[9,:,:] = empty   #  C4 crops
    patchfrac[10,:,:] = empty  #  wetland
    patchfrac[11,:,:] = empty  #  empty
    patchfrac[12,:,:] = empty  #  empty
    patchfrac[13,:,:] = bare   #  barren
    patchfrac[14,:,:] = empty  #  urban
    patchfrac[15,:,:] = empty  #  lakes
    patchfrac[16,:,:] = empty  #  ice

    print(patchfrac.shape)
    print(tree.shape)

    #plt.imshow(tree)
    #plt.colorbar()
    #plt.show()

    f.close()

    ds = xr.open_dataset(out_fname)
    print(ds.patch)
    plt.imshow(ds.patchfrac[1,:,:])
    plt.colorbar()
    plt.show()

if __name__ == "__main__":

    main()
