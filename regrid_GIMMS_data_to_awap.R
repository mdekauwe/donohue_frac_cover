library(raster)

veg <- brick("lai_climatology.nc")

awap <- raster("/Users/mdekauwe/Desktop/AWAP.Tair.3hr.2000.nc")
regrid <- resample(veg, awap, method="bilinear")
writeRaster(regrid, "lai_climatology_AWAP_grid.nc", varname="LAI", zname="time",
            overwrite=TRUE)
