The SignWriting 2010 Tools
=====================
- - - 
> Version 1.5  
September 17th, 2015

The SignWriting 2010 Tools are used to build the fonts of the SignWriting 2010 typeface.  The [SignWriting 2010 Fonts][29] project contains the input and the output of the tools.  The fonts are designed for the [SignWriting 2010 JavaScript Library][60].

Developers
----------
To build the fonts from the sources, you need [FontForge][45] with [Python scripting][46] support.

To control the different aspect of the automated font creation, customize the files in the `source`  directory and the `tools` directory.
Newly created fonts are written to the `fonts` directory.

To create the demo pages, you need pystache for templating.  Demo pages are written to the `demo` directory.

To retrace the SVG from the command line, you will need several command line tools: Inkscape, pngtopnm, mkbitmap, and potrace.

To unpack the SVG Line and SVG Fill data files, the `unpack.py` tool can be used.

To create the SWAP symbol data file, the `repack.py` tool can be used.

- - -

Source Directory
------------------
The `source` directory is used to organize the main input of the build process.  

### SVG Files
The Scalar Vector Graphic files are converted to TrueType outlines with FontForge scripting.  

The source SVG files required to build the fonts are available from the [SignWriting 2010 Fonts][29] project.  These files were created with the SignWriting 2010 Tools by retracing the SVG Refinement using the `retrace.py` script.  To use these files, save them to the `source` directory and unzip.

* [SVG Line][55]  
* [SVG Filling][56]  

These files can be unpacked with the `unpack.py` script in the `tools` directory.  For the best import results, unpack with magnify level 10.

    > cd tools
    > python unpack.py svg_line.dat -m 10
    > python unpack.py svg_fill.dat -m 10

The SVGs of the compatibility glyphs for the character set "S1234567890abcdef" are based on [Source Sans Pro][25]
written by Paul D. Hunt and licensed under SIL Open Font License.
These files and more are available in the `other-svg` directory.

### FEA Files
The [Feature files][41] define the standard ligature substitution for the various character sets. Three different character sets can be used to access the glyphs.

[1D800..1DAAF][42]; Sutton SignWriting  
[Unicode 8][21] support without facial diacritic combining.

[FD800..FDFFF][43]; SignWriting Text  
[Private Use Area characters][26] for 2-dimensional text.

[S10000..S38b07][44]; ISWA 2010 Symbol Keys  
[Symbol keys][19] used as glyph names in the font files.

### template directory
The `templates` directory is used to organize the template input for the creation of the demo pages.
The templates are HTML with Mustache syntax.

- - -

Tools Directory
-----------------
To build individual font files, use the Python script `build.py`.   Use "-h" for help.

    > cd tools
    > python build.py -h
    
    usage: build.py [-h] [-c filename] [-d directory] [-e extension] [-f]
                    [-g filename] [-k filename] [-i version] [-l [filename]] [-m]
                    [-p] [-q] [-s] [-t fontname] [-u] [-v]
                    [{,Filling,Shadow}]

    SignWriting 2010 build script for TTF files from SVG (version 1.4.0)

    positional arguments:
      {,Filling,Shadow}     name of the subfont

    optional arguments:
      -h, --help            show this help message and exit
      -c filename, --custom filename
                            name of font customization file, default of custom.txt
      -d directory, --dir directory
                            name of the sub-directory in sources for the subfont
                            files
      -e extension, --ext extension
                            name of the file extension for import, default of svg
      -f, --force           overwrite existing font files
      -g filename, --glyph filename
                            name of glyph customization file, default of glyph.txt
      -k filename, --keys filename
                            name of symbol key file, default of symkeys.txt
      -i version, --ident version
                            version of the SignWriting 2010 Fonts, default of
                            1.1.0
      -l [filename], --log [filename]
                            write to log file
      -m, --mono            helper flag for naming, import, and functions (partial
                            support)
      -p, --preview         perform all of the actions but generating the TTF
                            output
      -q, --quick           skip creation of glyphs, characters, and feature file
                            merge
      -s, --silent          eliminates the print output
      -t fontname, --title fontname
                            prefix for the various font names and files, default
                            of SignWriting 2010
      -u, --unicode         use Unicode code points for individual glyphs
      -v, --verbose         increase output verbosity

- - -

