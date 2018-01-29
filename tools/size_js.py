# size_js.py is a python script to write a javascript object of symbol key sizes
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

sys.stdout = open("symsize.js",'w') #redirect all prints to this log file
print "var symSize = {"

lines = [line.strip() for line in open("symsize.txt")]
for line in lines:
	key = line[:6]
	x = int(line[7:9])
	y = int(line[11:13])
	print key + ':"' + str(x) + 'x' + str(y) + '",'

print "}"
