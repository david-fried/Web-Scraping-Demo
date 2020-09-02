from bs4 import BeautifulSoup as bs
import requests
import time
from splinter import Browser
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    
    browser = init_browser()
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)

    time.sleep(1)
    
    soup = bs(browser.html, "html.parser")
    latest_title = soup.find('div', class_='list_text').find('div', class_='content_title').a.text
    latest_paragraph = soup.find('div', class_='list_text').find('div', class_="article_teaser_body").text
    browser.quit()
    browser = init_browser()

    featured_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_url)
    time.sleep(5)
    soup = bs(browser.html, "html.parser")
    full_img_button = browser.find_by_id('full_image')
    full_img_button.click()
    time.sleep(1)
    browser.find_by_css(".buttons .button").click()
    time.sleep(1)
    browser.find_by_css(".lede").click()
    time.sleep(1)
    featured_image = browser.url
    browser.quit()
    
    table_url = "https://space-facts.com/mars/"
    df = pd.read_html(table_url)[0]
    html_table = df.to_html().replace('\n', '')
    
    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html_hemispheres = browser.html
    soup = bs(html_hemispheres, 'html.parser')
    items = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    hemispheres_main_url = 'https://astrogeology.usgs.gov'
    for i in items: 
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(hemispheres_main_url + partial_img_url)
        partial_img_html = browser.html 
        soup = bs( partial_img_html, 'html.parser')
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    data = {
        "latest_title": latest_title,
        "latest_paragraph": latest_paragraph,
        "featured_image": featured_image,
        "html_table": html_table,
        "hemisphere_imgs": [hemisphere_image_urls]
    }
    return data

print(scrape())


### Mars Hemispheres

# Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
# Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
#Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.

