# dump.py is a python script to write a javascript object
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

sys.stdout = open("test.size.js",'w') #redirect all prints to this log file
print "var assert = chai.assert;"

max = 38;
count = max;
item = 1;
lines = [line.strip() for line in open("symsize.txt")]
for line in lines:
	key = line[:6]
	x = int(line[7:9])
	y = int(line[11:13])
	if count==max:
		if item>1:
			print '    });'
			print '  });'
		print "  suite('test " + str(item) + "', function(){"
		print "    this.timeout(5000);"
		print "    test('starting key " + key + "', function(){"
		count = 0
		item += 1
	count += 1
	print "      assert.equal(ssw.size('" + key + "'),'" + str(x) + 'x' + str(y) + "','" + key + "');"

print '    });'
print '  });'
