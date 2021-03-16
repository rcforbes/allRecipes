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
#options.add_argument('--headless')
driver = webdriver.Chrome("/Users/rachelforbes/Documents/chromedriver", options=options)


#load urls
links = pickle.load(open('dessert_urls.pkl', 'rb'))
len(links)

# removes urls that link to galleries, not recipes
links= [x for x in links if not x.startswith('/gallery')]

# Add prefix to extracted url
# thtps://www.allrecipes.com/

# elements I want to store
titles = []
rating_counts = []
review_counts = []
photo_counts = []
descriptions = []
ingriedents_list = []
ingredients = []
directions_list = []
directions = []
recipe_summaries = [] # I made this into a dict, should i still use a list?

nutrition_facts = []

# ratings = []
# reviews = []


for i in links:
    url = "https://www.allrecipes.com" + links[1]
    page_source = driver.page_source
    driver.get(url)
    soup = BeautifulSoup(page_source, "html.parser")
    
    # title
    title = soup.find('h1', class_='headline heading-content').text
    titles.append(title)
    
    # rating count
    rating_count = soup.find('span', class_="ugc-ratings-item").text #need to clean
    rating_counts.append(rating_count.strip())
    
    # review count
    review_count = soup.find('a', class_="ugc-ratings-link ugc-reviews-link").text #need to clean
    review_counts.append(review_count.strip())
    
    # photo count
    photo_count = soup.find('a', class_="ugc-ratings-link ugc-photos-link").text #need to clean
    photo_counts.append(photo_count.strip())
    
    # descriptions
    description = soup.find('p', class_="margin-0-auto").text
    descriptions.append(description.strip())
    
    # ingredient list
    ingredients_div = soup.find_all('li', class_= 'ingredients-item')
    for section in ingredients_div:
        ingredient = section.label.span.span.text
        ingredients_list.append(ingredient.strip())
        ingredients.append(ingredients_list)
    
    # directions list
    directions_div = soup.find_all('li', class_='subcontainer instructions-section-item')
    for section in directions_div:
        direction = section.text
        directions_list.append(direction.strip())
        ingredients.append(ingredients_list)
    
    # recipe summaries
    summary_div = soup.find_all('section', class_='recipe-meta-container two-subcol-content clearfix')
    for section in summary_div:
        meta_header_div = section.find_all('div', class_="recipe-meta-item-header")
        meta_headers = []
        for meta_header in meta_header_div:
            meta_header = meta_header.text
            meta_headers.append(meta_header.strip())
        meta_body_div = section.find_all('div', class_="recipe-meta-item-body")
        meta_bodies = []
        for meta_body in meta_body_div:
            meta_body = meta_body.text
            meta_bodies.append(meta_body.strip())
        summary_dic = dict(zip(meta_headers, meta_bodies))
    
    # nutrition facts
    nutrition_div = soup.find_all('div', class_='partial recipe-nutrition-section')
    for section in nutrition_div:
        nutrition = section.find('div', class_="section-body").text
        nutrition_facts.append(nutrition.strip())
    i += 1
    sleep(1)


# save pickle file

pickle.dump(links, open('dessert_urls.pkl', 'wb'))