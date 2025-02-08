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
        driver = self.setup_driver(urls_idx=0)

        name = self.get_single_data_by_selector('h1', response, driver)
        price = self.get_single_data_by_selector('span.pricing.nowPrice', response, driver)
        current_color = self.get_single_data_by_selector('span.swatchName--KWu4Q', response, driver)

        self.close_driver(driver)

        print(name, price, current_color)

        product_data = {
            'name': name,
            'price': price,
            'color': current_color,
        }

        yield product_data

    @staticmethod
    def get_single_data_by_selector(selector, response, driver):
        """
        Tries to get/fetch element by normal CSS Selector using only Scrapy,
        if not - it is dynamic and gets it with Selenium
        """

        data = response.css(selector + '::text').get()
        if data is None:
            data = driver.find_element(by=By.CSS_SELECTOR, value=selector).text

        return data.strip()

    def setup_driver(self, urls_idx):
        driver = webdriver.Firefox()
        driver.get(self.start_urls[urls_idx])
        return driver

    def close_driver(self, driver):
        driver.quit()
