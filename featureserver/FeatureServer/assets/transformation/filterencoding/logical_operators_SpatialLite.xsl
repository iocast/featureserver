<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" 
	xmlns:regexp="http://exslt.org/regular-expressions" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	
    <xsl:param name="version" />
	
	<xsl:template match="/">
		<Statements>
			<xsl:apply-templates></xsl:apply-templates>
		</Statements>
	</xsl:template>
	
	<xsl:template match="*[local-name(.)='And']">
        <Statement>
            <xsl:call-template name="operators">
                <xsl:with-param name="sign"> AND </xsl:with-param>
            </xsl:call-template>
        </Statement>
	</xsl:template>
	
	<xsl:template match="*[local-name(.)='Or']">
        <Statement>
            <xsl:call-template name="operators">
                <xsl:with-param name="sign"> OR </xsl:with-param>
            </xsl:call-template>
        </Statement>
	</xsl:template>
	
	<xsl:template match="*[local-name(.)='Not']">
        <Statement> NOT <xsl:value-of select="//Operator"/></Statement>
	</xsl:template>
	
	<xsl:template name="operators">
		<xsl:param name="sign" />
		(<xsl:for-each select="Operator"><xsl:value-of select="."/><xsl:if test="position() &lt; count(//Operator)"><xsl:value-of select="$sign" /></xsl:if></xsl:for-each>)
	</xsl:template>

</xsl:stylesheet>