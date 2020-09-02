from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():

    b = init_browser()

    # Scrape news title and paragraph
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    b.visit(url)
    time.sleep(5)
    html = b.html
    soup = bs(html, "html.parser")
    a = soup.find('div', class_="list_text")
    t = a.find('div', class_="content_title").text  
    p = a.find('div', class_="article_teaser_body").text 

    #Scrapefeatured image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    b.visit(url)
    time.sleep(5)
    html = b.html
    soup = bs(html, 'html.parser')
    image =soup.find('img', class_="thumb")["src"]
    featured ="https://jpl.nasa.gov"+ image

    # Mars Facts Table
    url = "https://space-facts.com/mars/"
    b.visit(url)
    time.sleep(5)
    df = pd.read_html(url)[0]
    df.columns=['Mars','Data']
    html_table = df.to_html()
    html_table = html_table.replace('\n',' ')

    # Hemisphere Image Urls
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    b.visit(url)
    time.sleep(5)
    html_hemispheres = b.html
    soup = bs(html_hemispheres, 'html.parser')
    items = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    hemispheres_main_url = 'https://astrogeology.usgs.gov'
    for item in items: 
        title = item.find('h3').text
        partial_img_url = item.find('a', class_='itemLink product-item')['href']
        url = hemispheres_main_url + partial_img_url
        b.visit(url)
        partial_img_html = b.html
        soup = bs( partial_img_html, 'html.parser')
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
    # Store in dictionary
    mars_data = {}

    mars_data = {
    "News_Title": t,
    "News_Paragraph": p,
    "Featured_Image": featured,
    "Mars_Table": html_table,
    "Hemisphere_Data": hemisphere_image_urls
    }

    b.quit()

    return mars_data
