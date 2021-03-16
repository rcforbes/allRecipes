import requests
from requests import get
from bs4 import BeautifulSoup 
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/Users/rachelforbes/Documents/chromedriver", options=options)

# dessert recipes- starting at pg 2 due to website formatting

num_pages = list(range(2,417))

# Iterate over pages and modify url
links = []
for i in num_pages:
    url = "https://www.allrecipes.com/recipes/79/desserts/?page=" + str(i)
    page_source = driver.page_source
    driver.get(url)
    soup = BeautifulSoup(page_source, "html.parser")
    for link in soup.find_all('a', class_='tout__titleLink'):
        link = link.get('href')
        links.append(link)
    i += 1
    sleep(1)
# save urls

pickle.dump(links, open('dessert_urls.pkl', 'wb'))

#load urls
links = pickle.load(open('dessert_urls.pkl', 'rb'))
len(links)

# removes urls that link to galleries, not recipes
links= [x for x in links if not x.startswith('/gallery')]
