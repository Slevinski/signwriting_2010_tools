# unpack.py is a python script to expand a single file into a directory of glyphs
#
# Copyright (c) 2014 Stephen E Slevinski Jr <slevin@signpuddle.net>
#
# License: MIT

import sys
import os
import base64
import argparse
import glob

##################
# Argument Setup
##################
parser = argparse.ArgumentParser(description="SignWriting 2010 unpacking script takes a data file and creates a directory of files."
	,epilog="Source SVG and completed TTF available online https://github.com/slevinski/signwriting_2010_fonts")
parser.add_argument("datafile", nargs="?", help="name of the data file in sources for input")
parser.add_argument("-a","--adjust", metavar="filename", help="file with symbol adjustment numbers from svg_bbox")
parser.add_argument("-b","--beta", metavar="filename", help="file with symbol adjustment numbers from svg_bbox of first adjustment")
parser.add_argument("-d","--dir", metavar="directory", help="name of directory in sources for output")
parser.add_argument("-i","--id", help="for SVG, use the symbol key as the ID of the SVG",action="store_true")
parser.add_argument("-r","--reverse", help="for SVG, switch black and white paths", action="store_true")
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
		print("creating output in directory '" + dir + "'")
	else:
		print("overwriting directory '" + dir + "'")
		print("\tuse -d for a different dir")

##################
# # initializing
##################
sourceDir = "../source/"

if not args.datafile:
	files = glob.glob(sourceDir + "*dat")
	if not len(files):
		print("")
		print("FAILURE: no data files available for unpacking in " + sourceDir)
	else:
		print
		print("Please specify a data file from " + sourceDir)
		for file in files:
			print("\tpython unpack.py " + file.replace(sourceDir,''))
	sys.exit()

lines = [line.strip() for line in open("symsize.txt")]
sizes = {}
for line in lines:
	key = line[:6]
	w = line[7:9]
	h = line[11:13]
	sizes[key] = [w,h]

if args.adjust:
	lines = [line.strip() for line in open(args.adjust)]
	sizesAdj = {}
	for line in lines:
		parts = line.split(',')
		key = parts[0]
		x = float(parts[1])
		y = float(parts[2])
		w = float(parts[3])
		h = float(parts[4])
		sizesAdj[key] = [x,y,w,h]

if args.beta:
	lines = [line.strip() for line in open(args.beta)]
	sizesBeta = {}
	for line in lines:
		parts = line.split(',')
		key = parts[0]
		x = float(parts[1])
		y = float(parts[2])
		w = float(parts[3])
		h = float(parts[4])
		sizesBeta[key] = [x,y,w,h]

if os.path.exists(sourceDir + args.datafile):
	print("input data file " + sourceDir + args.datafile)
