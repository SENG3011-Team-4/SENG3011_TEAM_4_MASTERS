import requests
from bs4 import BeautifulSoup
from pprint import pprint

web_data = []

# Scraping first 10 pages
count = 0
while count != 10:
    url = 'https://www.cidrap.umn.edu/news-perspective?page='+str(count)

    data = requests.get(url)
    html = BeautifulSoup(data.text, 'html.parser')

    articles = html.select('div.views-rows')


    for article in articles:
        sub_art = article.select('div.views-field.views-field-rendered-entity')
        for sub in sub_art:
            date = sub.select_one('.date-display-single').text
            url = "cidrap.umn.edu"+ sub.select_one('.node-title.fieldlayout.node-field-title a')['href']     
            headline = sub.select_one('.node-title.fieldlayout.node-field-title a').text                      
            web_data.append({"url": url, "date": date, "headline": headline})
            
    count += 1        

pprint(web_data)