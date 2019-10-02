#!/usr/bin/env python

"""
Sample new PFT space to get the soil params ranges...

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

KPA_2_MPa = 0.001
M_HEAD_TO_MPa = 9.8 * KPA_2_MPa

fname = "/Users/mdekauwe/Desktop/SE_aus_veg_types_AWAP_grid.nc"
ds = xr.open_dataset(fname)
#print(ds)

bch = ds.bch.values
iveg = ds.iveg.values

# Soil matric potential at saturation (m of head to MPa: 9.81 * KPA_2_MPA)
sucs = ds.sucs.values * M_HEAD_TO_MPa

iveg = np.where(iveg < 15, np.nan, iveg)
sucs = np.where(np.isnan(iveg), np.nan, sucs)
bch = np.where(np.isnan(iveg), np.nan, bch)

#plt.imshow(sucs)
#plt.colorbar()
#plt.show()
#sys.exit()


n18l,n18u = ( np.nanmean(sucs[iveg == 18])-np.nanstd(sucs[iveg == 18]),
              np.nanmean(sucs[iveg == 18])+np.nanstd(sucs[iveg == 18]) )
n19l,n19u = ( np.nanmean(sucs[iveg == 19])-np.nanstd(sucs[iveg == 19]),
              np.nanmean(sucs[iveg == 19])+np.nanstd(sucs[iveg == 19]) )
n20l,n20u = ( np.nanmean(sucs[iveg == 20])-np.nanstd(sucs[iveg == 20]),
              np.nanmean(sucs[iveg == 20])+np.nanstd(sucs[iveg == 20]) )
n21l,n21u = ( np.nanmean(sucs[iveg == 21])-np.nanstd(sucs[iveg == 21]),
              np.nanmean(sucs[iveg == 21])+np.nanstd(sucs[iveg == 21]) )
n22l,n22u = ( np.nanmean(sucs[iveg == 22])-np.nanstd(sucs[iveg == 22]),
              np.nanmean(sucs[iveg == 22])+np.nanstd(sucs[iveg == 22]) )
print("SUCS")
print( "18 ", round(n18l, 8), "-", round(n18u, 8), round(np.nanmean(sucs[iveg == 18]),8) )
print( "19 ", round(n19l, 8), "-", round(n19u, 8), round(np.nanmean(sucs[iveg == 19]),8) )
print( "20 ", round(n20l, 8), "-", round(n20u, 8), round(np.nanmean(sucs[iveg == 20]),8) )
print( "21 ", round(n21l, 8), "-", round(n21u, 8), round(np.nanmean(sucs[iveg == 21]),8) )
print( "22 ", round(n22l, 8), "-", round(n22u, 8) , round(np.nanmean(sucs[iveg == 22]),8) )
print("\n")

n18l,n18u = ( np.nanmean(bch[iveg == 18])-np.nanstd(bch[iveg == 18]),
              np.nanmean(bch[iveg == 18])+np.nanstd(bch[iveg == 18]) )
n19l,n19u = ( np.nanmean(bch[iveg == 19])-np.nanstd(bch[iveg == 19]),
              np.nanmean(bch[iveg == 19])+np.nanstd(bch[iveg == 19]) )
n20l,n20u = ( np.nanmean(bch[iveg == 20])-np.nanstd(bch[iveg == 20]),
              np.nanmean(bch[iveg == 20])+np.nanstd(bch[iveg == 20]) )
n21l,n21u = ( np.nanmean(bch[iveg == 21])-np.nanstd(bch[iveg == 21]),
              np.nanmean(bch[iveg == 21])+np.nanstd(bch[iveg == 21]) )
n22l,n22u = ( np.nanmean(bch[iveg == 22])-np.nanstd(bch[iveg == 22]),
              np.nanmean(bch[iveg == 22])+np.nanstd(bch[iveg == 22]) )
print("BCH")
print( "18 ", round(n18l, 2), "-", round(n18u, 2), round(np.nanmean(bch[iveg == 18]),2) )
print( "19 ", round(n19l, 2), "-", round(n19u, 2), round(np.nanmean(bch[iveg == 19]),2) )
print( "20 ", round(n20l, 2), "-", round(n20u, 2), round(np.nanmean(bch[iveg == 20]),2) )
print( "21 ", round(n21l, 2), "-", round(n21u, 2), round(np.nanmean(bch[iveg == 21]),2) )
print( "22 ", round(n22l, 2), "-", round(n22u, 2) , round(np.nanmean(bch[iveg == 22]),2) )

"""
18  4.78 - 6.94 5.86
19  3.46 - 6.19 4.83
20  1.43 - 4.75 3.09
21  1.27 - 3.39 2.33
22  0.34 - 1.67 1.0
"""
#lai = np.where(iveg !=22, np.nan, lai)
#
#plt.imshow(lai)
#plt.colorbar()
#plt.show()
