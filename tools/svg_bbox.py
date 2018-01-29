# svg_bbox.py is a python script to create a single html to calculate the SVG bounding boxes
#
# Copyright (c) 2014 Stephen E Slevinski Jr <slevin@signpuddle.net>
#
# License: MIT
#
# source material generated without magnification and with id
# >  python unpack.py svg_line.dat -i
# >  python unpack.py svg_line.dat -i -a adj_a.txt
# >  python unpack.py svg_line.dat -i -a adj_a.txt -b adj_b.txt

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
parser = argparse.ArgumentParser(description="SignWriting 2010 SVG Bounding Box script takes a directory of files and writes a single html file."
	,epilog="Source SVG and completed TTF available online https://github.com/slevinski/signwriting_2010_fonts")
parser.add_argument("directory", help="name of the sub-directory in sources for the subfont files")

args = parser.parse_args()



##################
# # initializing
##################
sourceDir = "../source/"


fontDir = sourceDir + args.directory + "/"

dataFile = "svg_bbox.html"

if os.path.exists(fontDir):
	print "input directory " + fontDir
	print "output html file " + dataFile
else:
	print "FAILURE: directory " + fontDir + " does not exist"
	sys.exit(-1)

sys.stdout = open(dataFile,'w') #redirect all prints to this log file

print '<!DOCTYPE html>';
print '<html>';
print '<head>';
print '    <title>SignWriting 2010 SVG Bounding Boxes</title>';
print '    <meta charset="utf-8">';
print '</head>';
print '<body>';
print '<div id="output"></div>';

files = glob.glob(fontDir + "*svg")
fnCalls = '';
for file in files:
	name = file.split('/')[-1].split('.')[0]
	with open(file, "rb") as image_file:
		data = image_file.read()
		print data;
		fnCalls += 'docSize("' + name + '");\n';

print '<script>';
print 'function docSize(key) {';
print '  var el=document.getElementById(key)';
print '  var b = el.getBBox();';
print '  var newP = document.createElement("p");';
print '  newP.innerHTML = key + "," + b.x + "," + b.y + "," + b.width + "," + b.height;';
print '  document.getElementById("output").appendChild(newP);';
print '}';
print fnCalls;
print '</script>';
print '</body></html>';
