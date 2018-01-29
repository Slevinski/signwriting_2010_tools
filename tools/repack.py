# repack.py is a python script to rewrite three files as a single tab delimited file
#
# Copyright (c) 2014-2015 Stephen E Slevinski Jr <slevin@signpuddle.net>
#
# License: MIT

import sys
import os
from time import gmtime, strftime
import re
import base64
import argparse
import glob

##################
# Argument Setup
##################
parser = argparse.ArgumentParser(description="SignWriting 2010 repacking script takes 3 datafiles and writes a single tab delimited file."
	,epilog="Source SVG and completed TTF available online https://github.com/slevinski/signwriting_2010_fonts")
parser.add_argument("datafile", nargs="?", help="name of the data file for output")
parser.add_argument("-f","--force", help="overwrite existing font files", action="store_true")
parser.add_argument("-t","--test", help="write one example to the screen", action="store_true")

args = parser.parse_args()


##################
# # initializing
##################
sourceDir = "../source/"

if not args.datafile:
	args.datafile = sourceDir + "symbol.txt"

if os.path.exists(args.datafile) and not args.test:
	if args.force:
		print "Overwriting data file " + args.datafile
	else:
		print
		print "FAILURE: Data file already exists: " + args.datafile
		print "Move file or use -f to force the file creation"
		print
		sys.exit(-1)

lines = [line.strip() for line in open("symsize.txt")]
sizes = {}
for line in lines:
	key = line[:6]
	w = line[7:9]
	h = line[11:13]
	sizes[key] = [w,h]

lines = [line.strip() for line in open(sourceDir + "svg_line.dat")]
svgL = {}
for line in lines:
	if line[0] != "#":
		parts = line.split("\t")
		key = parts[0]
		data = parts[1]
		data = data.replace('"/> <path d="', ' ');
		start = data.index("<g")
		end = data.index(">", start)+1
		dataG = data[start:end]
		start = data.index("<path")
		end = data.index(">", start)+1
		dataP = data[start:end]
		dataP = dataP.replace('<path ', '<path class="sym-line" ')
		svgL[key] = [dataG,dataP]

lines = [line.strip() for line in open(sourceDir + "svg_fill.dat")]
svgF = {}
for line in lines:
	if line[0] != "#":
		parts = line.split("\t")
		key = parts[0]
		data = parts[1]
		data = data.replace('"/> <path d="', ' ');
		start = data.index("<g")
		end = data.index(">", start)+1
		dataG = data[start:end]
		start = data.index("<path")
		end = data.index(">", start)+1
		dataP = data[start:end]
		dataP = dataP.replace('<path ', '<path class="sym-fill" fill="#ffffff" ')
		svgF[key] = [dataG,dataP]
		if svgL[key][0] != svgF[key][0]:
		  print "g element different for key " + key

if args.test:
	print "size: " + sizes['S10000'][0] + ',' + sizes['S10000'][1]
	print "line g: " + svgL['S10000'][0];
	print "line path: " + svgL['S10000'][1];
	print "fill g: " + svgF['S10000'][0];
	print "fill path: " + svgF['S10000'][1];
	sys.exit()

else:
	sys.stdout = open(args.datafile,'w') #redirect all prints to this log file

for key in svgL:
	print key + '\t' + sizes[key][0] + '\t' + sizes[key][1] + '\t' + svgL[key][0] + svgF.get(key,['',''])[1] + svgL[key][1] + '</g>'
	
