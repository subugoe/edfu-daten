#! /bin/sh
# Convert Windows EMF to usable graphics files with a crazy chain of tools.
# 2012 Sven-S. Porst, SUB Göttingen <porst@sub.uni-goettingen.de>

# Configuration
BASEPATH=/Users/ssp/SUB/edfu/emf
WINE=wine
METAFILE2EPS=$BASEPATH/metafile2eps-linux/metafile2eps.exe
PS2PDF=ps2pdf
INKSCAPE=/Applications/Graphik/Inkscape.app/Contents/Resources/bin/inkscape
XSLTPROC=xsltproc
XSLT=$BASEPATH/svg-stroke-width.xsl

# Variables
INPATH=$1
OUTPATH=$2
UUID=`uuidgen`
TMPPATH=/tmp/emf-converter-$UUID
mkdir $TMPPATH



# Step 1: EMF -> EPS
# Requires Wine and CUPS configured for this purpose.
# http://wiki.lyx.org/Windows/MetafileToEPSConverter
DOSINPATH=`winepath --windows "$INPATH"`
EPSPATH=$TMPPATH/file.eps
DOSEPSPATH=`winepath --windows "$EPSPATH"`
"$WINE" "$METAFILE2EPS" "$DOSINPATH" "$DOSEPSPATH"

# Step 2: EPS -> PDF
# Requires Ghostscript’s ps2pdf.
PDFPATH=$TMPPATH/file.pdf
"$PS2PDF" "$EPSPATH" "$PDFPATH"

# Step 3: PDF -> SVG
# Requires: Inkscape.
SVGPATH=$TMPPATH/file-temp.svg
"$INKSCAPE" --without-gui --export-plain-svg="$SVGPATH" "$PDFPATH"

# Step 4: SVG -> SVG
# Requires: libxml’s xsltproc.
# Apply XSL to set a line width which was lost in the preceding steps.
SVG2PATH=$TMPPATH/file.svg
"$XSLTPROC" "$XSLT" "$SVGPATH" > $SVG2PATH

rm "$SVGPATH"


# Step 5: SVG -> PNG
# Requires Inkscape.
PNGPATH=$TMPPATH/file.png
"$INKSCAPE" --without-gui --export-height=200 --export-area-drawing --export-png="$PNGPATH" "$SVG2PATH"


TARGETPATH=$INPATH-converted
mv "$TMPPATH" "$TARGETPATH"