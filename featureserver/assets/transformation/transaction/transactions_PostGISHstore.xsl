<xsl:stylesheet version="1.0"
	xmlns:regexp="http://exslt.org/regular-expressions"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:wfs="http://www.opengis.net/wfs"
    xmlns:fs="http://featureserver.org">
	
	<xsl:output method = "xml" indent = "yes" />
	
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
                    </xsl:call-template>
                </xsl:when>
                <xsl:when test="$transactionType='update'">
                    <xsl:call-template name="Update">
                    </xsl:call-template>
                </xsl:when>
                <xsl:when test="$transactionType='delete'">
                    <xsl:call-template name="Delete">
                    </xsl:call-template>
                </xsl:when>
            </xsl:choose>
		</Statements>
	</xsl:template>
	
	
	
	<xsl:template name="Delete">
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
	
	
	
	<xsl:template name="Insert">
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
	
	
	<xsl:key name="update-by-hstore-1.1.0" match="./*[local-name()='Property']" use="./*[local-name()='Name']"/>
	<xsl:key name="update-by-hstore-2.0.0" match="./*[local-name()='Property']" use="./*[local-name()='ValueReference']" />
	<xsl:template name="Update">
		<xsl:for-each select="child::*">
			
			<Statement>
				<xsl:choose>
					<xsl:when test="$version='1.1.0'">
						UPDATE <xsl:value-of select="$tableName"/> SET
						<xsl:variable name="total-groups" select="count(./*[local-name()='Property'][generate-id() = generate-id(key('update-by-hstore-1.1.0', ./*[local-name()='Name'])[1])])" />
						
						<xsl:for-each select="./*[local-name()='Property'][count(. | key('update-by-hstore-1.1.0', ./*[local-name()='Name'])[1]) = 1]">
							<xsl:sort select="./*[local-name()='Name']" />
							<xsl:variable name="total-in-group" select="count(key('update-by-hstore-1.1.0', ./*[local-name()='Name']))" />
							
							<xsl:variable name="name" select="./*[local-name()='Name']" />
							
							<xsl:choose>
								
								<xsl:when test="$name=$geometryAttribute and string-length($geometryData) > 0">
									"<xsl:value-of select="$name"/>" = ST_GeomFromGML('<xsl:value-of select="string($geometryData)" />')
								</xsl:when>
								
								
								<xsl:when test="fs:is_hstore($name)">
									<xsl:value-of select="./*[local-name()='Name']"/> = <xsl:value-of select="./*[local-name()='Name']"/> || ('
									
									<xsl:for-each select="key('update-by-hstore-1.1.0', ./*[local-name()='Name'])">
										<xsl:sort select="./*[local-name()='Value']" />
										<xsl:variable name="value" select="./*[local-name()='Value']" />
										<xsl:value-of select="fs:clip_hstore($value)"/>
										<xsl:if test="position() &lt; $total-in-group">,</xsl:if>
									</xsl:for-each>
									'::hstore)
								</xsl:when>
								
								<xsl:otherwise>
									<xsl:value-of select="$name"/> = '<xsl:value-of select="./*[local-name()='Value']"/>'
								</xsl:otherwise>
								
							</xsl:choose>
							
							<xsl:if test="position() &lt; $total-groups"> , </xsl:if>
							
						</xsl:for-each>
						
						<xsl:if test="//*[local-name() = 'Filter']">
							WHERE
						</xsl:if>
						
					</xsl:when>
					<xsl:when test="$version='2.0.0'">
						UPDATE <xsl:value-of select="$tableName"/> SET
						<xsl:variable name="total-groups" select="count(./*[local-name()='Property'][generate-id() = generate-id(key('update-by-hstore-2.0.0', ./*[local-name()='ValueReference'])[1])])" />
						
						<xsl:for-each select="./*[local-name()='Property'][count(. | key('update-by-hstore-2.0.0', ./*[local-name()='ValueReference'])[1]) = 1]">
							<xsl:sort select="./*[local-name()='ValueReference']" />
							<xsl:variable name="total-in-group" select="count(key('update-by-hstore-2.0.0', ./*[local-name()='ValueReference']))" />
							
							<xsl:variable name="name" select="./*[local-name()='ValueReference']" />
							
							<xsl:choose>
								
								<xsl:when test="$name=$geometryAttribute and string-length($geometryData) > 0">
									"<xsl:value-of select="$name"/>" = ST_GeomFromGML('<xsl:value-of select="string($geometryData)" />')
								</xsl:when>
								
								
								<xsl:when test="fs:is_hstore($name)">
									<xsl:value-of select="./*[local-name()='ValueReference']"/> = <xsl:value-of select="./*[local-name()='ValueReference']"/> || ('
									
									<xsl:for-each select="key('update-by-hstore-2.0.0', ./*[local-name()='ValueReference'])">
										<xsl:sort select="./*[local-name()='Value']" />
										<xsl:variable name="value" select="./*[local-name()='Value']" />
										<xsl:value-of select="fs:clip_hstore($value)"/>
										<xsl:if test="position() &lt; $total-in-group">,</xsl:if>
									</xsl:for-each>
									'::hstore)
								</xsl:when>
								
								<xsl:otherwise>
									<xsl:value-of select="$name"/> = '<xsl:value-of select="./*[local-name()='Value']"/>'
								</xsl:otherwise>
								
							</xsl:choose>
							
							<xsl:if test="position() &lt; $total-groups"> , </xsl:if>
							
						</xsl:for-each>
						
						<xsl:if test="//*[local-name() = 'Filter']">
							WHERE
						</xsl:if>
						
					</xsl:when>
				</xsl:choose>
			</Statement>
		</xsl:for-each>
		
	</xsl:template>
    
</xsl:stylesheet>