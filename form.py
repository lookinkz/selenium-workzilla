# get the imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from cities_dictionary import cities
import time
import csv
import re

# create the driver
path = r'.chromedriver_win32\chromedriver.exe'
service = Service(path)
driver = webdriver.Chrome(service=service)
driver.get("https://www.google.com/maps/?hl=en")
html = driver.find_element(By.TAG_NAME, "html")
cities_of_usa = cities

# searching in google map the right place


def search(text):
    search_box.clear()
    search_box.send_keys(text)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

# getting the data from the search by <a> tag


def get_a_tags():
    a_tags = driver.find_elements(By.CLASS_NAME, 'hfpxzc')
    data = list()
    for a in a_tags:
        aria_label = a.get_attribute('aria-label')
        href = a.get_attribute('href')
        lst = [aria_label, href]
        data.append(lst)
    return data

# RegEx for the data from links


def get_clear_text(text):
    pattern = re.compile("^[^:]*:\s+")
    match = pattern.search(text)
    if match:
        new_string = text[match.end():]
    else:
        new_string = text
    return new_string


# srolling the side bar:
def scrolling(html):
    html.send_keys(Keys.TAB * 3)
    while True:
        try:
            time.sleep(1)
            the_end = driver.find_element(By.CLASS_NAME, "HlvSq")
            print("THE END:", the_end.text)
            data = get_a_tags()
            print(len(data))
            break
        except:
            time.sleep(1)
            sidebar = driver.find_elements(By.CLASS_NAME, 'hfpxzc')
            driver.execute_script(
                "arguments[0].scrollIntoView();", sidebar[-1])
            time.sleep(2)
    return data

# working with data


def work_with_data(data):
    get_address = "Copy address"
    get_website = "Open website"
    get_telephone = "Copy phone number"
    get_post = "Copy plus code"
    for i in data:
        label = i[0]
        link = i[1]
        print(label, link)
        driver.get(link)
        time.sleep(2)
        try:
            address_elem = driver.find_element(
                By.CSS_SELECTOR, f"button[data-tooltip='{get_address}']")
            address = address_elem.get_attribute("aria-label")
            address = get_clear_text(address)
            print(address)
        except:
            with open('log.txt', 'a', newline='', encoding='utf-8') as file:

                file.write(f"Was an error with address in {label}")
        try:
            website_elem = driver.find_element(
                By.CSS_SELECTOR, f"a[data-tooltip='{get_website}']")
            website = website_elem.get_attribute("aria-label")
            website = get_clear_text(website)
            print(website)
        except:
            with open('log.txt', 'a', newline='', encoding='utf-8') as file:
                file.write(f"Was an error with website in {label}")
        try:
            telephone_elem = driver.find_element(
                By.CSS_SELECTOR, f"button[data-tooltip='{get_telephone}']")
            telephone = telephone_elem.get_attribute('aria-label')
            telephone = get_clear_text(telephone)
            print(telephone)
        except:
            with open('log.txt', 'a', newline='', encoding='utf-8') as file:
                file.write(f"Was an error with telephone in {label}")
        try:
            address_code_elem = driver.find_element(
                By.CSS_SELECTOR, f"button[data-tooltip='{get_post}']")
            address_code = address_code_elem.get_attribute('aria-label')
            address_code = get_clear_text(address_code)
            print(address_code)
        except:
            with open('log.txt', 'a', newline='', encoding='utf-8') as file:
                file.write(f"Was an error with code in {label}")

# writing row to the csv file
        row = [geo, label, address, website, telephone, address_code]
        with open('my_file.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(row)


# START THE BROWSER
for state, cities in cities_of_usa.items():
    for city in cities:
        geo = f"{city}, {state}, USA"
        what_to = f"Lawyer in {geo}"
        # searching...
        search_box = driver.find_element(by='id', value='searchboxinput')

        search(what_to)
        time.sleep(5)

        # scrolling...
        data = scrolling(html)
        with open('log.txt', 'a', newline='', encoding='utf-8') as file:
            file.write('--- WORKING WITH THAT DATA ---')
            file.write(data)

            # working with data
        work_with_data(data)

        # QUIT FROM THE PROGRAM
        driver.quit()
