# build.py is a python script to create the Sutton SignWriting fonts 
#    by importing SVG glyphs and merging feature files.
#
# Copyright (c) 2014-2017 Stephen E Slevinski Jr <slevin@signpuddle.net>
#
# License: MIT
#
# Reference
# http://fontforge.org/scripting-tutorial.html
# http://www.adobe.com/devnet/opentype/afdko/topic_feature_file_syntax.html#4
# http://fontforge.org/scripting-alpha.html
# http://fontforge.org/python.html#f-createChar

import sys
import fontforge
import psMat
import os
import math
import argparse
from array import array
import time
from stat import * # ST_SIZE etc
import glob

__version__ = '2.2.0'

start = time.time()

##################
# Argument Setup
##################
parser = argparse.ArgumentParser(description="Sutton SignWriting build script for TTF files from SVG (version " + __version__ + ")"
	,epilog="Source SVG and completed TTF available online https://github.com/slevinski/signwriting_2010_fonts")
parser.add_argument("subfont",nargs='?',choices=['Line', 'Fill', 'OneD', '8', '1d', '1dOpt', 'Null'], help="name of the subfont")
parser.add_argument("-a","--fea", help="include Unicode 8 features", action="store_true")
parser.add_argument("-b","--beta", help="include beta design to overwrite Unicode 8", action="store_true")
parser.add_argument("-c","--custom", metavar="filename", default="custom.txt", help="name of font customization file, default of %(default)s")
parser.add_argument("-d","--dir", metavar="directory", help="name of the sub-directory in sources for the subfont files")
parser.add_argument("-e","--ext", metavar="extension", default="svg", help="name of the file extension for import, default of %(default)s")
parser.add_argument("-f","--force", help="overwrite existing font files", action="store_true")
parser.add_argument("-g","--glyph", metavar="filename", default="glyph.txt", help="name of glyph customization file, default of %(default)s")
parser.add_argument("-k","--keys", metavar="filename", default="symkeys.txt", help="name of symbol key file, default of %(default)s")
parser.add_argument("-i","--ident", metavar="version", default="1.1.0", help="version of the Sutton SignWriting Fonts, default of %(default)s")
parser.add_argument("-l","--log", nargs='?',metavar="filename", help="write to log file", default="NA")
parser.add_argument("-m","--mono", help="helper flag for naming, import, and functions (partial support)", action="store_true")
parser.add_argument("-p","--preview", help="perform all of the actions but generating the TTF output", action="store_true")
parser.add_argument("-q","--quick", help="skip creation of glyphs, characters, and feature file merge", action="store_true")
parser.add_argument("-s","--silent", help="eliminates the print output", action="store_true")
parser.add_argument("-t","--title", metavar="fontname", default="SuttonSignWriting", help="prefix for the various font names and files, default of %(default)s")
parser.add_argument("-u","--unicode", metavar="unicode", help="Unicode plane number")
parser.add_argument("-v","--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-x","--next", help="include 17 control characters for Unicode next", action="store_true")
args = parser.parse_args()

