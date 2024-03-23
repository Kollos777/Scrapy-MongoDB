import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com']

    def __init__(self):
        self.output = []
        self.authors = []

    def parse(self, response):
        for quote in response.css('div.quote'):
            tags = quote.css('div.tags a.tag::text').getall()
            author = quote.css('span small::text').get()
            quote_text = quote.css('span.text::text').get()

            self.output.append({
                'tags': tags,
                'author': author,
                'quote': quote_text,
            })

            author_url = quote.css('span a::attr(href)').get()
            if author_url:
                yield response.follow(author_url, self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        content = response.xpath("/html//div[@class='author-details']")
        fullname = content.xpath("h3[@class='author-title']/text()").get().strip()
        born_date = content.xpath("p/span[@class='author-born-date']/text()").get().strip()
        born_location = content.xpath("p/span[@class='author-born-location']/text()").get().strip()
        description = content.xpath("div[@class='author-description']/text()").get().strip()

        self.authors.append({
            'fullname': fullname,
            'born_date': born_date,
            'born_location': born_location,
            'description': description,
        })

    def closed(self, reason):
        with open('quotes.json', 'w', encoding='utf-8') as f:
            json.dump(self.output, f, ensure_ascii=False, indent=4)
        with open('authors.json', 'w', encoding='utf-8') as f:
            json.dump(self.authors, f, ensure_ascii=False, indent=4)

    