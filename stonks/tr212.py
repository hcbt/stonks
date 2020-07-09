import time
import sys
import signal
import curses
import pickle

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
from lxml import html
from lxml import etree

import credentials

#Loads the driver
def load_driver():
    chrome_options = Options()

    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    #chrome_options.add_argument("--disable-dev-shm-usage")
    #chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options = chrome_options)
    
    return driver

#Login page
def login(driver, url, username, password):
    driver.get(url)
    time.sleep(5)

    login_field = driver.find_element_by_xpath("//*[@id='username-real']")
    password_field = driver.find_element_by_xpath("//*[@id='pass-real']")
    login_button = driver.find_element_by_xpath("/html/body/div[1]/section[2]/div/div/div/form/input[2]")

    login_field.clear()
    password_field.clear()
    
    login_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

#Switch to demo mode if needed
def login_to_demo(driver, demo_url):
    driver.get(demo_url)

#Show P/L, free cash, blocked cash and total cash
def equity():
    soup = BeautifulSoup(driver.page_source, "lxml")

    live_result = driver.find_element_by_xpath("//*[@id='equity-ppl']/span[2]")
    equity_free = driver.find_element_by_xpath("//*[@id='equity-free']/span[2]")
    equity_blocked = driver.find_element_by_xpath("//*[@id='equity-blocked']/span[2]")
    equity_total = driver.find_element_by_xpath("//*[@id='equity-total']/span[2]")
    equity_status = driver.find_element_by_xpath("//*[@id='equity-indicator']/div/span[2]/span")

#Get current price of current chart
def get_ticker(driver):
    soup = BeautifulSoup(driver.page_source, "lxml")
    ticker = soup.find("span", class_ = "inst-name")
    return ticker.string

def get_bid(driver):
    soup = BeautifulSoup(driver.page_source, "lxml")
    bid = soup.find("span", class_ = "chart-trade-sell")
    return bid.string

def get_ask():
    soup = BeautifulSoup(driver.page_source, "lxml")
    ask = soup.find("span", class_ = "chart-trade-buy")
    return ask.string
        
#Buy button
def buy():
    pass

#Sell button
def sell():
    pass
    
def main():
    url = "https://live.trading212.com/"
    demo_url = "https://demo.trading212.com/"
    
    username = credentials.username
    password = credentials.password

    driver = load_driver()

    login(driver, url, username, password)

    time.sleep(1)
    
    login_to_demo(driver, demo_url)

    time.sleep(5)

    while True:
        time.sleep(1)
        print(get_ticker(driver), get_bid(driver), end = "\r", flush = True)

    signal.pause()
    driver.quit()

if __name__ == "__main__":
    main()
