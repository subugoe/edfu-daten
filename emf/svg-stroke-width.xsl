<?xml version="1.0" encoding="UTF-8"?>
<!--
	Remove styles from SVG file and add a stroke width to its path.

	2012 Sven-S. Porst, SUB Göttingen <porst@sub.uni-goettingen.de>
-->
<xsl:stylesheet
	version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:svg="http://www.w3.org/2000/svg"
	xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape">

	<xsl:output indent="yes" method="xml" version="1.0" encoding="UTF-8"/>


	<xsl:template match="@*|node()">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()"/>
		</xsl:copy>
	</xsl:template>
	
	
	<xsl:template match="@style">
		<xsl:attribute name="style">
		<xsl:text>stroke:#000000;stroke-width:8;stroke-miterlimit:4;stroke-dasharray:none;fill:none;stroke-opacity:1</xsl:text>
		</xsl:attribute>
	</xsl:template>

</xsl:stylesheet>
