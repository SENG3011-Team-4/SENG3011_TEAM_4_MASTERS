import requests
from bs4 import BeautifulSoup

def county_scraper():
    countries = []

    url = 'https://www.cidrap.umn.edu/news-perspective'

    data = requests.get(url)
    html = BeautifulSoup(data.text, 'html.parser')

    country_list = html.select('ul.facetapi-facetapi-links.facetapi-facet-field-country li')

    for c in country_list:
        country = c.text
        country = country.split('(')
        countries.append(country[0].rstrip())
        
    return countries