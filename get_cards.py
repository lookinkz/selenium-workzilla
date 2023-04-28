# get the imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from cities_dictionary import cities
import time
import csv
cities_of_usa = cities


def main_get_all_tags():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.google.com/maps/?hl=en")
    html = driver.find_element(By.TAG_NAME, "html")
    # searching
    search_box = driver.find_element(by='id', value='searchboxinput')
    search_box.clear()
    search_box.send_keys(what_to)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)
    # scrolling
    html.send_keys(Keys.TAB * 3)
    while True:
        try:
            time.sleep(1)
            the_end = driver.find_element(By.CLASS_NAME, "HlvSq")
            print("THE END:", the_end.text)
            # getting a tags
            a_tags = driver.find_elements(By.CLASS_NAME, 'hfpxzc')
            print(f'{state}, {city}: {len(a_tags)} tags')
            for a in a_tags:
                aria_label = a.get_attribute('aria-label')
                href = a.get_attribute('href')
                name_of_file = f'{state}_{city}.csv'
                with open(name_of_file, 'a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([aria_label, href])
            break
        except:
            time.sleep(1)
            sidebar = driver.find_elements(By.CLASS_NAME, 'hfpxzc')
            driver.execute_script(
                "arguments[0].scrollIntoView();", sidebar[-1])
            time.sleep(2)
    driver.quit()


for state, cities in cities_of_usa.items():
    for city in cities:
        try:
            # what we want to search
            geo = f"{city}, {state}, USA"
            what_to = f"Lawyer in {geo}"
            with open('log.txt', 'a', newline='', encoding='utf-8') as file:
                text = f'Working with {state}, {city}...\n'
                file.write(text)
                # launcing the browser
            print(f"\n\nWorking on {state}: {city}.")
            main_get_all_tags()
        except:
            print(f"Error in {state}: {city}\n\n")
            with open('log.txt', 'a', newline='', encoding='utf-8') as file:
                text = f'\nError in {state}, {city}...\n'
                file.write(text)
            continue
