<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
	xmlns:regexp="http://exslt.org/regular-expressions"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	
    <xsl:param name="version" />
    
	<xsl:template match="/">
		<Resources>
			<xsl:apply-templates select="//*[local-name(.) = 'ResourceId']" />, <xsl:apply-templates select="//*[local-name(.) = 'FeatureId']" />
		</Resources>
	</xsl:template>
    
	<!-- Filter Encoding 2.0.0 -->
	<xsl:template match="*[local-name(.) = 'ResourceId']"><xsl:value-of select="./@rid" />,</xsl:template>
     
	<!-- Filter Encoding 1.1.0 -->
    <xsl:template match="//*[local-name(.) = 'FeatureId']"><xsl:value-of select="./@fid" />,</xsl:template>
    
</xsl:stylesheet>
