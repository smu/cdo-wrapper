#!/bin/bash
#
# Stefan Muthers <muthers@climate.unibe.ch>
#
#  around 2012
#
#
#
#
# Multiple variables from a number of netcdf/grib files can easily extracted 
# with
#
#    $ cdo -select,name=var1,var2 file1 file2 ... filen outputfile
#
# However, when the files differ in some aspects, e.g., the number of variables is
# different between file1 and file2, this may fail with an error message like:
#
#   do select (Abort): Input streams have different number of records per timestep!
# 
# In these situations this script can be used. 
#
# It loops over all files from file1 to filen and extract the variables to a temporary
# file, which is merged afterwards using 'cdo mergtime ...'
# Due to the loop it is less efficient than the 'cdo -select' command.
#  

set -e

CDOARG='-s'

variables=$1
shift
eval outfile=\${$#}
numArgs="$#"

if [ -e $outfile ]; then
	echo Outputfile exists: $outfile
	exit 1
fi

tmpfiles=
for i in `seq $(($numArgs-1))` ; do
	tmp=`tempfile --directory='.'`
	cdo ${CDOARG} selvar,$variables $1 $tmp
	tmpfiles="${tmpfiles} $tmp"
	shift
done

#echo NUmargs: $numArgs
#echo Variable: $variables
#echo Last Command Line Arg: $outfile
#echo Input: $infiles

cdo ${CDOARG} mergetime $tmpfiles $outfile

rm -rf $tmpfiles
