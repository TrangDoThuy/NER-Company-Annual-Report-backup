import scrapy
from io import StringIO

import re
class PostsSpider(scrapy.Spider):
    name = 'posts'
    allowed_domains = ['www.nasdaq.com']
    start_urls=[
        "https://www.nasdaq.com/market-activity/stocks/screener?exchange=NYSE&render=download"
    ]

    def parse(self, response):
        try:
            file_like = StringIO(response.body)

            # Ignore first row
            file_like.next()

            for line in file_like:
                print(line)
        finally:
            file_like.close()


