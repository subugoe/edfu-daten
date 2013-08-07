<?xml version="1.0" encoding="UTF-8"?>
<!--
	Einfache METS Datei aus Chassinat Bildnamen erstellen.

	Sven-S. Porst, SUB Göttingen <porst@sub.uni-goettingen.de>
-->
<xsl:stylesheet
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:mets="http://www.loc.gov/METS/"
	xmlns:xlink="http://www.w3.org/1999/xlink"
	xmlns:mods="http://www.loc.gov/mods/v3"
	xmlns:dv="http://dfg-viewer.de/"
	version="1.0">

	<xsl:output indent="yes" method="xml" version="1.0" encoding="UTF-8"/>

	<xsl:template match="/">
		<mets:mets>
			<xsl:call-template name="dmdSec"/>
			<xsl:call-template name="amdSec"/>
			<xsl:call-template name="fileSec"/>
			<xsl:call-template name="structMap"/>
		</mets:mets>
	</xsl:template>

	<xsl:template name="dmdSec">
		<dmdSec xmlns="http://www.loc.gov/METS/">
			<xsl:attribute name="ID">
				<xsl:text>dmd-chassinat-</xsl:text>
				<xsl:value-of select="/images/volume"/>
			</xsl:attribute>
			
			<mdWrap MIMETYPE="text/xml" MDTYPE="MODS">
				<xmlData>
					<mods version="3.0" xmlns="http://www.loc.gov/mods/v3">
						<titleInfo>
							<nonSort>Le</nonSort>
							<title>temple d’Edfou</title>
							<partNumber>
								<xsl:value-of select="/images/volume"/>
							</partNumber>
						</titleInfo>
						<name>
							<family>Chassinat</family>
							<given>Émile</given>
						</name>
						<originInfo>
							<place>
								<placeTerm type="code" authority="marccountry">ua</placeTerm>
							</place>
							<place>
								<placeTerm type="text">Le Caire</placeTerm>
							</place>
							<publisher>Institut français d'archéologie orientale</publisher>
							<dateIssued>
								<xsl:choose>
									<xsl:when test="/images/volume = '5'">1930</xsl:when>
									<xsl:when test="/images/volume = '6'">1931</xsl:when>
									<xsl:when test="/images/volume = '7'">1932</xsl:when>
									<xsl:when test="/images/volume = '8'">1933</xsl:when>
								</xsl:choose>
							</dateIssued>
						</originInfo>
					</mods>
				</xmlData>
			</mdWrap>
		</dmdSec>
	</xsl:template>
	
	<xsl:template name="amdSec">
		<amdSec xmlns="http://www.loc.gov/METS/">
			<xsl:attribute name="ID">
				<xsl:text>amd-chassinat-</xsl:text>
				<xsl:value-of select="/images/volume"/>
			</xsl:attribute>
			
			<rightsMD ID="rights">
				<mdWrap MIMETYPE="text/xml" MDTYPE="OTHER" OTHERMDTYPE="DVRIGHTS">
					<xmlData>
						<dv:rights>
							<dv:owner>Edfu Projekt</dv:owner>
						</dv:rights>
					</xmlData>
				</mdWrap>
			</rightsMD>
			
			<digiprovMD ID="digiprov">
				<mdWrap MIMETYPE="text/xml" MDTYPE="OTHER" OTHERMDTYPE="DVLINKS">
					<xmlData>
						<dv:links>
							<dv:reference>http://opac.sub.uni-goettingen.de/DB=1/</dv:reference>
						</dv:links>
					</xmlData>
				</mdWrap>
			</digiprovMD>
		</amdSec>
	</xsl:template>
	
	<xsl:template name="fileSec">
		<xsl:variable name="baseURL">
			<xsl:text>http://vlib.sub.uni-goettingen.de/test/fileadmin/edfu-data/Chassinat/</xsl:text>
		</xsl:variable>
		
		<fileSec xmlns="http://www.loc.gov/METS/">
			<fileGrp USE="DEFAULT">
				<xsl:for-each select="/images/image">
					<file MIMETYPE="image/jpeg">
						<xsl:attribute name="ID">
							<xsl:text>img</xsl:text>
							<xsl:value-of select="substring-before(., '.')"/>
						</xsl:attribute>
						<FLocat LOCTYPE="URL">
							<xsl:attribute name="xlink:href">
								<xsl:value-of select="$baseURL"/>
								<xsl:value-of select="."/>
							</xsl:attribute>
						</FLocat>
					</file>
				</xsl:for-each>
			</fileGrp>
		</fileSec>
	</xsl:template>
	
	<xsl:template name="structMap">
		<structMap TYPE="LOGICAL" xmlns="http://www.loc.gov/METS/">
			<div TYPE="monograph" ID="log1">
				<xsl:attribute name="ADMID">
					<xsl:text>amd-chassinat-</xsl:text>
					<xsl:value-of select="/images/volume"/>
				</xsl:attribute>
		
				<xsl:attribute name="DMDID">
					<xsl:text>dmd-chassinat-</xsl:text>
					<xsl:value-of select="/images/volume"/>
				</xsl:attribute>
			</div>
		</structMap>

		<structMap TYPE="PHYSICAL" xmlns="http://www.loc.gov/METS/">
			<div TYPE="physSequence">
				<xsl:attribute name="ADMID">
					<xsl:text>amd-chassinat-</xsl:text>
					<xsl:value-of select="/images/volume"/>
				</xsl:attribute>
		
				<xsl:attribute name="DMDID">
					<xsl:text>dmd-chassinat-</xsl:text>
					<xsl:value-of select="/images/volume"/>
				</xsl:attribute>

				<xsl:attribute name="ID" TYPE="physSequence">
					<xsl:text>phys-chassinat-</xsl:text>
					<xsl:value-of select="/images/volume"/>
				</xsl:attribute>
							
				<xsl:for-each select="/images/image">
					<xsl:variable name="filename">
						<xsl:value-of select="substring-before(., '.')"/>
					</xsl:variable>
					<div TYPE="page">
						<xsl:attribute name="ORDER">
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="ORDERLABEL">
							<xsl:variable name="page">
								<xsl:value-of select="substring-after($filename, '_')"/>
							</xsl:variable>
							<xsl:variable name="page2">
								<xsl:choose>
									<xsl:when test="substring($page, 1, 3) = '000'">
										<xsl:value-of select="translate(
											substring($page, 4),
											'abcdefghijklmn',
											'ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫXX')"/>
										<xsl:if test="substring($page, 4) = 'm'">III</xsl:if>
										<xsl:if test="substring($page, 4) = 'n'">IV</xsl:if>
									</xsl:when>
									<xsl:when test="substring($page, 1, 2) = '00'">
										<xsl:value-of select="substring($page, 3)"/>
									</xsl:when>
									<xsl:when test="substring($page, 1, 1) = '0'">
										<xsl:value-of select="substring($page, 2)"/>
									</xsl:when>
									<xsl:otherwise>
										<xsl:value-of select="$page"/>
									</xsl:otherwise>
								</xsl:choose>
							</xsl:variable>
							<xsl:value-of select="$page2"/>
						</xsl:attribute>
						<xsl:attribute name="ID">
							<xsl:text>div-</xsl:text>
							<xsl:value-of select="$filename"/>
						</xsl:attribute>
						<fptr>
							<xsl:attribute name="FILEID">
								<xsl:text>img</xsl:text>
								<xsl:value-of select="$filename"/>
							</xsl:attribute>
						</fptr>
					</div>
				</xsl:for-each>
			</div>
		</structMap>
	</xsl:template>

</xsl:stylesheet>

