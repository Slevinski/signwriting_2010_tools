#!/bin/sh
python build.py Line -d svg1L -v -l
python build.py Filling -d svg1F -v -l
python build.py Shadow -d svg1U -v -l
python build.py Line -d svb1L -vm -l
python build.py Filling -d svb1F -vm -l
python build.py Shadow -d svb1U -vm -l

