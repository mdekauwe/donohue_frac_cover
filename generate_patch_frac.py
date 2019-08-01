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

    output_dir = "nc_files/patch_frac"
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
    tree = np.where(np.isnan(tree), fill, tree)
    grass = np.where(np.isnan(grass), fill, grass)

    bare = 1.0 - tree - grass
    bare = np.where(bare > 1.0, fill, bare)
    total = tree + grass + bare
    empty = np.where(np.logical_and(bare >= 0.0, bare <= 1.0), 0.0, bare)

    # create file and write global attributes
    out_fname = os.path.join(output_dir, "patch_frac.nc")
    f = nc.Dataset(out_fname, 'w', format='NETCDF4')
    f.description = 'patchfrac for CABLE, created by Martin De Kauwe'

    f.history = "Created by: %s" % (os.path.basename(__file__))
    f.creation_date = "%s" % (datetime.datetime.now())
    f.contact = "mdekauwe@gmail.com"

    # set dimensions
    f.createDimension('patch', npfts)
    f.createDimension('lat', nrows)
    f.createDimension('lon', ncols)

    patch = f.createVariable('patch', 'int32', ('patch'))
    patch.long_name = "patch"
    patch.long_name = "patch dimensions"

    #y = f.createVariable('y', 'int32', ('y'))
    #y.long_name = "y"
    #y.long_name = "y dimension"

    #x = f.createVariable('x', 'int32', ('x'))
    #x.long_name = "x"
    #x.long_name = "x dimension"

    latitude = f.createVariable('lat', 'f4', ('lat'))
    latitude.units = "degrees_north"
    latitude.missing_value = fill
    latitude.long_name = "Latitude"
    latitude.standard_name = "latitude"
    latitude.axis = "Y"

    longitude = f.createVariable('lon', 'f4', ('lon'))
    longitude.units = "degrees_east"
    longitude.missing_value = fill
    longitude.long_name = "Longitude"
    longitude.standard_name = "longitude"
    longitude.axis = "X"

    patchfrac = f.createVariable("patchfrac", 'f4', ('patch', 'lat', 'lon'))
    patchfrac.units = "[0-1]"
    patchfrac.missing_value = fill
    patchfrac.long_name = "Patch frac"


    # write data to file
    #x[:] = np.arange(1, ncols+1)
    #y[:] = np.arange(1, nrows+1)
    #patch[:] = np.arange(1, npfts+1)
    #lat[:] = nrows
    #lon[:] = ncols
    #patch[:] = npfts
    #latitude[:,:] = fper.latitude.values
    #longitude[:,:] = fper.longitude.values
    latitude[:] = fper.latitude.values[:,0]
    longitude[:] = fper.longitude.values[0,:]

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

    f.close()

    ds = xr.open_dataset(out_fname)
    plt.imshow(ds.patchfrac[5,:,:])
    plt.colorbar()
    plt.show()

if __name__ == "__main__":

    main()
