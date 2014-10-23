# adj.py is a python script that takes a symbol adjustment file and rewrites part of the symbol adjustment bbox data
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

# Key, left, top, width, height
# S10001,0.0390625,0.1015625,20.60546875,29.20703125
infile = "symadj_bbox.txt"

# Key with size {correct} is reporting {error}
# S1710d with size 520x516 is reporting 521x516
adjfile = "symadj_file.txt"

lines = [line.strip() for line in open(adjfile)]
sizesAdj = {}
for line in lines:
	parts = line.split(' ')
	key = parts[0]
	size = (parts[3]).split('x')
	off = (parts[6]).split('x')
	x = int(size[0]) - int(off[0])
	y = int(size[1]) - int(off[1])
	sizesAdj[key] = [x,y]

f = open ('adj_out.txt','w')

lines = [line.strip() for line in open(infile)]
sizesBeta = {}
for line in lines:
	parts = line.split(',')
	key = parts[0]
	x = float(parts[1])
	y = float(parts[2])
	w = float(parts[3])
	h = float(parts[4])
	if key in sizesAdj:
		w = w - (0.1) * sizesAdj[key][0]
		h = h - (0.1) * sizesAdj[key][1]
		f.write(key + ',' + str(x) + ',' + str(y) + ',' + str(w) + ',' + str(h) + '\n')
	else:
		f.write(line + '\n')
f.close
