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
import datetime
import os
import sys

def main():

    fper_files = glob.glob("nc_files/fper/*.nc")
    frec_files = glob.glob("nc_files/frec/*.nc")

    for fper_fname, frec_fname in zip(fper_files, frec_files):
        fper = xr.open_dataset(fper_fname)
        frec = xr.open_dataset(frec_fname)

        plt.imshow(frec.frec)
        plt.colorbar()
        sys.exit()

if __name__ == "__main__":

    main()
