import requests
from requests import get
from bs4 import BeautifulSoup 
from selenium import webdriver
from time import sleep
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/Users/rachelforbes/Documents/chromedriver", options=options)

# cake recipes
url = "https://www.allrecipes.com/recipes/276/desserts/cakes/?internalSource=hub%20nav&referringId=79&referringContentType=Recipe%20Hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202"

driver.get(url)


#click_more=True
#while click_more:
#    WebDriverWait(driver, 30).until(EC.presence_of_element_located((driver.find_elements_by_class_name, "category-page-list-related-load-more-button"))).click()

load_more = driver.find_elements_by_class_name("category-page-list-related-load-more-button")

#note: this does not continue to click load more once the new page is loaded, need to figure out a wait script to load additional pages
for x in range(len(load_more)):
    if load_more[x].is_displayed():
        driver.execute_script("arguments[0].click();", load_more[x])
        time.sleep(1)

page_source = driver.page_source

soup = BeautifulSoup(page_source, "html.parser")
#print(soup.prettify())

recipes = []
reviewCount = []
links = []

recipe_div = soup.find_all('div', class_='recipeCard__detailsContainer')

for container in recipe_div:
    name = container.a.h3.text
    name = name.replace("\n", "", 5)
    recipes.append(name.strip())
    link = str(container.a)
    start = link.index('www')
    end = link.index('" title')
    links.append(link[start:end])

print(recipes)
print(links)

reviewCount_div = soup.find_all('span', class_= 'recipeCard__reviewsCount')

for container in reviewCount_div:
    reviews = container.text
    reviews = reviews.replace("\n", "", 2)
    reviewCount.append(reviews.strip())

print(reviewCount)

ingredientList = []
ingridents_div = soup.find_all('div', class_= 'recipe-shopper-wrapper')

for recipe in recipes:
    driver.get(x)
    for section in ingridents_div:
        ingredients = container.section.fieldset.ul.label.text
        print(ingridents)
recipe_df = pd.DataFrame(list(zip(recipes, reviewCount, links)),
            columns = ["Recipe Name", "Review Count", "Link"])