To build all of the release font files, use the shell script `release.sh`.

    > cd tools
    > more release.sh
    
    python build.py "" -d svg_line -vf -l
    python build.py Filling -d svg_fill -vf -l

    > chmod a+x release.sh
    > ./release.sh

- - -

To create the demo pages, use the Python script `demo.py`.  Use "-h" for help.

    > cd tools
    > python demo.py -h

    usage: demo.py [-h] [-d directory] [-u | -p | -k] [-a server] [-w] [-i server]
                   [-s multiplier] [-t name]
                  [{,Filling,Mono,Mono Filling} ...]
    
    Automated creation of the SignWriting 2010 font demo pages
    
    positional arguments:
      {,Filling,Mono,Mono Filling}
                            name of the subfont
    
    optional arguments:
      -h, --help            show this help message and exit
      -d directory, --dir directory
                            name of subdirectory to write demo files, default of
                            test
      -u, --uni             use Unicode 8 for demo pages
      -p, --pua             use Unicode Private Use Area for demo pages
      -k, --key             use symbol keys for demo pages
      -a server, --asset server
                            url of SignWriting Asset Provider for SVG, default of
                            http://signbank.org/swap
      -w, --withpng         include PNG column in comparison table
      -i server, --image server
                            url of SignWriting Icon Server for PNG, default of
                            http://signbank.org/swis
      -s multiplier, --size multiplier
                            set the relative size of the glyph, default of 5
      -t name, --title name
                            title for the HTML demo pages, default of SignWriting
                            2010 Demo Pages


                        
To build the current demo pages used for development, use the shell script `demo.sh`.

    > cd tools
    > more demo.sh
    
    python demo.py "" Filling -w -u -d "unicode8"
    python demo.py "" Filling -w -p -d "unicodepua"
    python demo.py "" Filling -w -k -d "symbolkey"
    
    > chmod a+x demo.sh
    > ./demo.sh

There are 3 types of demo pages available online.

* Unicode 8 demo pages: [view online][47] or [download][48]
* Unicode Private Use Area demo pages: [view online][49] or [download][50]
* Symbol Key demo pages: [view online][51] or [download][52]

- - - 

The text file `symkeys.txt` contains a list of the 37,811 symbol keys of the ISWA 2010.

    S10000
    S10001
    S10002
    ...

- - -

The text file `symsize.txt` contains a list of the 37,811 symbol keys with their individual sizes.

    S10000515x530
    S10001521x530
    S10002530x515
    ...

- - -

The text file `custom.txt` contains a list of custom settings for the entire font.

    weight="Medium"
    copyright="SignWriting 2010 is released under the SIL Open Font License
    comment="The SignWriting 2010 font is a typeface for written sign languages
    descent=30
    ascent=0
    em=300

- - -

The text file `glyph.txt` contains a list of glyph settings to apply to each char.

    right_side_bearing=0

- - -


Reference
-----------


The character encodings used in SignWriting 2010 are defined in an Internet Draft submitted to the IETF: [draft-slevinski-signwriting-text][26].
The document is improved and resubmitted every 6 months.
The character design has been stable since January 12, 2012.
The current version of the Internet Draft is 05.
The next version is planned for November 2015.

- - -

Epilogue
----------
This is a work in progress. Feedback, bug reports, and patches are welcomed.

While I strived to keep the code clean and organized, it got away from me in the end.  The fine tuning and the symbol adjustments were not as straightforward as anticipated.  The script `unpack.py` required a series of complications, as found with the --adjust and --beta flags.  These flags and custom data files were used to update the source SVG.  Because of the new source SVG, these types of adjustments will not be needed again.  Future adjustments may be required of a different sort to address the occasional flattening of various symbols on specific browser/platform combinations.

- - -

To Do
-------
* Clean up code and restructure as needed.

Version History
------------------
* 1.5 - Sept 17th, 2015: added repack.py for SWAP symbol data file 
* 1.4.1 - June 26th, 2015: no facial diacritic combining 
* 1.4 - Nov 10th, 2014: development updates for the SignWriting 2010 JavaScript Library
* 1.3 - Oct 13th, 2014: production ready fonts
* 1.2 - Oct 6th, 2014: refactored build for simplicity, expanded demo for linking and optional PNG
* 1.1 - Oct 4th, 2014: added script to create demo pages
* 1.0 - Oct 3rd, 2014: added to readme for tools directory
* 1.0 - Oct 2nd, 2014: Initial project able to build TrueType font by importing SVG files and merging OpenType features