#################
# function defs
#################
def unichar(uni):
        code = int(uni,16)
        try:
                return unichr(code)
        except ValueError:
                return unichr( 0xd800 + ((code-0x10000)//0x400) ) \
                        +unichr( 0xdc00 + ((code-0x10000)% 0x400) )

def key2code(key,plane):
	return (int(plane + '0000',16) + ((int(key[1:4],16) - 256) * 96) + ((int(key[4:5],16))*16) + int(key[5:6],16) + 1)

##################
# # initializing
##################
sourceDir = "../source/"

if args.mono:
	underPostfix = "_Mono"
	fontPostfix = " Mono"
else:
	underPostfix = ''
	fontPostfix = ''

if args.subfont:
	underPostfix = underPostfix + args.subfont
	fontPostfix = fontPostfix + args.subfont

fontTitle = args.title
underTitle = fontTitle
fontfilename ="../fonts/" + fontTitle + fontPostfix + ".ttf";
logfilename ="../fonts/" + fontTitle + fontPostfix + ".log";

if args.silent:
	if args.verbose:
		print "devnull"
	f = open(os.devnull, 'w') #redirect all prints to this log file
	sys.stdout = f
else:
	if args.log != "NA":
		
		#temp = sys.stdout #store original stdout object for later
		if args.log:
			logfilename = args.log
		sys.stdout = open(logfilename,'w') #redirect all prints to this log file

if args.verbose:
	for item in sys.argv:
		if " " in item:
			print '"' + item + '"',
		else:
			print item,
	print
	print
	print "SignWriting 2010 Tools project"
	print "-------------------------------"
	print "\tversion " + __version__
	print "-------------------------------"
	print "https://github.com/slevinski/signwriting_2010_tools"
	print 
	print "verbosity turned on"
	if args.mono:
		print
		print "mono sized"
	print
	print "using Unicode plane " + args.unicode
	print
else:
	print
	print "Building font..."

# symbol key input file
if os.path.exists(args.keys):
	if args.verbose:
		print "using symbol key file " + args.keys
# if args.keys != "symkeys.txt":
# 	args.quick = True;

if args.dir:
	fontDir = sourceDir + args.dir + "/"
	# check directory
	if os.path.exists(fontDir):
		if args.verbose:
			print "using directory " + fontDir + " for import files"
	else:
		print "FAILURE: directory " + fontDir + " does not exist"
		sys.exit(-1)
elif args.subfont == "Null":
	if args.verbose:
		print "using null.svg for import"
else:
	directories = os.walk( os.path.join(sourceDir,'.')).next()[1]
	directories.remove('templates')
	if not len(directories):
		print ""
		print "FAILURE: no directory of import files available in the directory " + sourceDir
	else:
		print
		print "FAILURE: use the -d arguement with one of the following options from the directory " + sourceDir

		for dir in directories:
			print "-d " + dir

	sys.exit(-1)

if args.verbose:
	print "using extension " + args.ext

if os.path.exists(fontfilename):
	if args.force:
		if args.verbose:
			print
			print "Overwriting font file " + fontfilename
	elif not args.preview:
		print
		print "FAILURE: File already exists: " + fontfilename
		print "Move file or use -f to force the file creation"
		print
		sys.exit(-1)


if args.verbose:
	print
	print"Font initilization"
font = fontforge.font()
font.fontname = underTitle + underPostfix
font.familyname = fontTitle + fontPostfix
font.fondname = fontTitle + fontPostfix
font.fullname = fontTitle + fontPostfix
font.fontlog = "August 2016 Update"
font.version = args.ident

if args.verbose:
	print
	print "Custom settings file: " + args.custom
lines = [line.strip() for line in open(args.custom)]
for line in lines:
	if line[0] != "#":
		parts = line.split('=')
		if (args.verbose):
			print "\tsetting: " + parts[0] + " as " + parts[1]
		if parts[1][0]=='"':
			parts[1] = parts[1].replace('"','').replace('\\n','\n')
			setattr(font,parts[0],parts[1])
		else:
			setattr(font,parts[0],int(parts[1]))

#UnderlinePosition: -133
#UnderlineWidth: 20
#WidthSeparation: 140
#LayerCount: 2
#Layer: 0 0 "Back" 1
#Layer: 1 1 "Fore" 0
#DisplaySize: -24
#DisplayLayer: 1
#font.antialias = 1
#font.size_feature(16);


char = font.createChar(0, ".notdef")

glfset = [line.strip() for line in open(args.glyph)]

if args.verbose:
	print
	print "Glyph settings file: " + args.glyph
	for line in glfset:
		if line[0] != "#":
			if "=" in line:
				parts = line.split('=')
				print "\tsetting: " + parts[0] + " as " + parts[1]
			else:
				print "\tcalling: " + line

if args.beta or args.next:
	args.size = "symsize.txt"
	lines = [line.strip() for line in open(args.size)]
	sizes = {}
	for line in lines:
	        key = line[:6]
	        w = line[7:9]
	        h = line[11:13]
	        sizes[key] = [w,h]

	if args.verbose:
		print
		print "Glyph size file: " + args.size
		

glfCnt=0;
glfTtl=0;
glfStart = time.time()
print
print "ISWA 2010 Glyphs"
if args.verbose:
	print "\tload file " + args.keys
infile = open(args.keys, "r")
missing = 0
codepoint = -1

for symkey in infile:
	planes = args.unicode.split('_')

	for idx,plane in enumerate(planes):

		glfTtl = glfTtl + 1
		if idx == 0:
			glyph_name = symkey[:-1]
		else:
			glyph_name = symkey[:-1] + " " + plane
		if args.verbose:
			glfCnt = glfCnt + 1
			if glfCnt==60:
				print glyph_name,
				sys.stdout.flush()
				glfCnt=0
		else:
			glfCnt = glfCnt + 1
			if glfCnt==1150:
				print ".",
				sys.stdout.flush()
				glfCnt=0


		codepoint = key2code(glyph_name,plane)
		
		char = font.createChar(codepoint,glyph_name)

		if args.subfont == "Null":
			char.importOutlines(sourceDir + "other_svg/null.svg");
		else:
			filename = fontDir + glyph_name + "." + args.ext
			if os.path.isfile(filename):
				char.importOutlines(filename)
			else:
				missing += 1

		#		glyph = char.background
		#		glyph.removeOverlap();
		#		char.activeLayer=0
		#		char.clear();
		#		char.background=glyph;

		for line in glfset:
			if line[0] != "#":
				if "=" in line: 
					parts = line.split('=')
					if parts[1][0]=='"':
						parts[1] = parts[1].replace('"','')
						setattr(char,parts[0],parts[1])
					else:
						setattr(char,parts[0],int(parts[1]))
				else:
					getattr(char, line)()

		if args.beta or args.next:
			char.transform(psMat.translate(0,int(sizes[glyph_name][1])*5-135))
			setattr(char,"width",int(sizes[glyph_name][0])*10+40);  # bearing 20 each side



		if args.verbose:
			glfCnt = glfCnt + 1
			if glfCnt==60:
				print glyph_name,
				sys.stdout.flush()
				glfCnt=0
		else:
			glfCnt = glfCnt + 1
			if glfCnt==1150:
				print ".",
				sys.stdout.flush()
				glfCnt=0


print "OK"

if missing == 37811:
	print
	print "FAILURE: no files with extension " + args.ext + " in directory " + fontDir
	sys.exit(-1)

glfEnd = time.time()


if not args.quick:

	if args.fea:
		chrStart = time.time()

		#Unicode 8
		uniCnt=0;
		uniTtl=0;
		print
		print "Unicode 8 Characters"
		for codigo in range(0x1D800,0x1DAAF+1):
			uniTtl = uniTtl + 1
			char_name = "%x" % (codigo)
			char_name = "u" + char_name.upper();
			if args.verbose:
				print char_name,
				sys.stdout.flush()
			else:
				uniCnt = uniCnt + 1
				if uniCnt==20:
					print ".",
					sys.stdout.flush()
					uniCnt=0

			char = font.createChar(codigo,char_name);
			char.importOutlines(sourceDir + "other_svg/placeholder.svg");
		print "OK"

		chrEnd = time.time()
	
		feaStart = time.time()
		print
		print "Merging Unicode 8 Features",
		sys.stdout.flush()
		if args.subfont == "1d":
			font.mergeFeature(sourceDir + "signwriting_2010_unicode1D.fea");
			font.mergeFeature(sourceDir + "signwriting_2010_unicode1Dliga.fea");
		else:
			font.mergeFeature(sourceDir + "signwriting_2010_unicode8.fea");
		print "OK"
		feaEnd = time.time()

	transY = -25;
	if args.beta:
		chrStart = time.time()

		#beta design overwrites Unicode 8
		uniCnt=0;
		uniTtl=0;
		print
		print "Beta design overwrites Unicode 8 Characters"
		print "\tstructural markers: ABLMR"
		codigo = 0x1D800
		char = font.createChar(codigo,"SW A");
		char.importOutlines(sourceDir + "other_svg/swA.svg");
		char.transform(psMat.translate(0,transY))
		setattr(char,"left_side_bearing",20);
		setattr(char,"right_side_bearing",20);

		codigo = 0x1D801
		char = font.createChar(codigo,"SW B");
		char.importOutlines(sourceDir + "other_svg/swB.svg");
		char.transform(psMat.translate(0,transY))
		setattr(char,"left_side_bearing",20);
		setattr(char,"right_side_bearing",20);

		codigo = 0x1D802
		char = font.createChar(codigo,"SW L");
		char.importOutlines(sourceDir + "other_svg/swL.svg");
		char.transform(psMat.translate(0,transY))
		setattr(char,"left_side_bearing",20);
		setattr(char,"right_side_bearing",20);

		codigo = 0x1D803
		char = font.createChar(codigo,"SW M");
		char.importOutlines(sourceDir + "other_svg/swM.svg");
		char.transform(psMat.translate(0,transY))
		setattr(char,"left_side_bearing",20);
		setattr(char,"right_side_bearing",20);

		codigo = 0x1D804
		char = font.createChar(codigo,"SW R");
		char.importOutlines(sourceDir + "other_svg/swR.svg");
		char.transform(psMat.translate(0,transY))
		setattr(char,"left_side_bearing",20);
		setattr(char,"right_side_bearing",20);

		print "OK"
		print "\tnumbers: 250-749"
		for codigo in range(0x1D80C,0x1D9FF+1):
			uniTtl = uniTtl + 1
			char_name = "%x" % (codigo)
			char_name = "u" + char_name.upper();
			glyph_num = str(249 + uniTtl);
			if args.verbose:
				print char_name,
				sys.stdout.flush()
			else:
				uniCnt = uniCnt + 1
				if uniCnt==20:
					print ".",
					sys.stdout.flush()
					uniCnt=0

			char = font.createChar(codigo,"SW " + glyph_num);
			char.importOutlines(sourceDir + "other_svg/sw" + glyph_num + ".svg");
			char.transform(psMat.translate(0,transY))
			setattr(char,"width",75);
			setattr(char,"left_side_bearing",10);
			setattr(char,"right_side_bearing",10);
		print "OK"

		chrEnd = time.time()

	if args.next:
		chrStart = time.time()

		# 8 Unicode plus 17 characters
		uniCnt=0;
		uniTtl=0;
		print
		print "8 Unicode plus 17 characters"
		print "\tstructural markers: ABLMR"
		codigo = 0x1DABA
		char = font.createChar(codigo,"SW A");
		char.importOutlines(sourceDir + "other_svg/swA.svg");
		char.transform(psMat.translate(0,transY))
		setattr(char,"left_side_bearing",20);
		setattr(char,"right_side_bearing",20);

		codigo = 0x1DABB
		char = font.createChar(codigo,"SW B");
		char.importOutlines(sourceDir + "other_svg/swB.svg");
		char.transform(psMat.translate(0,transY))
		setattr(char,"left_side_bearing",20);
		setattr(char,"right_side_bearing",20);

		codigo = 0x1DABC
		char = font.createChar(codigo,"SW L");
		char.importOutlines(sourceDir + "other_svg/swL.svg");
		char.transform(psMat.translate(0,transY))
		setattr(char,"left_side_bearing",20);
		setattr(char,"right_side_bearing",20);

		codigo = 0x1DABD
		char = font.createChar(codigo,"SW M");
		char.importOutlines(sourceDir + "other_svg/swM.svg");
		char.transform(psMat.translate(0,transY))
		setattr(char,"left_side_bearing",20);
		setattr(char,"right_side_bearing",20);

		codigo = 0x1DABE
		char = font.createChar(codigo,"SW R");
		char.importOutlines(sourceDir + "other_svg/swR.svg");
		char.transform(psMat.translate(0,transY))
		setattr(char,"left_side_bearing",20);
		setattr(char,"right_side_bearing",20);

		print "OK"
		print "\tnumbers: 0-9"
		for codigo in range(0x1DAB0,0x1DAB9+1):
			char_name = "%x" % (codigo)
			char_name = "u" + char_name.upper();
			glyph_num = str(uniTtl);
			uniTtl = uniTtl + 1
			if args.verbose:
				print char_name,
				sys.stdout.flush()

			char = font.createChar(codigo,"SW " + glyph_num);
			char.importOutlines(sourceDir + "other_svg/sw" + glyph_num + ".svg");
			char.transform(psMat.translate(0,transY))
			setattr(char,"width",150);
			setattr(char,"left_side_bearing",10);
			setattr(char,"right_side_bearing",10);
		print "OK"

		chrEnd = time.time()


if args.preview:
	print
	print "Skipping Font File Generation"
else:
	genStart = time.time()
	print
	print "Generating Font File..."
	font.generate(fontfilename);
	print
	print "OK"
	genEnd = time.time()

if args.verbose:
	end = time.time()
	elapsed = end - start
	print
	print "Elapsed time of ", '%.1f'%(elapsed), "seconds."
	if not args.quick:
		print "\t" + '%.1f'%(glfEnd-glfStart), "seconds to create " + str(glfTtl) + " glyphs",
		if missing:
			print "minus " + str(missing) + " glyphs not imported"
		else:
			print

		if args.fea:
			print "\t" + '%.1f'%(chrEnd-chrStart), "seconds to create " + str(uniTtl) + " characters" 
			print "\t\t" + str(uniTtl) + " Unicode 8 characters"
			print "\t" + '%.1f'%(feaEnd-feaStart), "seconds to merge features" 
		print "\t" + '%.1f'%(genEnd-genStart), "seconds to generate font file" 

if not args.preview:
	#file details
	print
	print "Wrote font file " + fontfilename
	if args.verbose:
		try:
	   		st = os.stat(fontfilename)
		except IOError:
			print "\tfailed to get information about", fontfilename
		else:
			print "\tfile created: " ,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st[ST_CTIME]))

			bytes = st[ST_SIZE]
			log = math.floor(math.log(bytes, 1024))
			print "\tfile size: %.*f %s" % (
			2,
			bytes / math.pow(1024, log),
			['bytes', 'KB', 'MB']
			[int(log)]
			)
