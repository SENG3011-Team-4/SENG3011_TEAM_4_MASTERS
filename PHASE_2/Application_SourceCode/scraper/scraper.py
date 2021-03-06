import requests
from bs4 import BeautifulSoup
from pprint import pprint
from country_scraper import county_scraper
import json

# CIDRAP doesn't have syndromes in articles -> need to input them manually
f1 = open('syndrome_list.json')
f2 = open('disease_list.json')
f3 = open('world-cities_json.json')
syndrome_list = json.load(f1)
disease_list = json.load(f2)
cities_list = json.load(f3)

countries = county_scraper()

# Getting cities from JSON file
# Excluding cities from countries not in countries list
cities = []
for c in cities_list:
    if c['country'] in countries:
        cities.append(c['name'])

web_data = []


# Some diseases have multiple syndromes
def identify_syndrome(disease_list):
    syndromes = []
    for d in disease_list:
        if d == "malaria" or d == "measles" or d == "rabies" or d == "poliomyelitis" or d == "zika" or d == "west nile virus" or d == "chikungunya" or d == "enterovirus 71 infection":
            syndromes.append("Encephalitis") 
        if "influenza" in d:
            syndromes.append("Influenza-like illness")    
        if d == "sars" or d == "COVID-19" or d == "pneumococcus pneumonia":
            syndromes.append("Acute respiratory syndrome")   
        if d == "poliomyelitis" or d == "botulism" or d == "west nile virus" or d == "diphtheria":
            syndromes.append("Acute Flaccid Paralysis")
        if d == "cryptococcosis" or d == "tuberculosis" or d == "poliomyelitis" or d == "hiv/aids" or d == "enterovirus 71 infection" or d == "varicella" or d == "mumps":
            syndromes.append("Meningitis")    
        if "haemorrhagic fever" in d or d == "chikungunya" or d == "lassa fever" or d == "rift valley fever" or d == "marburg virus disease" or d == "hantavirus" or d == "dengue" or d == "yellow fever":
            syndromes.append("Haemorrhagic Fever") 
        if d == "rotavirus infection" or d == "norovirus infection" or d == "salmonellosis" or d == "shigellosis" or d == "cholera":
            syndromes.append("Acute gastroenteritis")
        if "heptatitis" in d or d == "rubella" or d == "dengue" or d == "ehec (e.coli)" or d == "shigellosis" or d == "rubella" or d == "varicella":
            syndromes.append("Acute fever and rash")       
    syndromes = list(set(syndromes))        
    return syndromes        
                           
                

def month_to_num(mon):
    return {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }[mon]

def disease_shorthand(disease):
    match disease:
        case "anthrax":
            return "anthrax cutaneous" # Theres 3 different anthrax diseases idk how to differentiate
        case "Avian Influenza (Bird Flu)":
            return "influenza a/h5n1" # Theres 8 different bird flus
        case "E coli":
            return "ehec (e.coli)"
        case "Ebola":
            return "ebola haemorrhagic fever"
        case "Enterovirus, Non-Polio":
            return "enterovirus 71 infection" # Enterovirus is more an umbrella disease
        case "Food-and-Mouth Disease":
            return "hand, foot and mouth disease"
        case "H1N1 2009 Pandemic Influenza":
            return "influenza a/h1n1"
        case "H3N2v Influenza":
            return "influenza a/h3n2"
        case "H7N9 Avian Influenza":
            return "influenza a/h7n9"
        case "Influenza, General":
            return "influenza"
        case "Legionella":
            return "legionares"
        case "Listeria":
            return "listeriosis"
        case "Marburg":
            return "marburg virus disease"
        case "Norovirus":
            return "norovirus infection"
        case "Pneumonia":
            return "pneumococcus pneumonia" # Technically ranges from ear to lungs whereas regular pneumonia is particular to lungs
        case "Polio":
            return "poliomyelitis"
        case "Rotavirus":
            return "rotavirus infection"
        case "Salmonella":
            return "salmonellosis"
        case "West Nile":
            return "west nile virus"
        case _:
            return disease

# Scraping first 10 pages
# Final possible page: 1481
# First page starts at 0
# For testing, using only 1 page for faster results
# Scrape articles only
page_num = 0
while page_num != 1:
    url = 'https://www.cidrap.umn.edu/news-perspective?f%5B0%5D=type%3Ass_news&page='+str(page_num)

    data = requests.get(url)
    html = BeautifulSoup(data.text, 'html.parser')

    articles = html.select('div.views-rows')


    for article in articles:
        sub_art = article.select('div.views-field.views-field-rendered-entity')
        for sub in sub_art:
            
            reports = []
            
            # fetching and formatting date
            date = sub.select_one('.date-display-single').text
            date = date.split()
            date[1] = date[1].replace(",","")
            date[0] = month_to_num(date[0])
            date = date[2]+"-"+date[0]+"-"+date[1]+"T:00:00:00"
            
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
            country = []
            city = []
            for p in art_para:
                p = p.text
                # United States written as US in most articles
                if "US" in p:
                    if "United States" not in country:
                        country.append("United States")              
                for c in countries:
                    if c in p:
                        if c not in country:
                            country.append(c)
                for c in cities:
                    if c in p:
                        if c not in city:
                            city.append(c)                         
            locations.append({"country": country, "cities": city})        
            
            #event date
            #syndrome
            
            # Scraping the diseases mentioned in the article
            filed_under = report.select_one('div.fieldlayout-inline.fieldlayout.node-field-filed_under')
            diseases_filed = filed_under.select('div.field-items')
            diseases = []
            for d in diseases_filed:
                disease = disease_shorthand(d.select_one('.field-item.even a').text)
                if disease.lower() in disease_list:
                    diseases.append(disease)    
                
            syndromes = identify_syndrome(diseases)    
            reports.append({"disease": diseases, "syndrome": syndromes, "locations": locations})
            
            
            
            # Main texts -> scraping text under url link for articles
            main_text = sub.select_one('.field-item.even p').text   
                      
            headline = sub.select_one('.node-title.fieldlayout.node-field-title a').text                      
            web_data.append({"url": art_url, "date_of_publication": date, "headline": headline, "main_text": main_text, "report": reports})
            
    page_num += 1        

pprint(web_data)
f1.close()
f2.close()
f3.close()
