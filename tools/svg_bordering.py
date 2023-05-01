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
import argparse

##################
# Argument Setup
##################
parser = argparse.ArgumentParser(description="SignWriting 2010 SVG Bounding Box script takes a directory of files and writes a single html file."
	,epilog="Source SVG and completed TTF available online https://github.com/slevinski/signwriting_2010_fonts")
parser.add_argument("file", help="name of the file with the bbox adjustments")

args = parser.parse_args()



##################
# # initializing
##################
dataFile = "svg_bordering.html"
restore = sys.stdout
sys.stdout = open(dataFile,'w') #redirect all prints to this log file

print('<!DOCTYPE html>')
print('<html>')
print('<head>')
print('    <title>SignWriting 2010 SVG Bounding Boxes</title>')
print('    <meta charset="utf-8">')
print('    <script src="svg_bordering.js"></script>')
print('</head>')
print('<body>')
print('<div id="output"></div>')


top = 'S2ff00 S2ff01 S2ff02 S2ff03 S2ff20 S2ff31 S2ff33'
left = ''

zero = 0
other = 0
lines = [line.strip() for line in open(args.file)]
fnCalls = ''
for line in lines:
	parts = line.split(' ')
	key = parts[0]
	xMin = float(parts[1])
	xMax = float(parts[2])
	yMin = float(parts[3])
	yMax = float(parts[4])
	if xMin == 0 and yMin == 0 and parts[2][-1] and parts[4][-1]:
		zero += 1
	else:
		if yMin == 0: # or yMin == 2:
#		if yMin == 1:
#		if key[0:4] == 'S2ff':
#		if key in top:
#		if key in left:
			other += 1
			print("<h2>" + key + "</h2>")
			print("<p>" + str(xMin).rstrip('0').rstrip('.') + ', ' + str(yMin).rstrip('0').rstrip('.'))
			print('<p><canvas id="' + key + '" width="' + str(150 + xMax) + '" height="' + str(150 + yMax) + '"></canvas>')
			fnCalls += 'drawGrid("' + key + '");\n'

print('<script>')
print(fnCalls)
print('</script>')
print('</body></html>')

sys.stdout = restore
print(f'Output {str(other)} signs for inspection')
