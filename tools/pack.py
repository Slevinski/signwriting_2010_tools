# pack.py is a python script to create a single file from a glyph directory
#
# Copyright (c) 2014 Stephen E Slevinski Jr <slevin@signpuddle.net>
#
# License:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# This package is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import re
import base64
import argparse
import glob

##################
# Argument Setup
##################
parser = argparse.ArgumentParser(description="SignWriting 2010 packing script takes a directory of files and writes a single data file."
	,epilog="Source SVG and completed TTF available online https://github.com/slevinski/signwriting_2010_fonts")
parser.add_argument("directory", help="name of the sub-directory in sources for the subfont files")
parser.add_argument("-e","--ext", required=True, metavar="extension", help="name of the file extension for import, otherwise content sniffing")
parser.add_argument("-f","--force", help="overwrite existing font files", action="store_true")
parser.add_argument("-p","--precision", help="number of decimal places for rounding", default="NA")
parser.add_argument("-n","--name", metavar="filename", help="name of data file")
parser.add_argument("-t","--test", help="write one example to the screen", action="store_true")
args = parser.parse_args()



##################
# # initializing
##################
sourceDir = "../source/"
fontDir = sourceDir + args.directory + "/"
if args.name:
	dataFile = sourceDir + args.name + ".dat"
else:
	dataFile = sourceDir + args.directory + ".dat"


if os.path.exists(fontDir):
	print "packig directory " + fontDir
else:
	print "FAILURE: directory " + fontDir + " does not exist"
	sys.exit(-1)

if not args.test:
	sys.stdout = open(dataFile,'w') #redirect all prints to this log file

files = glob.glob(fontDir + "*" + args.ext)
for file in files:
	name = file.split('/')[-1].split('.')[0]
	with open(file, "rb") as image_file:
		data = image_file.read()
		if args.ext.lower()=="png":
			encoded_string = base64.b64encode(data)
			print name + "\t" + encoded_string
		else:
			data = data.replace("\n"," ")
			start = data.index("<g")
			end = data.index("</g>", start)+4
			glines = data[start:end]
			if args.precision != "NA":
				glines = re.sub(r'\.[0-9]+', 
				lambda m: (("%." + args.precision + "f") % float(m.group().strip()))[1:],
				glines).replace("." + "0"*int(args.precision),"")
    		print name + "\t" + glines
		if args.test:
			sys.exit()
