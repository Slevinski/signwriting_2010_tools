# demo.py is a python script to create the demo pages that use the SignWriting 2010 fonts.
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
import os
import math
import argparse
import time
import pystache
from pystache import Renderer
import codecs

start = time.time()

##################
# Argument Setup
##################
parser = argparse.ArgumentParser(description="Automated creation of the SignWriting 2010 font demo pages"
	,epilog="Source SVG and completed TTF available online\nhttps://github.com/slevinski/signwriting_2010_fonts")
parser.add_argument("subfont",nargs='*',choices=['', 'Filling', 'Mono','Mono Filling'], help="name of the subfont")
parser.add_argument("-d","--dir", metavar="directory", default="test", help="name of subdirectory to write demo files, default of %(default)s")
group = parser.add_mutually_exclusive_group()
group.add_argument("-u","--uni", help="use Unicode 8 for demo pages", action="store_true")
group.add_argument("-p","--pua", help="use Unicode Private Use Area for demo pages", action="store_true")
group.add_argument("-k","--key", help="use symbol keys for demo pages", action="store_true")
parser.add_argument("-a","--asset", metavar="server", default="http://signbank.org/swap", help="url of SignWriting Asset Provider for SVG, default of %(default)s")
parser.add_argument("-w","--withpng", help="include PNG column in comparison table", action="store_true")
parser.add_argument("-i","--image", metavar="server", default="http://signbank.org/swis", help="url of SignWriting Icon Server for PNG, default of %(default)s")
parser.add_argument("-s","--size", metavar="multiplier", type=int, default=5, help="set the relative size of the glyph, default of %(default)s")
parser.add_argument("-t","--title", metavar="name", default="SignWriting 2010 Demo Pages", help="title for the HTML demo pages, default of %(default)s")
args = parser.parse_args()

#####################
# Unicode functions
#####################

def unichar(uni):
	code = int(uni,16)
	try:
		return unichr(code)
	except ValueError:
		return unichr( 0xd800 + ((code-0x10000)//0x400) ) \
			+unichr( 0xdc00 + ((code-0x10000)% 0x400) )

def key2uni(key):
    uni = unichar(base2uni(key[1:4]))
    fill = fill2uni(key[4:5])
    if fill:
    	uni = uni + unichar(fill)
    rota = rota2uni(key[5:6])
    if rota:
    	uni = uni + unichar(rota)
    return uni

def base2uni(base):
	suffix = int(base,16) + int('700',16);
	return "1D" + hex(suffix)[2:].upper()

def fill2uni(fill):
	if fill != "0":
		suffix = int(fill,16) + int('A',16)
		return "1DA9" + hex(suffix)[2:].upper()
	else:
		return ""

def rota2uni(rota):
	if rota != "0":
		suffix = int(rota,16)
		return "1DAA" + hex(suffix)[2:].upper()
	else:
		return ""

def base2pua(base):
	suffix = int(base,16) + int('730',16);
	return "FD" + hex(suffix)[2:].upper()


def fill2pua(fill):
	suffix = int(fill,16)
	return "FD81" + hex(suffix)[2:].upper()

def rota2pua(rota):
	suffix = int(rota,16)
	return "FD82" + hex(suffix)[2:].upper()

def key2pua(key):
	pua = unichar(base2pua(key[1:4]))
	pua = pua + unichar(fill2pua(key[4:5]))
	pua = pua + unichar(rota2pua(key[5:6]))
	return pua

##############
# other defs
##############
def fontAbbr(font):
	abbr = "sw2010_"
	parts = font.split()
	for part in parts:
		abbr = abbr + part[0].lower() + "_"
	return abbr + "sym"

def fontName(font):
	if font:
		return "SignWriting 2010 " + font
	else:
		return "SignWriting 2010"

def firstNav(base):
	return {"url":"S100.html","display":"<<"}

def prevNav(base):
	if  base=="S100":
		return {"url":"S100.html","display":"<"}
	else:
		return {"url":"S" + hex(int(base[1:],16)-1)[2:] + ".html","display":"<"}

def nextNav(base):
	if  base=="S38b":
		return {"url":"S38b.html","display":">"}
	else:
		return {"url":"S" + hex(int(base[1:],16)+1)[2:] + ".html","display":">"}

def lastNav(base):
	return {"url":"S38b.html","display":">>"}

def createDir(dir):
	if not os.path.isdir(dir):
		os.makedirs(dir)
		print "creating output in directory '" + dir + "'"
	else:
		print "directory already exists"
		print "remove '" + dir + "' or use -d for a different dir"
#		sys.exit(1);
		

##################
# # initializing
##################
templateDir = "../source/templates/"
demoDir = "../demo/" + args.dir + "/"

fonts = []
for font in args.subfont:
	fonts.append({"abbr":fontAbbr(font),"name":fontName(font),"font":font})

headTpl = open(templateDir + "head.html").read()
indexTpl = open(templateDir + "index.html").read()
navTpl = open(templateDir + "nav.html").read()
tableTpl = open(templateDir + "table.html").read()
footTpl = open(templateDir + "foot.html").read()

renderer = Renderer()

createDir(demoDir)
print "READY"

#index
htmlFile = demoDir + "index.html"

infile = open("symkeys.txt", "r")
current = ''
bases = []
for symkey in infile:
	prefix = symkey[0:4]
	if prefix != current:
		bases.append({"base":prefix})
	current = prefix

content = {"title":"Symbol index of " + args.dir,
	"fonts":fonts,
	"fontsize": args.size*180,
	"size": args.size,
	"bases": bases
}

headHtml = renderer.render(headTpl, content)
indexHtml = renderer.render(indexTpl, content)
html = headHtml + indexHtml + footTpl
output_file = codecs.open(htmlFile, "w", 
   	                      encoding="utf-8", 
       	                  errors="xmlcharrefreplace"
)
output_file.write(html)

# base files
infile = open("symkeys.txt", "r")
current = ''
allrows = []
rows = []
for symkey in infile:
	symkey=symkey[:-1]
	prefix = symkey[0:4]
	if prefix != current:
		if len(rows):
			allrows.append(rows)
		rows=[]
	current = symkey[0:4]
	if args.uni:
		text = key2uni(symkey)
	if args.pua:
		text = key2pua(symkey)
	if args.key:
		text = symkey
	rows.append({"key":symkey,"text":text})
allrows.append(rows)

for rows in allrows:

	current = rows[0]["key"][0:4]
	htmlFile = demoDir + current + ".html"
	navs = []
	navs.append(firstNav(current))
	navs.append(prevNav(current))
	navs.append(nextNav(current))
	navs.append(lastNav(current))

	content = {"title":"Symbol set " + current,
		"fonts":fonts,
		"fontsize": args.size*180,
		"size": args.size,
		"with": args.withpng,
		"image": args.image,
		"asset": args.asset,
		"navs": navs,
		"rows": rows
	}

	headHtml = renderer.render(headTpl, content)
	navHtml = renderer.render(navTpl, content)
	tableHtml = renderer.render(tableTpl, content)
	html = headHtml + navHtml + tableHtml + footTpl
	output_file = codecs.open(htmlFile, "w", 
    	                      encoding="utf-8", 
        	                  errors="xmlcharrefreplace"
	)
	output_file.write(html)

print "DONE"