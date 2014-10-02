#!/bin/sh
python build.py Unified -v -l "../fonts/SignWriting 2010 Unified.log"
python build.py Line -v -l "../fonts/SignWriting 2010 Line.log"
python build.py Filling -v -l "../fonts/SignWriting 2010 Filling.log"
python build.py Unified -vm -l "../fonts/SignWriting 2010 Mono Unified.log"
python build.py Line -vm -l "../fonts/SignWriting 2010 Mono Line.log"
python build.py Filling -vm -l "../fonts/SignWriting 2010 Mono Filling.log"

