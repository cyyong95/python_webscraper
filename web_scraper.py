import time
import re
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def launch_chrome():
    # Any url with the wrong search parameter will redirect you to a new search page
    url = r"https://www.expedia.com/Flights-Search?starDate=08/30/2019&endDate=09/30/2019&mode=search&trip=roundtrip&" \
          r"leg1=from:KUL,to:SIN,departure:08/03/2019TANYT&leg2=from:SIN,to:KULdeparture:09/03/2019TANYT&" \
          r"passengers=children:0,adults:1,seniors:0,infantinlap:Y&mode=search&origref=www.expedia.com"

    # Add proxy
    proxy = r"134.209.99.127:8080"
    options = Options()
    options.add_argument('--proxy-server=%s' % proxy)

    # Run the web driver
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(random.randint(1, 5))
    driver.get(url)
    return driver


def get_departure_price(chrome):

    # Let the page load the first time
    time.sleep(10)

    airline_name = []
    airline_price = []

    html = chrome.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(html, 'html.parser')

    # Get airline price
    for price in soup.find_all('span', {'data-test-id': 'listing-price-dollars'}):
        airline_price.append(price.text)

    # Get airline name
    for span in soup.find_all('span', {'data-test-id': 'airline-name'}):
        airline_name.append(span.text.strip())

    print_result(airline_name, airline_price)


def print_result(airline_name, airline_price):
    # Number of results in both list must tally
    if len(airline_name) != len(airline_price):
        print("Length of lists does not tally.")
        return

    # Print results
    for i in range(len(airline_name)):
        if airline_name[i] == "Multiple Airlines":
            continue
        print('Airline: {}\tPrice: {}'.format(airline_name[i], airline_price[i]))


def get_price(dirty_text):
    # Remove white spaces
    clean_text = dirty_text.strip()

    # Get the price from the text
    pattern = r'RM[0-9]*,?[0-9]+$|RM[0-9]+$'
    price_list = re.findall(pattern, clean_text)

    # If match found, return result
    if len(price_list) == 1:
        return price_list[0]


if __name__ == '__main__':
    chrome_driver = launch_chrome()
    get_departure_price(chrome_driver)




