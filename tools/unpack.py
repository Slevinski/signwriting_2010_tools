# unpack.py is a python script to expand a single file into a directory of glyphs
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
from time import gmtime, strftime
import re
import base64
import argparse
import glob

##################
# Argument Setup
##################
parser = argparse.ArgumentParser(description="SignWriting 2010 unpacking script takes a data file and creates a directory of files."
	,epilog="Source SVG and completed TTF available online https://github.com/slevinski/signwriting_2010_fonts")
parser.add_argument("datafile", nargs="?", help="name of the data file in sources for input")
parser.add_argument("-d","--dir", metavar="directory", help="name of directory in sources for output")
parser.add_argument("-i","--inverse", help="for SVG, switch black and white paths", action="store_true")
parser.add_argument("-s","--shadow", help="for SVG, switch all paths to black", action="store_true")
parser.add_argument("-m","--magnify", metavar="level", type=int, default=1, help="for SVG, magnification level, default of 1")
parser.add_argument("-v","--viewbox", help="for SVG, include viewBox", action="store_true")
parser.add_argument("-x","--xml", help="for SVG, adds XML and doctype declaration", action="store_true")
parser.add_argument("-t","--test", help="write one example to the screen", action="store_true")

args = parser.parse_args()


#################
# function defs
#################
def createDir(dir):
	if not os.path.isdir(dir):
		os.makedirs(dir)
		print "creating output in directory '" + dir + "'"
	else:
		print "overwriting directory '" + dir + "'"
		print "\tuse -d for a different dir"
		
##################
# # initializing
##################
sourceDir = "../source/"

if not args.datafile:
	files = glob.glob(sourceDir + "*dat")
	if not len(files):
		print ""
		print "FAILURE: no data files available for unpacking in " + sourceDir
	else:
		print
		print "Please specify a data file from " + sourceDir
		for file in files:
			print "\tpython unpack.py " + file.replace(sourceDir,'')
	sys.exit()

lines = [line.strip() for line in open("symsize.txt")]
sizes = {}
for line in lines:
	key = line[:6]
	w = line[7:9]
	h = line[11:13]
	sizes[key] = [w,h]

if os.path.exists(sourceDir + args.datafile):
	print "input data file " + sourceDir + args.datafile
else:
	print "FAILURE: data file " + sourceDir + args.datafile + " does not exist"
	sys.exit(-1)

if args.dir:
	fontDir = sourceDir + args.dir + "/"
else:
	fontDir = sourceDir + args.datafile.split('/')[-1].split('.')[0] + "/"

createDir(fontDir)

ext = (args.datafile[:3]).lower()

lines = [line.strip() for line in open(sourceDir + args.datafile)]
for line in lines:
	if line[0] != "#":
		parts = line.split("\t")
		key = parts[0]
		file = fontDir + key + "." + ext
		data = parts[1]
		if ext=="svg":
			if not "path" in data:
				continue
			if args.xml:
				svg = '<?xml version="1.0"?>' + "\n"
				svg += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"' + "\n\t"
				svg += '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">' + "\n"
				svg += '<svg xmlns="http://www.w3.org/2000/svg"'
			else:
				svg = '<svg'
			if 'class="sym-' in data:
				# source SVG with 2 colors
				if args.inverse:
					data = data.replace(' fill="#ffffff" class="sym-fill"','')
					data = data.replace(' class="sym-line"','  fill="#ffffff"')
				if args.shadow:
					data = data.replace(' fill="#ffffff"','')
			elif 'fill="#000000"' in data:
				# generated SVG with 1 colors
				if args.inverse:
					data = data.replace('fill="#000000"','fill="#ffffff"')
			else:
				if args.inverse:
					data = data.replace('<path','<path fill="#ffffff"')

			w = int(sizes[key][0]) * int(args.magnify)
			h = int(sizes[key][1]) * int(args.magnify)
			svg += ' width="' + str(w) + '" height="' + str(h) + '"'
			
			if args.viewbox:
				svg += ' viewBox="0 0 ' + sizes[key][0] + ' ' + sizes[key][1] + '"'
			svg += '>' + data + "</svg>"
			if args.test:
				print "file: " + file
				print "svg: " + svg
				sys.exit()
			f = open (file,'w')
			f.write(svg)
			f.close
		else:
			if args.test:
				print "file: " + file
				print "data: " + data
				sys.exit()
			f = open (file,'w')
			f.write(base64.b64decode(data))
			f.close

