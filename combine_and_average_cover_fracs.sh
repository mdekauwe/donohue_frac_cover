#!/bin/bash
#
# Merge files and generate an average fper and frec file
#
# author: Martin De Kauwe"
# date: 30.07.2019
#

cdo mergetime nc_files/fper/*.nc nc_files/fper/mean_fper.nc
cdo ensmean nc_files/fper/mean_fper.nc test.nc
mv test.nc nc_files/fper/mean_fper.nc

cdo mergetime nc_files/frec/*.nc nc_files/frec/mean_frec.nc
cdo ensmean nc_files/frec/mean_frec.nc test.nc
mv test.nc nc_files/frec/mean_frec.nc
