# get the imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager 
import time, csv, re

# create the driver
options = webdriver.ChromeOptions() 
options.headless = True 
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.google.com/maps")

# searching in google map the right place
def search(text):
    search_box.clear()
    search_box.send_keys(text)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

# getting the data from the search by <a> tag
def get_a_tags(text):
    a_tags = driver.find_elements(By.CLASS_NAME, text)
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


# START THE BROWSER
# searching...
search_box = driver.find_element(by='id', value='searchboxinput')
geo = "Montana USA"
what_to = f"Lawyer in {geo}"

search(what_to)
time.sleep(5)

# scrolling... .kA9KIf (By.CSS_SELECTOR, f"a[data-tooltip='Вебсайтты ашу']")
element = driver.find_element(By.CSS_SELECTOR, f"div[class='m6QErb DxyBCb kA9KIf dS8AEf ecceSd']")
print(element.text)   
    
# QUIT FROM THE PROGRAM
driver.quit()
