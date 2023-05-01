# pack.py is a python script to create a single file from a glyph directory
#
# Copyright (c) 2014 Stephen E Slevinski Jr <slevin@signpuddle.net>
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
parser = argparse.ArgumentParser(description="SignWriting 2010 packing script takes a directory of files and writes a single data file."
	,epilog="Source SVG and completed TTF available online https://github.com/slevinski/signwriting_2010_fonts")
parser.add_argument("directory", nargs="?", help="name of the sub-directory in sources for the subfont files")
parser.add_argument("-f","--force", help="overwrite existing font files", action="store_true")
parser.add_argument("-n","--name", metavar="filename", help="name of data file")
parser.add_argument("-m","--minimize", metavar="factor", help="for SVG, minimization factor for coordinate space")
parser.add_argument("-p","--precision", help="for SVG, number of decimal places for rounding", default="NA")
parser.add_argument("-s","--simplify", help="for SVG, remove extra text", action="store_true")
parser.add_argument("-t","--test", help="write one example to the screen", action="store_true")
parser.add_argument("-r","--reserved", default="SignWriting 2010", help="Reserved Font Name, default of %(default)s")

args = parser.parse_args()



##################
# # initializing
##################
sourceDir = "../source/"

if not args.directory:
	directories = os.walk( os.path.join(sourceDir,'.')).next()[1]
	directories.remove('other_svg')
	directories.remove('templates')
	if not len(directories):
		print("")
		print("FAILURE: no directory available for packing " + sourceDir)
	else:
		print()
		print("Please specify a directory from " + sourceDir)

		for dir in directories:
			print("python pack.py " + dir)
	sys.exit()

fontDir = sourceDir + args.directory + "/"
if args.name:
	args.directory = args.name

ext = (args.directory[:3]).lower()

dataFile = sourceDir + args.directory + ".dat"

if os.path.exists(dataFile) and not args.test:
	if args.force:
		print("Overwriting data file " + dataFile)
	else:
		print()
		print("FAILURE: Data file already exists: " + dataFile)
		print("Move file or use -f to force the file creation")
		print()
		sys.exit(-1)

if os.path.exists(fontDir):
	print("input directory " + fontDir)
	print("output data file " + dataFile)
else:
	print(f"FAILURE: directory {fontDir} does not exist")
	sys.exit(-1)

if not args.test:
	sys.stdout = open(dataFile,'w') #redirect all prints to this log file

print("# SignWriting 2010 is released under the SIL Open Font License, Version 1.1.")
print("# http://scripts.sil.org/OFL")
print("#")
print("# This Font Software is Copyright (c) 1974-2014")
print("# Center For Sutton Movement Writing, Inc.")
print("#")
print("# The symbols of SignWriting 2010 were designed by Valerie Sutton (sutton@signwriting.org),")
print("#\t inventor of the SignWriting Script")
print("#")
print("# The symbol images were refined by Adam Frost (frost@signwriting.org).")
print("#")
print("# The symbols were encoded, transformed, and refactored by Stephen E Slevinski Jr (slevin@signpuddle.net).")
print("#")
print("# Reserved Font Name: " + args.reserved)
print("#")
print("# SignWriting 2010 Packed Data")
print("# ------------------------------------")
print("#\tinput directory: " + args.directory)
print("#\toutput data file: " + dataFile.replace(sourceDir,""))
print("#\tprocessed: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print("# ------------------------------------")
print("# https://github.com/slevinski/signwriting_2010_tools")
print("#")
print("# created with command:",)
for item in sys.argv:
	if " " in item:
		print(f'"{item}"')
	else:
		print(item)
print()
print("#")
files = glob.glob(fontDir + "*" + ext)
for file in files:
	name = file.split('/')[-1].split('.')[0]
	with open(file, "rb") as image_file:
		data = image_file.read()
		if not ext=="svg":
			encoded_string = base64.b64encode(data)
			print(name + "\t" + encoded_string)
		else:
			#cleanup for various svg sources
			data = data.replace("\n"," ")
			start = data.index("<g")
			end = data.index("</g>", start)+4
			glines = data[start:end]
			if args.precision != "NA":
				glines = re.sub(r'\.[0-9]+',
				lambda m: (("%." + args.precision + "f") % float(m.group().strip()))[1:],
				glines).replace("." + "0"*int(args.precision),"")
			if args.simplify:
				glines = glines.replace(' fill="#000000" stroke="none"',"")
			if args.minimize:
				start = glines.index("translate(")
				end = glines.index(")", start)+1
				translate =glines[start:end]
				start = translate.index("(")+1
				end = translate.index(",", start)
				transx =int(translate[start:end])/int(args.minimize)
				start = translate.index(",")+1
				end = translate.index(")", start)
				transy =int(translate[start:end])/int(args.minimize)
				glines = glines.replace(translate,"translate(" + str(transx) + "," + str(transy) + ")")

				start = glines.index("scale(")
				end = glines.index(")", start)+1
				scale =glines[start:end]
				start = scale.index("(")+1
				end = scale.index(",", start)
				scalex =float(scale[start:end])/int(args.minimize)
				start = scale.index(",")+1
				end = scale.index(")", start)
				scaley =float(scale[start:end])/int(args.minimize)
				glines=glines.replace(scale,"scale(" + str(scalex) + "," + str(scaley) + ")")

			print(name + "\t" + glines)
		if args.test:
			sys.exit()
