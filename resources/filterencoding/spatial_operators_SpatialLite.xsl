<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
	xmlns:gml="http://www.opengis.net/gml"
	xmlns:regexp="http://exslt.org/regular-expressions" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	
	<xsl:param name="operationType" />
	<xsl:param name="geometryName" />
	<xsl:param name="srs" />
	
	<xsl:template match="/">
		<Statements>
			<xsl:apply-templates>
				<xsl:with-param name="geometryName" select="$geometryName" />
				<xsl:with-param name="srs" select="$srs" />
			</xsl:apply-templates>
		</Statements>
	</xsl:template>

	<xsl:template match="*[local-name(.)='Equals']">
		<xsl:param name="geometryName" />
		<xsl:param name="srs" />
	</xsl:template>
	
	<xsl:template match="*[local-name(.)='Disjoint']">
		<xsl:param name="geometryName" />
		<xsl:param name="srs" />
    </xsl:template>

	<xsl:template match="*[local-name(.)='Touches']">
		<xsl:param name="geometryName" />
		<xsl:param name="srs" />
	</xsl:template>

	<xsl:template match="*[local-name(.)='Within']">
		<xsl:param name="geometryName" />
		<xsl:param name="srs" />
	</xsl:template>

	<xsl:template match="*[local-name(.)='Overlaps']">
		<xsl:param name="geometryName" />
		<xsl:param name="srs" />
	</xsl:template>

	<xsl:template match="*[local-name(.)='Crosses']">
		<xsl:param name="geometryName" />
		<xsl:param name="srs" />
	</xsl:template>

	<xsl:template match="*[local-name(.)='Intersects']">
		<xsl:param name="geometryName" />
		<xsl:param name="srs" />
	</xsl:template>

	<xsl:template match="*[local-name(.)='Contains']">
		<xsl:param name="geometryName" />
		<xsl:param name="srs" />
	</xsl:template>

	<xsl:template match="*[local-name(.)='DWithin']">
		<xsl:param name="geometryName" />
		<xsl:param name="srs" />
	</xsl:template>

	<xsl:template match="*[local-name(.)='Beyond']">
		<xsl:param name="geometryName" />
		<xsl:param name="srs" />
	</xsl:template>

	<xsl:template match="*[local-name(.)='BBOX']">
		<xsl:param name="geometryName" />
		<xsl:param name="srs" />
		
		<xsl:variable name="lower" select="//*[local-name() = 'Envelope']/*[local-name() = 'lowerCorner']"/>
		<xsl:variable name="upper" select="//*[local-name() = 'Envelope']/*[local-name() = 'upperCorner']"/>
		<xsl:variable name="srsName" select="//*[local-name() = 'Envelope']/@srsName"/>
		 
		<xsl:variable name="geometry" select="$geometryName"/>
							 
        <xsl:variable name="lower1" select="regexp:replace(string($lower), string(' '), 'g', ',')"/>
        <xsl:variable name="upper1" select="regexp:replace(string($upper), string(' '), 'g', ',')"/>
        <xsl:variable name="srs1" select="regexp:replace(string($srsName), '.*:(?!.*:)', 'g', '')"/>
		
		<Statement>Intersects(Transform(BuildMBR(<xsl:value-of select="$lower1" />,<xsl:value-of select="$upper1"/>, <xsl:value-of select="$srs1"/>), <xsl:value-of select="$srs" />), <xsl:value-of select="$geometry" />)</Statement>		
	</xsl:template>

</xsl:stylesheet>