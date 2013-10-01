<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" 
	xmlns:regexp="http://exslt.org/regular-expressions" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	
    <xsl:param name="version" />
	<xsl:param name="attributeIdName" />
	
	<xsl:template match="/">
		<Statements>
			<xsl:apply-templates></xsl:apply-templates>
		</Statements>
	</xsl:template>
	
	<!-- Filter Encoding 2.0.0 -->
	<xsl:template match="*[local-name(.)='ResourceId']">
        <Statement>"<xsl:value-of select="$attributeIdName" />" = '<xsl:value-of select="@rid" />'</Statement>
	</xsl:template>

	<!-- Filter Encoding 1.1.0 -->
	<xsl:template match="*[local-name(.)='FeatureId']">
        <Statement>"<xsl:value-of select="$attributeIdName" />" = '<xsl:value-of select="@fid" />'</Statement>
	</xsl:template>
    
	<xsl:template match="*[local-name(.)='GmlObjectId']">
        <Statement>"<xsl:value-of select="$attributeIdName" />" = '<xsl:value-of select="@*[local-name() = 'id']" />'</Statement>
	</xsl:template>

</xsl:stylesheet>