The SignWriting 2010 Tools
=====================
- - - 
> Version 1.0  
October 2nd, 2014

The SignWriting 2010 Tools are used to build a typeface for written sign languages
called the [SignWriting 2010 Fonts][29].

Developers
----------
To build the fonts from the sources, you need [FontForge][45] with [Python scripting][46] support.

To control the different aspect of the automated font creation, customize the files in the `source`  directory and the `tools` directory.  Newly created fonts are written to the `fonts` directory.

- - -

### source directory
The `source` directory is used to organize the main input of the build process.  

#### SVG Files
Scalar Vector Graphic files are converted to TrueType outlines with FontForge scripting.

The source SVG files required to build the fonts are available from the [SignWriting 2010 Fonts][29] project.

The SVGs of the compatibility glyphs for the character set "S1234567890abcdef" are based on [Source Sans Pro][25]
written by Paul D. Hunt and licensed under SIL Open Font License.
These files and more are available in the `other-svg` directory.

#### FEA Files
The [Feature files][41] define the standard ligature substitution for the various character sets. Three different character sets can be used to access the glyphs.

[1D800..1DAAF][42]; Sutton SignWriting  
To be published in [Unicode 8][21] in [2015][22].

[FD800..FDFFF][43]; SignWriting Text  
[Private Use Area characters][26] for 2-dimensional text.

[S10000..S38b07][44]; ISWA 2010 Symbol Keys  
[Symbol keys][19] used as glyph names in the font files.

- - -

###tools directory
To build individual font files, use the Python script `build.py`.   Use "-h" for help

    cd tools
    python build.py -h

To build all of the release font files, use the shell script `release.sh`.

    cd tools
    chmod a+x release.sh
    ./release.sh

- - - 

The text file `symkeys.txt` contains a list of the 37,811 symbol keys of the ISWA 2010.

    S10000
    S10001
    S10002
    ...

- - -

The text file `custom.txt` contains a list of custom settings for the entire font.

    weight="Medium"
    copyright="SignWriting 2010 is released under the SIL Open Font License
    comment="The SignWriting 2010 font is a typeface for written sign languages
    descent=15
    ascent=15
    em=30

- - -

The text file `glyph.txt` contains a list of glyph settings to appy to each char.

    left_side_bearing=5
    right_side_bearing=5
    removeOverlap
    autoInstr

- - -

Text files like `svg#ref.txt` contain a cross reference file from symbol key to subfont, such as Unified, Line, or Other.  The symbol key can be generalized or exact, such as *S100* or *S1000* or *S10000*.  This file is used to create the main SignWriting 2010 font, where some glyphs come from the Unified font, some from the Line font, and others require a new glyph.

    S100 U
    S101 u
    S102 Ou
    S103 L
    S104 l
    S105 Ol
    S1060 U
    S10610 u
    ...

Cross Reference for subfont

* U  - Unified subfont
* u - Unified subfont is imperfect
* Ou - Other subfont desired, otherwise use the Unified subfont
* L - Line subfont
* l - Line subfont is imperfect
* Ol - Other subfont desired, otherwise use the Line subfont

- - -


Reference
-----------


The character encodings used in SignWriting 2010 are defined in an Internet Draft submitted to the IETF: [draft-slevinski-signwriting-text][26].
The document is improved and resubmitted every 6 months.
The character design has been stable since January 12, 2012.
The current version of the Internet Draft is 03.
The next version is planned for November 2014.

- - -

Epilogue
----------
This is a work in progress. Feedback, bug reports, and patches are welcomed.

- - -

To Do
-------
* Customize the data files and build scripts as required to improve fonts
* Create demo script that creates test pages for the newly created fonts
* Create main SignWriting 2010 font file
  * index symbol glyphs in file `svg1ref.txt` as Unified, Line, or Other 
  * create new source SVG called `SVG1 Other Glyphs`
  * update build.py to create main font file


Version History
------------------
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
