#!/bin/sh
#python build.py "" -d svg_line -vf -u 4 -l (deprecated)
python build.py Line -d svg_line -vf -u F -l
python build.py Fill -d svg_fill -vf -u 10 -l
python build.py "8" -d svg_line -vfa -u F -c custom8.txt -l
python build.py "1dOpt" -d svg_line -vfb -u 4 -c custom1D.txt -g glyph1D.txt -l
python build.py "1d" -d svg_line -vfax -u F -c custom1D.txt -g glyph1D.txt -l

