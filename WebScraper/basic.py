from selenium import webdriver
from bs4 import BeautifulSoup
import ipdb
import pandas as pd
from time import sleep
import json
import datetime
import re
import os

def driver_init():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("./chromedriver", options=options)
    return driver

def get_soup(driver, url):
    #add error checking
    driver.get(url)
    return BeautifulSoup(driver.page_source, "lxml")

def dollar_to_int(dollar_string):
    digits = [str(x) for x in range(0, 10)]
    amount = int(''.join([c for c in dollar_string if c in digits]))
    if dollar_string[0] == '-':
        return -1*amount
    return amount
