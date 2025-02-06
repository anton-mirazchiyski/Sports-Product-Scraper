from typing import Any

import scrapy
from scrapy.http import Response


class SportsProductSpider(scrapy.Spider):
    name = 'product'

    allowed_domains = ['academy.com']

    start_urls = [
        'https://www.academy.com/p/nike-womens-court-legacy-next-nature-shoes'
    ]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        name = response.css('h1::text').get().strip()
        price = response.css('span.pricing.nowPrice::text').get()

        product_data = {
            'name': name,
            'price': price,
        }

        yield product_data

