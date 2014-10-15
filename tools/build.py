# build.py is a python script to create the SignWriting 2010 fonts 
#    by importing SVG glyphs and merging feature files.
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
#
# Reference
# http://fontforge.org/scripting-tutorial.html
# http://www.adobe.com/devnet/opentype/afdko/topic_feature_file_syntax.html#4
# http://fontforge.org/scripting-alpha.html
# http://fontforge.org/python.html#f-createChar

import sys
import fontforge
import os
import math
import argparse
from array import array
import time
from stat import * # ST_SIZE etc
import glob

__version__ = '1.2.0'

start = time.time()

##################
# Argument Setup
##################
parser = argparse.ArgumentParser(description="SignWriting 2010 build script for TTF files from SVG (version " + __version__ + ")"
	,epilog="Source SVG and completed TTF available online https://github.com/slevinski/signwriting_2010_fonts")
parser.add_argument("subfont",nargs='?',choices=['', 'Filling', 'Shadow'], help="name of the subfont")
parser.add_argument("-c","--custom", metavar="filename", default="custom.txt", help="name of font customization file, default of %(default)s")
parser.add_argument("-d","--dir", metavar="directory", help="name of the sub-directory in sources for the subfont files")
parser.add_argument("-e","--ext", metavar="extension", default="svg", help="name of the file extension for import, default of %(default)s")
parser.add_argument("-f","--force", help="overwrite existing font files", action="store_true")
parser.add_argument("-g","--glyph", metavar="filename", default="glyph.txt", help="name of glyph customization file, default of %(default)s")
parser.add_argument("-i","--iswa", metavar="version", default="1.10.1", help="version of the ISWA 2010, default of %(default)s")
parser.add_argument("-l","--log", nargs='?',metavar="filename", help="write to log file", default="NA")
parser.add_argument("-m","--mono", help="helper flag for naming, import, and functions (partial support)", action="store_true")
parser.add_argument("-p","--preview", help="perform all of the actions but generating the TTF output", action="store_true")
parser.add_argument("-q","--quick", help="skip creation of glyphs, characters, and feature file merge", action="store_true")
parser.add_argument("-s","--silent", help="eliminates the print output", action="store_true")
parser.add_argument("-t","--title", metavar="fontname", default="SignWriting 2010", help="prefix for the various font names and files, default of %(default)s")
parser.add_argument("-u","--unicode", help="use Unicode code points for individual glyphs", action="store_true")
parser.add_argument("-v","--verbose", help="increase output verbosity", action="store_true")
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

def key2code(key):
	return (int('100000',16) + ((int(key[1:4],16) - 256) * 96) + ((int(key[4:5],16))*16) + int(key[5:6],16) + 1)

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
	underPostfix = underPostfix + "_" + args.subfont
	fontPostfix = fontPostfix + " " + args.subfont

fontTitle = args.title
underTitle = fontTitle.replace(" ","_");
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
	if args.unicode:
		print
		print "using Unicode codepoints for glyphs"
	print
else:
	print
	print "Building font..."

if args.dir:
	fontDir = sourceDir + args.dir + "/"
	# check directory
	if os.path.exists(fontDir):
		if args.verbose:
			print "using directory " + fontDir + " for import files"
	else:
		print "FAILURE: directory " + fontDir + " does not exist"
		sys.exit(-1)
else:
	directories = os.walk( os.path.join(sourceDir,'.')).next()[1]
	directories.remove('other_svg')
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
font.fontlog = "Create October 2014"
font.version = args.iswa

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


font.createChar(0, ".notdef")

if not args.quick:
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

	glfCnt=0;
	glfTtl=0;
	glfStart = time.time()
	print
	print "ISWA 2010 Glyphs"
	if args.verbose:
		print "\tload file symkeys.txt"
	infile = open("symkeys.txt", "r")
	missing = 0
	codepoint = -1
	for symkey in infile:
		glfTtl = glfTtl + 1
		glyph_name = symkey[:-1]
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

		if args.unicode:
			codepoint = key2code(glyph_name)
		char = font.createChar(codepoint,glyph_name)

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

	print "OK"
	
	if missing == 37811:
		print
		print "FAILURE: no files with extension " + args.ext + " in directory " + fontDir
		sys.exit(-1)
	
	glfEnd = time.time()

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

	#Unicode PUA
	puaCnt=0;
	puaTtl=0;
	print
	print "Unicode PUA Characters"
	for codigo in range(0xFD810,0xFDABF+1):
		puaTtl = puaTtl + 1
		char_name = "%x" % (codigo)
		char_name = "u" + char_name.upper();
		if args.verbose:
			print char_name,
			sys.stdout.flush()
		else:
			puaCnt = puaCnt + 1
			if puaCnt==20:
				print ".",
				sys.stdout.flush()
				puaCnt=0

		char = font.createChar(codigo,char_name);
		char.importOutlines(sourceDir + "other_svg/placeholder.svg");
	print "OK"

	# ASCII support of symbol keys
	# S
	chrCnt=0;
	chrTtl=0;
	print
	print "Symbol Key Characters"
	char_name = chr(83);
	chrTtl = chrTtl + 1
	print char_name,
	sys.stdout.flush()
	char = font.createChar(83,char_name);
	char.importOutlines(sourceDir + "other_svg/" + char_name + ".svg");

	#ASCII support for numbers 0-9
	numbers = ['zero','one','two','three','four','five','six','seven','eight','nine'];
	for codigo in range(0x30,0x39+1):
		char_name = numbers[(codigo-0x30)];
		chrTtl = chrTtl + 1
		print char_name,
		sys.stdout.flush()
		char = font.createChar(codigo,char_name);
		char.importOutlines(sourceDir + "other_svg/" + char_name + ".svg");
	
	#ASCII support for hex letters a-f
	for codigo in range(0x61,0x66+1):
		char_name = chr(codigo);
		chrTtl = chrTtl + 1
		print char_name,
		sys.stdout.flush()
		char = font.createChar(codigo,char_name);
		char.importOutlines(sourceDir + "other_svg/" + char_name + ".svg");
	print "OK"

	chrEnd = time.time()
	
	feaStart = time.time()
	print
	print "Merging Unicode 8 Features",
	sys.stdout.flush()
	font.mergeFeature(sourceDir + "signwriting_2010_unicode8.fea");
	print "OK"

	print "Merging Unicode PUA Features",
	sys.stdout.flush()
	font.mergeFeature(sourceDir + "signwriting_2010_unicode_pua.fea");
	print "OK"

	print "Merging Symbol Key Features",
	sys.stdout.flush()
	font.mergeFeature(sourceDir + "signwriting_2010_symbolkey.fea");
	print "OK"
	feaEnd = time.time()

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
		print "\t" + '%.1f'%(chrEnd-chrStart), "seconds to create " + str(uniTtl + puaTtl + chrTtl) + " characters" 
		print "\t\t" + str(uniTtl) + " Unicode 8 characters"
		print "\t\t" + str(puaTtl) + " Unicode Private Use Area characters"
		print "\t\t" + str(chrTtl) + " Symbol Key characters"
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
