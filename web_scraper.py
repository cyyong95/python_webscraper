import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup


def launch_chrome():
    # Any url with the wrong search parameter will redirect you to a new search page
    url = "https://www.expedia.com.my/Flights-Search?flight-type=on&starDate=25%2F05%2F2019&endDate=25%2F05%2F20\
           19&mode=search&trip=roundtrip&leg1=from%3AKuala+Lumpur%2C+Malaysia+%28KUL-Kuala+Lumpur+Intl.%29%2Cto%3\
           ASingapore%2C+Singapore+%28SIN-Changi%29%2Cdeparture%3A25%2F05%2F2019TANYT&leg2=from%3ASingapore%2C+Si\
           ngapore+%28SIN-Changi%29%2Cto%3AKuala+Lumpur%2C+Malaysia+%28KUL-Kuala+Lumpur+Intl.%29%2Cdeparture%3A25\
           %2F05%2F2019TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY"

    # Run the web driver
    driver = webdriver.Chrome("C:\\Users\\Chun Yu\\Downloads\\chromedriver.exe")
    driver.get(url)
    return driver


def get_search_page(chrome):
    # Input departure location
    departure_input = chrome.find_element_by_id('Leg1departureReenterText')
    departure_input.clear()
    departure_input.send_keys("Kuala Lumpur, Malaysia (KUL-Kuala Lumpur Intl.)")
    time.sleep(2)

    # Input arrival location
    arrival_input = chrome.find_element_by_id("Leg1arrivalReenterText")
    arrival_input.clear()
    arrival_input.send_keys("Singapore, Singapore (SIN-All Airports)")
    time.sleep(2)

    # Input departure date
    depart_date_input = chrome.find_element_by_id("departDateInput1")
    depart_date_input.clear()
    depart_date_input.send_keys("26/05/2019")
    time.sleep(2)

    # Input arrival date
    return_date_input = chrome.find_element_by_id("returnDateInput1")
    return_date_input.clear()
    return_date_input.send_keys("26/05/2019")
    time.sleep(2)

    # Click on somewhere to move focus away from DatePicker
    footer_click = chrome.find_element_by_id("footer-copyright-msg")
    footer_click.click()
    time.sleep(2)

    # Search for result
    button_search = chrome.find_element_by_id("continue-search")
    button_search.click()
    time.sleep(2)


def get_html(chrome):

    airline_name = []
    airline_price = []

    html = chrome.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(html, 'html.parser')

    # Get airline price
    for price in soup.find_all('h3', {'data-test-id': 'result-header'}):
        airline_price.append(get_price(price.text))

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
    time.sleep(2)
    get_search_page(chrome_driver)
    get_html(chrome_driver)








