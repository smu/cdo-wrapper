#!/bin/bash
#
#
# Stefan Muthers <muthers@climate.unibe.ch>
# 
#  2012-xx-xx
# 
#  
# A simple bash script to extract the available dates from a 
# netcdf/grib file to detect missing or double values.
#


file=$1

if [ ! -e $file ] ; then
	echo "$file does not exists."
	exit 1
fi

years=`cdo -s showyear $file`

for y in $years; do
	echo -n "$y :"
	mon=`cdo -s -showmon -selyear,$y $file`
	n=`cdo -s -ntime -selyear,$y $file`
	echo "$mon ($n)"
done