else:
	print("FAILURE: data file " + sourceDir + args.datafile + " does not exist")
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

			if args.id:
				svg += ' id="' + key + '"';

			if 'class="sym-' in data:
				# source SVG with 2 colors
				if args.reverse:
					data = data.replace(' fill="#ffffff" class="sym-fill"','')
					data = data.replace(' class="sym-line"','  fill="#ffffff"')
				if args.shadow:
					data = data.replace(' fill="#ffffff"','')
			elif 'fill="#000000"' in data:
				# generated SVG with 1 colors
				if args.reverse:
					data = data.replace('fill="#000000"','fill="#ffffff"')
			else:
				if args.reverse:
					data = data.replace('<path','<path fill="#ffffff"')

			if args.viewbox:
				w = int(sizes[key][0]) * int(args.magnify)
				h = int(sizes[key][1]) * int(args.magnify)
				svg += ' width="' + str(w) + '" height="' + str(h) + '"'

				if args.viewbox:
					svg += ' viewBox="0 0 ' + sizes[key][0] + ' ' + sizes[key][1] + '"'
				svg += '>' + data + "</svg>"
			else:
				if int(args.magnify) != 1 or args.adjust:
					if args.adjust:
						aligned = sizesAdj[key][0]==0 and sizesAdj[key][1]==0 and sizesAdj[key][2]==int(sizes[key][0]) and sizesAdj[key][3]==int(sizes[key][1])
						if key in ['S2d50c','S2d51c','S2d52c','S3711c','S3712c','S38303']:
							aligned=False
						if key in ['S10914','S11114','S11144','S11604','S11614','S11704','S1300c','S1301c','S14104','S14124','S14144','S1585c','S16746','S17806','S1780e','S18502','S18922','S18952','S1895a','S19a0b','S19c2e','S1a902','S1a912','S1a93a','S1ab02','S1ab12','S1ab3e','S1ab5e','S1af04','S1af0c','S1af3c','S1b356','S22308','S2403e','S25f14','S26e00','S26e10','S28346','S28408','S28439','S28449','S2a220','S2b003','S32616','S37120']:
							aligned=False
						if key in ['S1415c','S1a92e','S1a92a','S1411c','S1171c','S29e2d','S1a926','S28459','S1af1c','S1ab32','S1781e','S14154','S1413c','S14114','S11714','S29e2a','S29d26','S2834a','S2531a','S24718','S24628','S2c825','S29e26','S29d1a','S28349','S25316','S24714','S24624','S1a922','S1091c','S1111c','S1160c','S1161c','S1170c','S1311c','S1314c','S1410c','S14134','S1414c','S1674e','S17816','S1801c','S18318','S1850a','S19b1c','S1a90a','S1a91a','S1a94a','S1ab2e','S1ab42','S1af14','S23e33','S24608','S24618','S24708','S24728','S24c2d','S2530a','S25411','S28151','S28345','S28418','S28451','S29d16','S29e0a','S29e1a','S2a228','S2c645','S2c815','S2de28','S2e42f','S32224']:
							aligned=False
					else:
						aligned = True;
					start = data.index("translate(")
					end = data.index(")", start)+1
					translate =data[start:end]
					start = translate.index("(")+1
					end = translate.index(",", start)
					transx = float(translate[start:end])
					start = translate.index(",")+1
					end = translate.index(")", start)
					transy = float(translate[start:end])

					start = data.index("scale(")
					end = data.index(")", start)+1
					scale =data[start:end]
					start = scale.index("(")+1
					end = scale.index(",", start)
					scalex = float(scale[start:end])*int(args.magnify)
					start = scale.index(",")+1
					end = scale.index(")", start)
					scaley =float(scale[start:end])*int(args.magnify)


					if not aligned:
						scaleAx = (int(sizes[key][0])-0.2)/(sizesAdj[key][2]+0.2);
						if (args.beta):
							scaleAx = scaleAx * (int(sizes[key][0])-0.4)/(sizesBeta[key][2]);
						scalex = scalex * scaleAx
						scaleAy = (int(sizes[key][1])-0.4)/(sizesAdj[key][3]+0.4)
						if (args.beta):
							scaleAy = scaleAy * (int(sizes[key][1])-0.4)/(sizesBeta[key][3]);
						scaley = scaley * scaleAy
					data=data.replace(scale,"scale(" + str(scalex) + "," + str(scaley) + ")")


					if not aligned:
						transx = ((sizesAdj[key][0]-0.2) * scaleAx) + 0.1
						if (args.beta):
							transx = transx + 0.15 - sizesBeta[key][0]
					if not aligned:
						transy = scaleAy * int(sizes[key][1]) + (sizesAdj[key][1] * scaleAy) + 0.1;
						if (args.beta):
							transy = transy + 0.15 - sizesBeta[key][1]

					transx = transx * int(args.magnify)
					transy = transy * int(args.magnify)
					data = data.replace(translate,"translate(" + str(transx) + "," + str(transy) + ")")


				w = int(sizes[key][0]) * int(args.magnify)
				h = int(sizes[key][1]) * int(args.magnify)
				svg += ' width="' + str(w) + '" height="' + str(h) + '"'
				svg += '>' + data + "</svg>"

			if args.test:
				print("file: " + file)
				print("svg: " + svg)
				sys.exit()
			f = open (file,'w')
			f.write(svg)
			f.close
		else:
			if args.test:
				print("file: " + file)
				print("data: " + data)
				sys.exit()
			f = open (file,'w')
			f.write(base64.b64decode(data))
			f.close

