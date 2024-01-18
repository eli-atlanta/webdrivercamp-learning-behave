from behave import *
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from behave_basics.components.base import *
import time

class GiftsPage(Base):
    def select_option(self, option, section):
        xpath = f"//span[.='{section}']//ancestor::div//span[.='{option}']//ancestor::a"
        locator = (By.XPATH, xpath)
        self.find_element(locator).location_once_scrolled_into_view
        time.sleep(3)
        self.click(locator)
        time.sleep(3)

    def find_product_name(self, parent):
        product_name_xpath = f"//{parent}a[@data-test='product-title']"
        product_name_locator = (By.XPATH, product_name_xpath)
        data = self.retrieve_text(product_name_locator)
        self.find_element(product_name_locator).location_once_scrolled_into_view
        return data

    def find_product_price(self, parent):
        price_xpath = f"//{parent}span[@data-test='current-price']/span[1]"
        price_locator = (By.XPATH, price_xpath)
        data = self.retrieve_text(price_locator)
        self.find_element(price_locator).location_once_scrolled_into_view
        return data

    def find_product_shipping(self, parent):
        shipping_xpath = f"//{parent}span[@class='h-text-md']//span[@class='h-text-greenDark']"
        shipping_locator = (By.XPATH, shipping_xpath)
        try:
            data = self.retrieve_text(shipping_locator)
            self.find_element(shipping_locator).location_once_scrolled_into_view
            return data
        except TimeoutException:
            return None

    def retrieve_product(self):
        time.sleep(1)
        retrieve_product_xpath = f"//div[@class='styles__StyledCol-sc-fw90uk-0 dOpyUp']"
        retrieve_product_locator = (By.XPATH, retrieve_product_xpath)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(retrieve_product_locator))
        item_element = self.driver.find_elements(*retrieve_product_locator)
        return item_element

    def collect_product_info(self):
        product_info = []
        products = self.retrieve_product()
        product_list = []
        product_list.extend(i for i in products)
        for i in range(1, len(product_list)+1):
            product_xpath = f"div[@class='styles__StyledCol-sc-fw90uk-0 dOpyUp'][" + str(i) + "]//child::"
            product_name = self.find_product_name(product_xpath)
            product_price = self.find_product_price(product_xpath)
            product_shipping = self.find_product_shipping(product_xpath)
            product_info.append({"name": product_name, "price": product_price, "shipment": product_shipping})
        return product_info









