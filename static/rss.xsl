<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="3.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml">
      <head>
        <title><xsl:value-of select="/rss/channel/title"/> RSS Feed</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"/>
        <meta charset="UTF-8"/>
        
        <link type="text/css" rel="stylesheet" href="https://xaselgio.net/css/styles.d225b84765ebd5eb4ab83f06e7e09371032e7199475bda8157f1f285bac0e0720482db82ed01710cced83ed937c019f9d0dfe2da88e3600f24c09c6903e360ee.css" integrity="sha512-0iW4R2Xr1etKuD8G5+CTcQMucZlHW9qBV/HyhbrA4HIEgtuC7QFxDM7YPtk3wBn50N/i2ojjYA8kwJxpA+Ng7g==" />
        <style>
          .aboutfeeds {
            margin: 24px 0; padding: 12px;
            border: 2px solid var(--default_accent);
            background-color: var(--default_hl_bg)
          }
          .head {
            display: flex;
            flex-direction: row;
            align-items: center;
          }
          .logo {
            width: 50px;
            max-height: 50px;
            border-radius: 5px;
            display: block;
            margin-right: 10px;
          }
          .rssLogo {
            display: block;
            margin-right: 10px;
          }
          header h1 {
            display: flex;
            flex-direction: row;
            align-items: center;
          }
          body{max-width:768px;margin:0 auto;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";font-size:16px;line-height:1.5em}section{margin:30px 15px}h1{font-size:2em;margin:.67em 0;line-height:1.125em}h2{border-bottom:1px solid #eaecef;padding-bottom:.3em}.alert{background:#fff5b1;padding:4px 12px;margin:0 -12px}a{text-decoration:none}.entry h3{margin-bottom:0}.entry p{margin:4px 0}
        
        </style>
      </head>
      <body>
        <header>
          <h1>
	  🗞️ <xsl:value-of select="/rss/channel/title"/>
          </h1>
          <div class="aboutfeeds">
            <p>This is a web feed, also known as an RSS feed. <strong>Subscribe</strong> by copying the URL into your RSS reader.</p>
          </div>
          <div class="head">
            <div class="avatar">
              <img class="logo" src="/img/logo.png" alt="Site Logo"/>
            </div>
            <div class="description">
              <p><xsl:value-of select="/rss/channel/description"/></p>
              <p><a hreflang="en"><xsl:attribute name="href"><xsl:value-of select="/rss/channel/link"/></xsl:attribute>Visit Website &#x2192;</a></p>
            </div>
          </div>
        </header>
        <div id="content">
          <main>
            <h2>🗞️ Recent Posts</h2>
            <xsl:for-each select="/rss/channel/item">
              <article>
                <h3><a target="_blank"><xsl:attribute name="href"><xsl:value-of select="link"/></xsl:attribute><xsl:value-of select="title"/></a></h3>
                <footer>Published: <time><xsl:value-of select="pubDate" /></time></footer>
              </article>
            </xsl:for-each>
          </main>
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
