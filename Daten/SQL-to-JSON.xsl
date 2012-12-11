<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
	version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:json="http://json.org/">

	<xsl:output indent="yes" method="text" version="1.0" encoding="UTF-8"/>


	<xsl:template match="resultset">
		<xsl:text>{"docs":[</xsl:text>
			<xsl:apply-templates select="row"/>
		<xsl:text>]}</xsl:text>
	</xsl:template>

	<xsl:template match="row">
		<xsl:text>{&#x0A;</xsl:text>
			<xsl:apply-templates select="field"/>
		<xsl:text>},&#x0A;</xsl:text>
	</xsl:template>

	<xsl:template match="field">
		<xsl:text>&#x09;"</xsl:text>
		<xsl:call-template name="encode-value">
			<xsl:with-param name="value" select="@name"/>
		</xsl:call-template>
		<xsl:text>":"</xsl:text>
		<xsl:call-template name="encode-value">
			<xsl:with-param name="value" select="."/>
		</xsl:call-template>
		<xsl:text>",&#x0A;</xsl:text>
	</xsl:template>


	<xsl:template name="escapeQuotes">
		<xsl:param name="text"/>
		<xsl:variable name="firstChar" select="substring($text, 1, 1)"/>
		<xsl:variable name="remainder" select="substring($text, 2)"/>

		<xsl:if test="$firstChar = '&#x22;'">
			<xsl:text>\</xsl:text>
		</xsl:if>
		<xsl:value-of select="firstChar"/>

		<xsl:call-template name="escapeQuotes">
			<xsl:with-param name="string" select="$remainder"/>
		</xsl:call-template>
	</xsl:template>



	<!--
		Escaping templates taken from xml-to-json.xsl.
		http://www.bramstein.com/projects/xsltjson/conf/xml-to-jsonml.xsl
	-->


	<json:search name="string">
		<json:replace src="\" dst="\\"/>
		<json:replace src="&quot;" dst="\&quot;"/>
		<json:replace src="&#xA;" dst="\n"/>
		<json:replace src="&#xD;" dst="\r"/>
		<json:replace src="&#x9;" dst="\t"/>
		<json:replace src="\n" dst="\n"/>
		<json:replace src="\r" dst="\r"/>
		<json:replace src="\t" dst="\t"/>
	</json:search>


	<xsl:template name="encode">
		<xsl:param name="input"/>
		<xsl:param name="index">1</xsl:param>
		<xsl:variable name="text">
			<xsl:call-template name="replace-string">
				<xsl:with-param name="input" select="$input"/>
				<xsl:with-param name="src" select="document('')//json:search/json:replace[$index]/@src"/>
				<xsl:with-param name="dst" select="document('')//json:search/json:replace[$index]/@dst"/>
			</xsl:call-template>
		</xsl:variable>

		<xsl:choose>
			<xsl:when test="$index &lt; count(document('')//json:search/json:replace)">
				<xsl:call-template name="encode">
					<xsl:with-param name="input" select="$text"/>
					<xsl:with-param name="index" select="$index + 1"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$text"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template name="replace-string">
		<xsl:param name="input"/>
		<xsl:param name="src"/>
		<xsl:param name="dst"/>

		<xsl:choose>
			<xsl:when test="contains($input, $src)">
				<xsl:value-of select="concat(substring-before($input, $src), $dst)"/>
				<xsl:call-template name="replace-string">
					<xsl:with-param name="input" select="substring-after($input, $src)"/>
					<xsl:with-param name="src" select="$src"/>
					<xsl:with-param name="dst" select="$dst"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$input"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template name="encode-value">
		<xsl:param name="value"/>

		<xsl:choose>
			<xsl:when test="(normalize-space($value) != $value 
								or string(number($value)) = 'NaN'
								or (substring($value , string-length($value), 1) = '.')
								or (substring($value, 1, 1) = '0')
								and not($value = '0'))
							 and not($value = 'false')
							 and not($value = 'true')
							 and not($value = 'null')">
				<xsl:text>"</xsl:text>
				<xsl:call-template name="encode">
				<xsl:with-param name="input" select="$value"/>
				</xsl:call-template>
				<xsl:text>"</xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$value"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

</xsl:stylesheet>