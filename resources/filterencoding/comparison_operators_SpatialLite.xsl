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
        <xsl:if test="//*[local-name() = 'ValueReference']">
            <Statement>"<xsl:value-of select="//*[local-name() = 'ValueReference']" />" != '<xsl:value-of select="//*[local-name() = 'Literal']" />'</Statement>
        </xsl:if>
        <xsl:if test="not(//*[local-name() = 'ValueReference'])">
            <Statement>"<xsl:value-of select="//*[local-name() = 'PropertyName']" />" != '<xsl:value-of select="//*[local-name() = 'Literal']" />'</Statement>
        </xsl:if>
	</xsl:template>

	<xsl:template match="*[local-name(.)='PropertyIsLessThan']">
        <xsl:if test="//*[local-name() = 'ValueReference']">
            <Statement>"<xsl:value-of select="//*[local-name() = 'ValueReference']" />" &lt; '<xsl:value-of select="//*[local-name() = 'Literal']" />'</Statement>
        </xsl:if>
        <xsl:if test="not(//*[local-name() = 'ValueReference'])">
            <Statement>"<xsl:value-of select="//*[local-name() = 'PropertyName']" />" &lt; '<xsl:value-of select="//*[local-name() = 'Literal']" />'</Statement>
        </xsl:if>
	</xsl:template>

	<xsl:template match="*[local-name(.)='PropertyIsGreaterThan']">
        <xsl:if test="//*[local-name() = 'ValueReference']">
            <Statement>"<xsl:value-of select="//*[local-name() = 'ValueReference']" />" &gt; '<xsl:value-of select="//*[local-name() = 'Literal']" />'</Statement>
        </xsl:if>
        <xsl:if test="not(//*[local-name() = 'ValueReference'])">
            <Statement>"<xsl:value-of select="//*[local-name() = 'PropertyName']" />" &gt; '<xsl:value-of select="//*[local-name() = 'Literal']" />'</Statement>
        </xsl:if>
	</xsl:template>

	<xsl:template match="*[local-name(.)='PropertyIsLessThanOrEqualTo']">
        <xsl:if test="//*[local-name() = 'ValueReference']">
            <Statement>"<xsl:value-of select="//*[local-name() = 'ValueReference']" />" &lt;= '<xsl:value-of select="//*[local-name() = 'Literal']" />'</Statement>
        </xsl:if>
        <xsl:if test="not(//*[local-name() = 'ValueReference'])">
            <Statement>"<xsl:value-of select="//*[local-name() = 'PropertyName']" />" &lt;= '<xsl:value-of select="//*[local-name() = 'Literal']" />'</Statement>
        </xsl:if>
	</xsl:template>

	<xsl:template match="*[local-name(.)='PropertyIsGreaterThanOrEqualTo']">
        <xsl:if test="//*[local-name() = 'ValueReference']">
            <Statement>"<xsl:value-of select="//*[local-name() = 'ValueReference']" />" &gt;= '<xsl:value-of select="//*[local-name() = 'Literal']" />'</Statement>
        </xsl:if>
        <xsl:if test="not(//*[local-name() = 'ValueReference'])">
            <Statement>"<xsl:value-of select="//*[local-name() = 'PropertyName']" />" &gt;= '<xsl:value-of select="//*[local-name() = 'Literal']" />'</Statement>
        </xsl:if>
	</xsl:template>

	<xsl:template match="*[local-name(.)='PropertyIsLike']">
        <xsl:variable name="like1" select="regexp:replace(string($literal), string($wildcard), 'g', '%%')"/>
        <xsl:variable name="like2" select="regexp:replace(string($like1), string($singlechar), 'g', '_')"/>
        
        <xsl:if test="//*[local-name() = 'ValueReference']">
            <Statement>"<xsl:value-of select="//*[local-name() = 'ValueReference']" />" LIKE '<xsl:value-of select="$like2" />'</Statement>
        </xsl:if>
        <xsl:if test="not(//*[local-name() = 'ValueReference'])">
            <Statement>"<xsl:value-of select="//*[local-name() = 'PropertyName']" />" LIKE '<xsl:value-of select="$like2" />'</Statement>
        </xsl:if>
	</xsl:template>

	<xsl:template match="*[local-name(.)='PropertyIsBetween']">
        <xsl:if test="//*[local-name() = 'ValueReference']">
            <Statement>"<xsl:value-of select="//*[local-name() = 'ValueReference']" />" BETWEEN '<xsl:value-of select="//*[local-name() = 'LowerBoundary']" />' AND '<xsl:value-of select="//*[local-name() = 'UpperBoundary']" />'</Statement>
        </xsl:if>
        <xsl:if test="not(//*[local-name() = 'ValueReference'])">
            <Statement>"<xsl:value-of select="//*[local-name() = 'PropertyName']" />" BETWEEN '<xsl:value-of select="//*[local-name() = 'LowerBoundary']" />' AND '<xsl:value-of select="//*[local-name() = 'UpperBoundary']" />'</Statement>
        </xsl:if>
	</xsl:template>
	
	<xsl:template match="*[local-name(.)='PropertyIsNil']">
        <xsl:if test="//*[local-name() = 'ValueReference']">
            <Statement>"<xsl:value-of select="//*[local-name() = 'ValueReference']" />" = ''</Statement>
        </xsl:if>
        <xsl:if test="not(//*[local-name() = 'ValueReference'])">
            <Statement>"<xsl:value-of select="//*[local-name() = 'PropertyName']" />" = ''</Statement>
        </xsl:if>
	</xsl:template>

	<xsl:template match="*[local-name(.)='PropertyIsNull']">
        <xsl:if test="//*[local-name() = 'ValueReference']">
            <Statement>"<xsl:value-of select="//*[local-name() = 'ValueReference']" />" = NULL</Statement>
        </xsl:if>
        <xsl:if test="not(//*[local-name() = 'ValueReference'])">
            <Statement>"<xsl:value-of select="//*[local-name() = 'PropertyName']" />" = NULL</Statement>
        </xsl:if>
	</xsl:template>

</xsl:stylesheet>