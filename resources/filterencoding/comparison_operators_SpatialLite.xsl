<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" 
	xmlns:regexp="http://exslt.org/regular-expressions" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	
	<xsl:param name="operationType" />
	
	<xsl:template match="/">
		<Statements>
			<xsl:apply-templates></xsl:apply-templates>
		</Statements>
	</xsl:template>
	
	<xsl:template match="*[local-name(.)='PropertyIsEqualTo']">
        <xsl:if test="//*[local-name() = 'ValueReference']">
            <Statement>"<xsl:value-of select="//*[local-name() = 'ValueReference']" />" = '<xsl:value-of select="//*[local-name() = 'Literal']" />'</Statement>
        </xsl:if>
        <xsl:if test="not(//*[local-name() = 'ValueReference'])">
            <Statement>"<xsl:value-of select="//*[local-name() = 'PropertyName']" />" = '<xsl:value-of select="//*[local-name() = 'Literal']" />'</Statement>
        </xsl:if>
	</xsl:template>

	<xsl:template match="*[local-name(.)='PropertyIsNotEqualTo']">
	</xsl:template>

	<xsl:template match="*[local-name(.)='PropertyIsLessThan']">
	</xsl:template>

	<xsl:template match="*[local-name(.)='PropertyIsGreaterThan']">
		</xsl:choose>
	</xsl:template>

	<xsl:template match="*[local-name(.)='PropertyIsLessThanOrEqualTo']">
	</xsl:template>

	<xsl:template match="*[local-name(.)='PropertyIsGreaterThanOrEqualTo']">
	</xsl:template>

	<xsl:template match="*[local-name(.)='PropertyIsLike']">
	</xsl:template>

	<xsl:template match="*[local-name(.)='PropertyIsBetween']">
	</xsl:template>
	
	<xsl:template match="*[local-name(.)='PropertyIsNil']">
	</xsl:template>

	<xsl:template match="*[local-name(.)='PropertyIsNull']">
	</xsl:template>

</xsl:stylesheet>