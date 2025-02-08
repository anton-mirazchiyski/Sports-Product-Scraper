from typing import Any

import scrapy
from scrapy.http import Response
from selenium import webdriver
from selenium.webdriver.common.by import By


class SportsProductSpider(scrapy.Spider):
    name = 'product'

    allowed_domains = ['academy.com']

    start_urls = [
        'https://www.academy.com/p/nike-womens-court-legacy-next-nature-shoes'
    ]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        name = response.css('h1::text').get().strip()
        price = response.css('span.pricing.nowPrice::text').get()

        driver = self.setup_driver(urls_idx=0)
        current_color = driver.find_element(by=By.CSS_SELECTOR, value='span.swatchName--KWu4Q').text
        self.close_driver(driver)

        print(current_color)

        product_data = {
            'name': name,
            'price': price,
            'color': current_color,
        }

        yield product_data

    def setup_driver(self, urls_idx):
        driver = webdriver.Firefox()
        driver.get(self.start_urls[urls_idx])
        return driver

    def close_driver(self, driver):
        driver.quit()
