# get the imports
import openpyxl
from cities_dictionary import cities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
import re
import csv
import os
import shutil

save_to = 'example.xlsx'


def get_clear_text(text):
    pattern = re.compile("^[^:]*:\s+")
    match = pattern.search(text)
    if match:
        new_string = text[match.end():]
    else:
        new_string = text
    return new_string


def main_get_data(label, link, filename):
    label = label
    link = link
    address = ''
    website = ''
    telephone = ''
    address_code = ''

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(link)
    time.sleep(3)
    get_address = "Copy address"
    get_website = "Open website"
    get_telephone = "Copy phone number"
    get_post = "Copy plus code"
    # address
    try:
        address_elem = driver.find_element(
            By.CSS_SELECTOR, f"button[data-tooltip='{get_address}']")
        address = address_elem.get_attribute("aria-label")
        address = get_clear_text(address)
        print(address)
    except:
        with open('log_of_links.txt', 'a', newline='', encoding='utf-8') as file:

            file.write(f"Was an error with address in {label}")
    # website link
    try:
        website_elem = driver.find_element(
            By.CSS_SELECTOR, f"a[data-tooltip='{get_website}']")
        website = website_elem.get_attribute("aria-label")
        website = get_clear_text(website)
        print(website)
    except:
        with open('log_of_links.txt', 'a', newline='', encoding='utf-8') as file:
            file.write(f"Was an error with website in {filename}: {label}")
    # telephone
    try:
        telephone_elem = driver.find_element(
            By.CSS_SELECTOR, f"button[data-tooltip='{get_telephone}']")
        telephone = telephone_elem.get_attribute('aria-label')
        telephone = get_clear_text(telephone)
        print(telephone)
    except:
        with open('log_of_links.txt', 'a', newline='', encoding='utf-8') as file:
            file.write(f"Was an error with telephone in {label}")
    # code
    try:
        address_code_elem = driver.find_element(
            By.CSS_SELECTOR, f"button[data-tooltip='{get_post}']")
        address_code = address_code_elem.get_attribute('aria-label')
        address_code = get_clear_text(address_code)
        print(address_code)
    except:
        with open('log_of_links.txt', 'a', newline='', encoding='utf-8') as file:
            file.write(f"Was an error with code in {label}")

    row = [label, address, website, telephone, address_code]
    workbook = openpyxl.load_workbook(save_to)
    worksheet = workbook.active
    worksheet.append(row)
    workbook.save(save_to)
    driver.quit()


folder_path = '.'
folder_to = './done'

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        print(f'Working with {file_path}')
        with open(file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                label = row[0]
                link = row[1]
                main_get_data(label, link, filename)
        shutil.move(file_path, folder_to)
