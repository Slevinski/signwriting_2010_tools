# adj.py is a python script that takes a symbol adjustment file and rewrites part of the symbol adjustment bbox data
#
# Copyright (c) 2014 Stephen E Slevinski Jr <slevin@signpuddle.net>
#
# License: MIT


# Key, left, top, width, height
# S10001,0.0390625,0.1015625,20.60546875,29.20703125
infile = "symadj_bbox.txt"


# Key with size {correct} is reporting {error}
# 0 3 6
# S1710d with size 520x516 is reporting 521x516
# or
# 0 2 1
# key {error} {correct}
adjfile = "symadj_file.txt"

lines = [line.strip() for line in open(adjfile)]
sizesAdj = {}
for line in lines:
	parts = line.split(' ')
	key = parts[0]
	size = (parts[2]).split('x')
	off = (parts[1]).split('x')
	x = int(size[0]) - int(off[0])
	y = int(size[1]) - int(off[1])
	sizesAdj[key] = [x,y]

f = open('adj_out.txt','w')

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
