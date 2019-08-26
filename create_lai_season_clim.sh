#!/bin/bash

cdo mergetime nc_files/lai/* nc_files/lai/joined.nc
cdo yseasmax nc_files/lai/joined.nc nc_files/lai/lai_max.nc
