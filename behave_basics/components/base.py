#!/usr/bin/python3
# from lib2to3.pgen2 import driver
from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Base:
    def __init__(self, driver):
        self.driver = driver

    def click(self, locator):
        element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(locator))
        element.click()

    def find_element(self, locator):
        element = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(locator))
        return element

    def input_search_text(self, text, locator):
        element = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(locator))
        element.send_keys(text)

    def retrieve_text(self, locator):
        element = WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(locator))
        return element.text

    def assert_text(self, search_text, locator):
        element = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(locator))
        try:
            assert search_text.lower() in element.text.lower()
            print(f'"{search_text}" is in the header')
        except AssertionError:
            print(f'"{search_text}" is NOT in the header')

    def before_feature(context, feature):
        context.browser = webdriver.Chrome()

