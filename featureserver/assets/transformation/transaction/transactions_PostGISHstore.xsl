<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
	xmlns:regexp="http://exslt.org/regular-expressions"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	
    <xsl:param name="version" />
	<xsl:param name="transactionType" />
	<xsl:param name="geometryAttribute" />
	<xsl:param name="geometryData" />
	<xsl:param name="tableName" />
	
	<xsl:template match="/">
		<Statements>
            <xsl:choose>
                <xsl:when test="$transactionType='insert'">
                    <xsl:call-template name="Insert">
                        <xsl:with-param name="version" select="$version" />
                        <xsl:with-param name="geometryAttribute" select="$geometryAttribute" />
                        <xsl:with-param name="geometryData" select="$geometryData" />
                        <xsl:with-param name="tableName" select="$tableName" />
                    </xsl:call-template>
                </xsl:when>
                <xsl:when test="$transactionType='update'">
                    <xsl:call-template name="Update">
                        <xsl:with-param name="version" select="$version" />
                        <xsl:with-param name="geometryAttribute" select="$geometryAttribute" />
                        <xsl:with-param name="geometryData" select="$geometryData" />
                        <xsl:with-param name="tableName" select="$tableName" />
                    </xsl:call-template>
                </xsl:when>
                <xsl:when test="$transactionType='delete'">
                    <xsl:call-template name="Delete">
                        <xsl:with-param name="version" select="$version" />
                        <xsl:with-param name="tableName" select="$tableName" />
                    </xsl:call-template>
                </xsl:when>
            </xsl:choose>
		</Statements>
	</xsl:template>
	
	<xsl:template name="Insert">
		<xsl:param name="version"/>
		<xsl:param name="geometryAttribute"/>
		<xsl:param name="geometryData"/>
		<xsl:param name="tableName"/>
        
        <Statement>
            INSERT INTO <xsl:value-of select="$tableName"/> (
            <xsl:for-each select="child::*">
                <xsl:variable name="total" select="count(child::*)" />
                <xsl:for-each select="child::*">
                    "<xsl:value-of select="local-name(.)"/>"
                    <xsl:if test="position() &lt; $total">,</xsl:if>
                </xsl:for-each>
            </xsl:for-each>
            ) VALUES (
            <xsl:for-each select="child::*">
                <xsl:variable name="total" select="count(child::*)" />
                <xsl:for-each select="child::*">
                    <xsl:choose>
                        <xsl:when test="local-name(.)=$geometryAttribute">
                            ST_GeomFromGML('<xsl:value-of select="string($geometryData)" />')
                        </xsl:when>
                        <xsl:otherwise>
                            '<xsl:value-of select="."/>'
                        </xsl:otherwise>
                    </xsl:choose>
                    <xsl:if test="position() &lt; $total">,</xsl:if>
                </xsl:for-each>
            </xsl:for-each>
            );
        </Statement>
	</xsl:template>
	
	<xsl:template name="Update">
		<xsl:param name="version"/>
		<xsl:param name="geometryAttribute"/>
		<xsl:param name="geometryData"/>
		<xsl:param name="tableName"/>
        
        <Statement>
            UPDATE <xsl:value-of select="$tableName"/> SET
            <xsl:for-each select="child::*">
                <xsl:variable name="total" select="count(//*[local-name()='Property'])" />
                <xsl:choose>
                    <xsl:when test="$version = '2.0.0'">
                        <xsl:for-each select="//*[local-name()='Property']/*[local-name()='ValueReference']">
                            <xsl:choose>
                                <xsl:when test=".=$geometryAttribute and string-length($geometryData) > 0">
                                    "<xsl:value-of select="."/>" = ST_GeomFromGML('<xsl:value-of select="string($geometryData)" />')
                                </xsl:when>
                                <xsl:otherwise>
                                    "<xsl:value-of select="."/>" = '<xsl:value-of select="./following-sibling::*[1]"/>'
                                </xsl:otherwise>
                            </xsl:choose>
                            <xsl:if test="position() &lt; $total">,</xsl:if>
                        </xsl:for-each>
                    </xsl:when>
                    <xsl:when test="$version = '1.1.0'">
                        <xsl:for-each select="//*[local-name()='Property']/*[local-name()='Name']">
                            <xsl:choose>
                                <xsl:when test=".=$geometryAttribute and string-length($geometryData) > 0">
                                    "<xsl:value-of select="."/>" = ST_GeomFromGML('<xsl:value-of select="string($geometryData)" />')
                                </xsl:when>
                                <xsl:otherwise>
                                    "<xsl:value-of select="."/>" = '<xsl:value-of select="./following-sibling::*[1]"/>'
                                </xsl:otherwise>
                            </xsl:choose>
                            <xsl:if test="position() &lt; $total">,</xsl:if>
                        </xsl:for-each>
                    </xsl:when>
                </xsl:choose>
                
            </xsl:for-each>
            <xsl:if test="//*[local-name() = 'Filter']">
                WHERE
            </xsl:if>
        </Statement>
    </xsl:template>
    
    <xsl:template name="Delete">
        <xsl:param name="version"/>
        <xsl:param name="tableName"/>
        
        <xsl:variable name="total">
            <xsl:choose>
                <xsl:when test="$version = '2.0.0'">
                    <xsl:value-of select="count(//*[local-name()='ResourceId'])" />
                </xsl:when>
                <xsl:when test="$version = '1.1.0'">
                    <xsl:value-of select="count(//*[local-name()='FeatureId'])" />
                </xsl:when>
            </xsl:choose>
        </xsl:variable>
        
        <Statement>
            DELETE FROM <xsl:value-of select="$tableName"/>
            <xsl:if test="//*[local-name() = 'Filter']">
                WHERE
            </xsl:if>
        </Statement>
    </xsl:template>
    
</xsl:stylesheet>