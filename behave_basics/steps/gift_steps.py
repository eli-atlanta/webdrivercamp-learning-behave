from behave import *
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from components.base import Base
from components.gifts_page import *
from environment import *
import time
import csv

# use_step_matcher("re")

@step("Print The current url")
def print_current_url(context):
    print(context.browser.current_url)

@step("Navigate to {url}")
def step_impl(context, url):
    context.browser.get(url)
    print_current_url(context)
#    context.browser = webdriver.Chrome()
#    context.browser.maximize_window()
#    context.browser.get(url)


@step("Search for {search_item}")
def step_impl(context, search_item):
    page = Base(context.browser)
    search_field_xpath = "//input[@name='searchTerm']"
    search_button_xpath = "//button[@aria-label='search']"
    page.find_element((By.XPATH, search_field_xpath))
    page.input_search_text(search_item,(By.XPATH, search_field_xpath))
    page.click((By.XPATH, search_button_xpath))
    time.sleep(5)

@step("Verify header of the page contains {search_item}")
def step_impl(context, search_item):
    page = Base(context.browser)
    h1_xpath = "//h1[@data-test='page-title']"
    page.assert_text(search_item, (By.XPATH, h1_xpath))

@step("Select {option} in {section} section")
def step_impl(context, option, section):
    context.gifts_page = GiftsPage(context.browser)
    context.gifts_page.select_option(option, section)

# @step("Collect all items on the first page into {context_var}")
# def step_impl(context, context_var):
#     items = context.gifts_page.collect_product_info()
#     setattr(context, context_var, items)
#     for i, item in enumerate(context.collected_items):
#         print(f"{i + 1}. {item}")
#     # print(type(context.collected_items))
#     for i in range(0, len(context.collected_items)):
#         # product_price = context.collected_items[i]["price"]
#         # product_price_clean = product_price.replace("$", "")
#         # product_price_split = product_price_clean.split(" - ")
#         # product_price_split = list(map(float, product_price_split))
#         # print(product_price_split)
#         # print(type(product_price_split))

@step("Collect all items on the first page into {var} on the {level} level")
def step_impl(context, var, level=None):
    items = context.gifts_page.collect_product_info()
    if level is not None:
        setattr(context.feature, var, items)
        # for i, item in enumerate(context.feature.collected_items):
        #     print(f"{i + 1}. {item}")
        #     product_ship = context.feature.collected_items[i]["shipment"]
        #     print(product_ship)
        # print(type(context.feature.collected_items))
        # for i in range(0, len(context.feature.collected_items)):
        # product_price = context.feature.collected_items[i]["price"]
        # product_price_clean = product_price.replace("$", "")
        # product_price_split = product_price_clean.split(" - ")
        # product_price_split = list(map(float, product_price_split))
        # print(product_price_split)
        # print(type(product_price_split))
    else:
        setattr(context, var, items)


# @step("Verify all collected results' price is {condition}")
# def step_impl(context, condition):
#     for i in range(0, len(context.collected_items)):
#         product_price = context.collected_items[i]["price"]
#         product_price_clean = product_price.replace("$", "")
#         product_price_split = product_price_clean.split(" - ")
#         product_price_split = list(map(float, product_price_split))
#         try:
#             assert eval(f'{product_price_split[0]} {condition}')
#         except AssertionError:
#             print(f"{i + 1}. Error: The price of ${product_price_split[0]}, for |{context.collected_items[i]["name"]}| does NOT meet the condition: {condition}")

@step("Verify all collected results' {param} is {condition}")
def step_impl(context, param, condition):
    if 'price' in param:
        for i in range(0, len(context.feature.collected_items)):
            product_price = context.feature.collected_items[i]["price"]
            product_price_clean = product_price.replace("$", "")
            product_price_split = product_price_clean.split(" - ")
            product_price_split = list(map(float, product_price_split))
            try:
                assert eval(f'{product_price_split[0]} {condition}')
            except AssertionError:
                print(f"{i + 1}. Error: The price of ${product_price_split[0]}, for |{context.feature.collected_items[i]["name"]}| does NOT meet the condition: {condition}")
    elif 'shipment' in param:
        for i in context.feature.collected_items:
            product_parameter = i[param]
            if i[param] is not None:
                try:
                    assert condition in product_parameter
                except AssertionError:
                    print(f"The {context.feature.collected_items[0]["name"]} Does NOT meet this condition: {condition}")
            else:
                print(f"The {context.feature.collected_items[0]["name"]} Does NOT meet this condition: {condition}")
    else:
        print(f"Please enter a valid parameter in the feature file")