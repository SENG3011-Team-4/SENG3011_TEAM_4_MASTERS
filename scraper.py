import requests
from bs4 import BeautifulSoup
from pprint import pprint
import pycountry

web_data = []

# Scraping first 10 pages
# First page starts at 0
# For testing, using only 1 page for faster results
page_num = 0
while page_num != 1:
    url = 'https://www.cidrap.umn.edu/news-perspective?page='+str(page_num)

    data = requests.get(url)
    html = BeautifulSoup(data.text, 'html.parser')

    articles = html.select('div.views-rows')


    for article in articles:
        sub_art = article.select('div.views-field.views-field-rendered-entity')
        for sub in sub_art:
            
            reports = []
            
            date = sub.select_one('.date-display-single').text
            art_url = "http://cidrap.umn.edu"+ sub.select_one('.node-title.fieldlayout.node-field-title a')['href']  
            
            # Opening article to be scraped
            art_data = requests.get(art_url)
            art_html = BeautifulSoup(art_data.text, 'html.parser')
            
            report = art_html.select_one('div.node-inner')
            
            # Getting each paragraph in the article
            art_start = art_html.select_one('div.field.field-name-field-body.field-type-text-long.field-label-hidden')
            art_para = art_start.select('div.field-item.even p')
            
            # TODO Fix up location -> some countries not included + add cities
            locations = []
            for p in art_para:
                p = p.text
                # United States written as US in most articles
                if "US" in p:
                    if "United States" not in locations:
                        locations.append("United States")
                for c in pycountry.countries:
                    if c.name in p:
                        if c.name not in locations:
                            locations.append(c.name)             
                        
            
            #event date
            #syndrome
            
            # Scraping the diseases mentioned in the article
            filed_under = report.select_one('div.fieldlayout-inline.fieldlayout.node-field-filed_under')
            diseases_filed = filed_under.select('div.field-items')
            diseases = []
            for d in diseases_filed:
                disease = d.select_one('.field-item.even a').text
                diseases.append(disease)    
                
            reports.append({"disease": diseases, "locations": locations})
            
            
            #TO FIX - Scans with dot points as main texts 
            try:
                main_text = sub.select_one('.field-item.even p').text   
            except AttributeError:
                main_text = "None"  
            
            headline = sub.select_one('.node-title.fieldlayout.node-field-title a').text                      
            web_data.append({"url": art_url, "date_of_publication": date, "headline": headline, "main_text": main_text, "report": reports})
            
    page_num += 1        

pprint(web_data)