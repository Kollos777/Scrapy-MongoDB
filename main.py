import json
from scrapy.crawler import CrawlerProcess
from models import Author, Quote
from my_scraper.my_scraper.spiders.quotes_spider import QuotesSpider
from mongoengine import connect

def main():
    connect('mydatabase', host='mongodb+srv://kollos:B4tsy9vyOKU4kD8D@nosql.3ivomcd.mongodb.net/')

    with open('authors.json', 'r', encoding='utf-8') as f:
        authors_data = json.load(f)

    for author_data in authors_data:
        author = Author(**author_data)
        try:
            author.save()
        except Exception as e:
            print(f"Error saving author: {e}")


    with open('quotes.json', 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)

    for quote_data in quotes_data:
        author_fullname = quote_data.pop('author')
        author = Author.objects(fullname=author_fullname).first()
        if author:
            quote = Quote(author=author, **quote_data)
            try:
                quote.save()
            except Exception as e:
                print(f"Error saving author: {e}")
        else:
            print(f"Author with fullname '{author_fullname}' not found.")



if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
    main()
