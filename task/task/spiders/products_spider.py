import random
import time
from typing import Any

import scrapy
from scrapy.http import Response
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('-headless')


class SportsProductSpider(scrapy.Spider):
    name = 'product'

    allowed_domains = ['academy.com']

    start_urls = [
        'https://www.academy.com/p/nike-womens-court-legacy-next-nature-shoes'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.start_urls[0])


    def parse(self, response: Response, **kwargs: Any) -> Any:
        # driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        # time.sleep(5)

        name = self.get_single_data_by_selector('h1.productTitle--FWmyK', response, self.driver)
        price = self.get_single_data_by_selector('span.pricing.nowPrice', response, self.driver)
        collected_data = self.get_data_by_selector('span.swatchName--KWu4Q', response, self.driver)

        current_colour, current_size, _ = collected_data if collected_data else '', '', ''

        available_colours = self.get_all_available_colors(response, self.driver)

        self.driver.quit()

        product_data = {
            'name': name,
            'price': price,
            'size': current_size,
            'colour': current_colour,
            'available_colours': available_colours,
        }

        yield product_data

    def get_all_available_colors(self, response, driver):
        button_elements = driver.find_elements(by=By.CSS_SELECTOR, value='button.buttonWrapper--S9sgu')
        available_colours = []

        for button_element in button_elements:
            colour = self.get_single_data_by_selector('span.swatchName--KWu4Q', response, driver)
            available_colours.append(colour)
            button_element.click()
            time.sleep(random.uniform(2, 5))

        return available_colours

    @staticmethod
    def get_single_data_by_selector(selector, response, driver):
        """
        Tries to get/fetch element by normal CSS Selector using only Scrapy,
        if not - it is dynamic and gets it with Selenium
        """

        data = response.css(selector + '::text').get()
        if data is None:
            try:
                data = driver.find_element(by=By.CSS_SELECTOR, value=selector).text
            except NoSuchElementException:
                data = None

        return data.strip() if data else None

    @staticmethod
    def get_data_by_selector(selector, response, driver):
        """
        Same as the method 'get_single_data_by_selector' but returns a collection of data
        """

        data = response.css(selector + '::text').getall()
        if data is None:
            data = [element.text for element in driver.find_elements(by=By.CSS_SELECTOR, value=selector)]

        # data = [text.strip() for text in data]
        return data
