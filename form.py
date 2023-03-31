# get the imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# create the driver
path = r'.chromedriver_win32\chromedriver.exe'
service = Service(path)
driver = webdriver.Chrome(service=service)
driver.get("https://www.google.com/maps")

driver.execute_script("window.scrollBy(0,500)", "")
time.sleep(5)


# Scroll to the end of the page
def scroll_sidebar_to_end():
    # find the sidebar element
    sidebar = driver.find_element_by_css_selector("div.widget-scene")

    # get the initial height of the sidebar
    initial_height = driver.execute_script(
        "return arguments[0].scrollHeight;", sidebar)

    # scroll the sidebar down until the height stops changing (i.e., the end of the SPA is reached)
    while True:
        driver.execute_script(
            "arguments[0].scrollTo(0, arguments[0].scrollHeight);", sidebar)
        time.sleep(2)  # adjust sleep time as needed
        new_height = driver.execute_script(
            "return arguments[0].scrollHeight;", sidebar)
        if new_height == initial_height:
            break
        initial_height = new_height


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
    print(len(data))


# START THE BROWSER
# searching...
search_box = driver.find_element(by='id', value='searchboxinput')
search('Алматы')
search('строительно-монтажные компании')
time.sleep(5)


# scrolling...
# scrolling_to_the_end('hfpxzc')
scroll_sidebar_to_end()
# getting the data
get_a_tags('hfpxzc')

# QUIT FROM THE PROGRAM
driver.quit()
