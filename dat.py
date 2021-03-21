import scrapy


class GetdataSpider(scrapy.Spider):
    name = 'dat'
    allowed_domains = ['aback-blog.iwi.unisg.ch']
    start_urls = ['https://aback-blog.iwi.unisg.ch/category/agile-innovation/',
    'https://aback-blog.iwi.unisg.ch/category/allgemein/',
    'https://aback-blog.iwi.unisg.ch/category/artificial-intelligence/',
    'https://aback-blog.iwi.unisg.ch/category/corporate-entrepreneurship/',
    'https://aback-blog.iwi.unisg.ch/category/cyber-security/',
    'https://aback-blog.iwi.unisg.ch/category/digital/',
    'https://aback-blog.iwi.unisg.ch/category/future-of-work/',
    'https://aback-blog.iwi.unisg.ch/category/kolumne/',
    'https://aback-blog.iwi.unisg.ch/category/learning-innovations/',
    'https://aback-blog.iwi.unisg.ch/category/learning-to-code/',
    'https://aback-blog.iwi.unisg.ch/category/lehrstuhlnachrichten/',
    'https://aback-blog.iwi.unisg.ch/category/leseempfehlung/',
    'https://aback-blog.iwi.unisg.ch/category/linktipps/',
    'https://aback-blog.iwi.unisg.ch/category/management-tools/',
    'https://aback-blog.iwi.unisg.ch/category/mobile-business/',
    'https://aback-blog.iwi.unisg.ch/category/praxisprojekt/',
    'https://aback-blog.iwi.unisg.ch/category/productivity-tools/',
    'https://aback-blog.iwi.unisg.ch/category/publikation/',
    'https://aback-blog.iwi.unisg.ch/category/smart-iot/',
    'https://aback-blog.iwi.unisg.ch/category/sponsored-post/',
    'https://aback-blog.iwi.unisg.ch/category/sports-digitalization/',
    ]



    def parse(self, response):

        # An dieser Stelle benoetigen wir die xPath von den Elementen, die wir aus der Webseite extrahieren wollen 
        # Dazu muessen wir uns erst einmal klar machen, wie genau die Webseitenstruktur aufgebaut ist. Hierfuer nutzen wir den Google Chrome Inspector (Rechte Maustase -> Inspect)
        # Sobald wir die Webseitenstruktur kennen, nutzen wir den xPath-Helper, um den xPath- des Elements zu identifizieren, welches wir extrahieren wollen 
        single_blogbeitrag = response.xpath('//*[@class="col-xs-12 col-sm-6 col-md-4 col-lg-3 col-xl-2"]')

        # Wir haben durch die Webseitenstruktur gesehen, dass die Klasse "listing-summary col-xs-12 col-sm-6" unsere Informationen enthaelt. Daher bauen wir nun eine Schleife, die diese Elemente extrahiert

        for blog in single_blogbeitrag: 
            Artikel_URL = blog.xpath('//div[@class="post-title"]/h1/text()').extract()



            # Da wird die Ergebnisse ausgeben lassen wollen, definieren wir ein Dictionary und entfernen die pass-Funktion 
            yield {'Autor': Artikel_URL}