[1]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/fonts/SignWriting%202010%20Filling.ttf
[2]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/fonts/SignWriting%202010%20Filling.log
[3]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/fonts/SignWriting%202010%20Mono%20Filling.ttf
[4]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/fonts/SignWriting%202010%20Mono%20Filling.log
[5]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/fonts/SignWriting%202010%20Unified.ttf
[6]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/fonts/SignWriting%202010%20Unified.log
[7]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/fonts/SignWriting%202010%20Line.ttf
[8]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/fonts/SignWriting%202010%20Line.log
[9]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/fonts/SignWriting%202010%20Mono%20Unified.ttf
[10]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/fonts/SignWriting%202010%20Mono%20Unified.log
[11]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/fonts/SignWriting%202010%20Mono%20Line.ttf
[12]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/fonts/SignWriting%202010%20Mono%20Line.log
[13]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/source/svg1U.zip
[14]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/source/svg1L.zip
[15]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/source/svg1F.zip
[16]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/source/svb1U.zip
[17]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/source/svb1L.zip
[18]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/source/svb1F.zip
[19]: http://signbank.org/iswa
[20]: http://signpuddle.net/iswa
[21]: http://www.unicode.org/alloc/Pipeline.html
[22]: http://unicode-inc.blogspot.com/2014/08/new-publication-schedule-for-unicode.html
[23]: http://tools.ietf.org/html/draft-slevinski-signwriting-text
[24]: http://scripts.sil.org/OFL
[25]: https://www.google.com/fonts/specimen/Source+Sans+Pro
[26]: http://tools.ietf.org/html/draft-slevinski-signwriting-text
[27]: http://signpuddle.net/iswa/swfont_test.html
[28]: http://signpuddle.net/iswa/swfonts.html
[29]: https://github.com/Slevinski/signwriting_2010_fonts
[30]: https://github.com/Slevinski/signwriting_2010_tools
[31]: https://github.com/Slevinski/swap
[32]: https://github.com/Slevinski/swis
[33]: https://signbank.org/swap
[34]: http://swis.wmflabs.org
[35]: http://signbank.org/swis
[36]: http://signpuddle.com
[37]: https://incubator.wikimedia.org/wiki/User:Slevinski
[38]: https://incubator.wikimedia.org/wiki/User:Slevinski/SignWriting/Incubator#SignWriting_Gadget
[39]: https://incubator.wikimedia.org/wiki/Wp/ase
[40]: https://incubator.wikimedia.org/wiki/Category:Incubator:Test_wikis_of_sign_languages
[41]: http://www.adobe.com/devnet/opentype/afdko/topic_feature_file_syntax.html#5.d
[42]: https://raw.githubusercontent.com/Slevinski/signwriting_2010_tools/master/source/signwriting_2010_unicode8.fea
[43]: https://raw.githubusercontent.com/Slevinski/signwriting_2010_tools/master/source/signwriting_2010_unicode_pua.fea
[44]: https://raw.githubusercontent.com/Slevinski/signwriting_2010_tools/master/source/signwriting_2010_symbolkey.fea
[45]: http://fontforge.org/
[46]: http://fontforge.org/python.html
[47]: http://signpuddle.net/iswa/demo/unicode8
[48]: http://signpuddle.net/iswa/demo/unicode8.zip
[49]: http://signpuddle.net/iswa/demo/unicodepua
[50]: http://signpuddle.net/iswa/demo/unicodepua.zip
[51]: http://signpuddle.net/iswa/demo/symbolkey
[52]: http://signpuddle.net/iswa/demo/symbolkey.zip
[53]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/source/png_sutton.zip
[54]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/source/svg_refinement.zip
[55]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/source/svg_line.zip
[56]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/source/svg_fill.zip
[57]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/fonts/SignWriting%202010.ttf
[58]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/fonts/SignWriting%202010.log
[59]: http://codepen.io/Slevinski/pen/exnju
[60]: https://github.com/Slevinski/sw10js
[61]: https://github.com/Slevinski/signwriting_2010_fonts/raw/master/fonts/SignWriting%202010.mobileconfig
[62]: http://github.com/Slevinski/sw10js
[63]: http://www.opensource.org/licenses/mit-license.php
