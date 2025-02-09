import random
import time
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
        driver_options = self.set_driver_options()
        driver = self.setup_driver(0, driver_options)

        name = self.get_single_data_by_selector('h1.productTitle--FWmyK', response, driver)
        price = self.get_single_data_by_selector('span.pricing.nowPrice', response, driver)
        current_color, current_size, _ = self.get_data_by_selector('span.swatchName--KWu4Q', response, driver)

        # available_colors = self.get_all_available_colors(response, driver)

        self.close_driver(driver)

        # print(name, price, current_color)
        # print(available_colors)

        product_data = {
            'name': name,
            'price': price,
            'size': current_size,
            'color': current_color,
            # 'available_colors': available_colors,
        }

        yield product_data

    def get_all_available_colors(self, response, driver):
        button_elements = driver.find_elements(by=By.CSS_SELECTOR, value='button.buttonWrapper--S9sgu')
        available_colors = []

        for button_element in button_elements:
            color = self.get_single_data_by_selector('span.swatchName--KWu4Q', response, driver)
            available_colors.append(color)
            button_element.click()
            time.sleep(random.uniform(2, 5))

        return available_colors

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

    @staticmethod
    def get_data_by_selector(selector, response, driver):
        """
        Same as the method 'get_single_data_by_selector' but returns a collection of data
        """

        data = response.css(selector + '::text').getall()
        if data is None:
            data = [element.text for element in driver.find_elements(by=By.CSS_SELECTOR, value=selector)]

        data = [text.strip() for text in data]
        return data

    @staticmethod
    def set_driver_options():
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        return options

    def setup_driver(self, urls_idx, options):
        driver = webdriver.Firefox(options=options)
        driver.get(self.start_urls[urls_idx])
        return driver

    def close_driver(self, driver):
        driver.quit()
