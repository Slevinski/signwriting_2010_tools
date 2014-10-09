# retrace.py is a python script to automate the retracing of the SVG Refinement
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
import math
import argparse
import time

start = time.time()

##################
# Argument Setup
##################
parser = argparse.ArgumentParser(description="Automated script creation to retrace the SVG Refinement"
	,epilog="Source SVG and completed TTF available online\nhttps://github.com/slevinski/signwriting_2010_fonts")
parser.add_argument("subfont", help="name of the subfont")
parser.add_argument("-c","--create", help="create sub directores for PNG, PNM, PBM, and SVG", action="store_true")
parser.add_argument("-d","--dir", required=True, metavar="directory", help="name of the sub-directory in sources for the SVG files")
parser.add_argument("-i","--inkscape", metavar="location", default="/Applications/Inkscape.app/Contents/Resources/script", help="location of inkscape script")
parser.add_argument("-s","--symbol", metavar="key", help="symbol key for individual symbol conversion")
parser.add_argument("-o","--output", nargs='?',metavar="filename", help="write to output file", default="NA")
args = parser.parse_args()

#################
# function defs
#################
def createDir(dir):
	if not os.path.isdir(dir):
		os.makedirs(dir)
		print "creating directory '" + dir + "'"
	else:
		print "overwriting directory '" + dir + "'"

##################
# # initializing
##################
args.subfont = (args.subfont.lower()).replace(' ','_')
if args.output != "NA":
		#temp = sys.stdout #store original stdout object for later
	outfilename = "retrace_" + args.subfont + ".sh"
	if args.output:
		outfilename = args.output
	print "writing to output file " + outfilename
	sys.stdout = open(outfilename,'w') #redirect all prints to this log file

sourceDir = os.path.abspath("../source/") + "/"

if args.create:
	createDir(sourceDir + "png_" + args.subfont)
	createDir(sourceDir + "pnm_" + args.subfont)
	createDir(sourceDir + "pbm_" + args.subfont)
	createDir(sourceDir + "svg_" + args.subfont)

if args.symbol:
	keylist=[args.symbol + " "]
else:
	keylist = open("symkeys.txt", "r")
for symkey in keylist:
	symkey = symkey[:-1]
	print args.inkscape + " " + sourceDir + args.dir + "/" + symkey + ".svg --export-png=" + sourceDir + "png_" + args.subfont + "/" + symkey + ".png -d 900"
	print "pngtopnm " + sourceDir + "png_" + args.subfont + "/" + symkey + ".png > " + sourceDir + "pnm_" + args.subfont + "/" + symkey + ".pnm" 
	print "mkbitmap " + sourceDir + "pnm_" + args.subfont + "/" + symkey + ".pnm -x -t 0.3 -o " + sourceDir + "pbm_" + args.subfont + "/" + symkey + ".pbm" 
	print "potrace " + sourceDir + "pbm_" + args.subfont + "/" + symkey + ".pbm -s -o " + sourceDir + "svg_" + args.subfont + "/" + symkey + ".svg" 
