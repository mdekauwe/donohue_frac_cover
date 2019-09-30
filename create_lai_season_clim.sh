#!/bin/bash

i=0
for F in nc_files/lai/gimms3g-lai-bimonth-*;
do
    echo $i $F
    if [ $i -eq 0 ]; then
        previous=$F
        echo $previous
    elif [ $i -eq 1 ]; then
        cdo mergetime $previous $F tmp.nc
    elif [ $i -gt 1 ]; then
        cdo mergetime tmp.nc $F tmp2.nc
        mv tmp2.nc tmp.nc
    fi

    i=$((i+1))
done
mv tmp.nc nc_files/lai/joined.nc

cdo ymonmean nc_files/lai/joined.nc nc_files/lai/lai_climatology.nc
