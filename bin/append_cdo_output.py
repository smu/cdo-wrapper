#!/usr/bin/python2
#
#  append_cdo_output.py
#
#  Stefan Muthers <muthers@climate.unibe.ch>
#
#  2012-02-12
#
#
#  Append the output of a cdo command to a existing file.
#
#  This script is used in situations were the amount of data is growing in time, e.g.,
#  the output from an ungoing climate model simulations.
#
#  Lets explain it using the following example:
#
#     $ ./append_cdo_output -f nc -selvar,temp2 $model_output/*BOT_mm*.nc 2m_temperatures.nc
#
#   With the first call, the example command above basically does a simple
#
#    $ cdo -f nc -selvar,temp2 $model_output/*BOT_mm*.nc 2m_temperatures.nc
#
#   With the second call, however, append_cdo_output first checks the output file
#   (2m_temperatures.nc) for the dates which were already extracted and appends only the
#   the data from  $model_output/*BOT_mm*.nc to the output file, which has not been
#   processed in the previous run.
# 
# 
#
#

import os
import sys
import subprocess
import shlex
import tempfile
import shutil

def get_dates(file):
	cmd = shlex.split("cdo -s showdate %s" % file)
	p = p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	p.wait()
	if p.stdout:
		dates = p.stdout.readlines()[0].split()
	else:
		print 'ERROR: STDOUT not available'
		sys.exit(1)
	return dates

def append_new(cmd, files, outfile, overwrite=False):
	if os.path.exists(outfile):
		# we assume that the number/choice of variables did not change
		# get existing dates
		dates = get_dates(outfile)
		# check all files, wheither first date already present in outfile
		# if yes, remove file from filelist
		files = [f for f in files if get_dates(f)[0] not in dates]
		# extract new dates to new file
		if len(files) > 0:
			tmpfile = tempfile.mktemp()
			cmd = shlex.split("%s %s %s" % (cmd, ' '.join(files), tmpfile))
			subprocess.call(cmd)
			# merge with existing file
			tmpfile2 = tempfile.mktemp()
			cmd = shlex.split("cdo -s mergetime %s %s %s" % (tmpfile, outfile, tmpfile2))
			subprocess.call(cmd)
			shutil.move(tmpfile2, outfile)
		else:
			print "%s already up-to-date" % outfile
	else:
		cmd = shlex.split("%s %s %s" % (cmd, ' '.join(files), outfile))
		subprocess.call(cmd)
	return

def usage():
	print 'usage'
	print "%s <cdo command> <inputfile> [inputfile, ...] <outputfile>" % sys.argv[0]
	sys.exit(1)



if __name__ == '__main__':

	length = len(sys.argv)
	if (length < 4):
		usage()
	
	cmd = sys.argv[1]
	target_file = sys.argv[length-1]
	files = sys.argv[2:length-1]

	append_new(cmd, files, target_file)



