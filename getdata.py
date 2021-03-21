import scrapy


class GetdataSpider(scrapy.Spider):
    name = 'getdata'
    allowed_domains = ['aback-blog.iwi.unisg.ch']
    start_urls = ['https://aback-blog.iwi.unisg.ch/2021/02/18/neues-projekt-mit-smartfeld-filmint-fuer-kinder-und-jugendliche/'
    ]


    def parse(self, response):

        # An dieser Stelle benoetigen wir die xPath von den Elementen, die wir aus der Webseite extrahieren wollen 
        # Dazu muessen wir uns erst einmal klar machen, wie genau die Webseitenstruktur aufgebaut ist. Hierfuer nutzen wir den Google Chrome Inspector (Rechte Maustase -> Inspect)
        # Sobald wir die Webseitenstruktur kennen, nutzen wir den xPath-Helper, um den xPath- des Elements zu identifizieren, welches wir extrahieren wollen 
        single_blogbeitrag = response.xpath('//*[@class="col-md-6 blog-mobile"]')

        # Wir haben durch die Webseitenstruktur gesehen, dass die Klasse "listing-summary col-xs-12 col-sm-6" unsere Informationen enthaelt. Daher bauen wir nun eine Schleife, die diese Elemente extrahiert

        for blog in single_blogbeitrag: 
            Artikel_Autor = blog.xpath('//*[@rel="author"]/text()').extract()
            Artikel_Titel = blog.xpath('//*[@style="color: #008840;"]/text()').extract()
            Artikel_Tags = blog.xpath('//a[starts-with(@href, "https://aback-blog.iwi.unisg.ch/category/")]/text()').extract()
            Artikel_Text = blog.xpath('//div[@class="col-md-6 blog-mobile"]/p/text()|//div[@class="col-md-6 blog-mobile"]//a/text()').extract()


            # Da wird die Ergebnisse ausgeben lassen wollen, definieren wir ein Dictionary und entfernen die pass-Funktion 
            yield {'Autor': Artikel_Autor,
            'Titel': Artikel_Titel,
            'Tags': Artikel_Tags,
            'Text': Artikel_Text}


