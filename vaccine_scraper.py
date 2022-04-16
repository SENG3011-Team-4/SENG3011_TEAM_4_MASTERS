import requests
from bs4 import BeautifulSoup
from pprint import pprint

def disease_prevention(disease):
    prevention = []
    vaccine = []
    match disease:
        case "anthrax" | "anthrax cutaneous" | "anthrax gastrointestinous" | "anthrax inhalation":
            url = "https://www.cdc.gov/anthrax/prevention/index.html"
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            
            data = html.select('div.col-md-12 p')
            count = 0
            for p in data:
                p = p.text
                prevention.append(p)
                count += 1
                if count == 3:
                    break
                
            url = "https://www.cdc.gov/anthrax/prevention/antibiotics/index.html"
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            
            data = html.select('div.col-md-8 li')
            prevention.append("Two of the antibiotics that can be used to prevent anthrax are:")
            
            for link in data:
                link = link.text
                prevention.append(link)
                
            url = "https://www.cdc.gov/anthrax/prevention/vaccine/index.html"
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            
            data = html.select("div.card-body.bg-amber-t p")
            for p in data:
                p = p.text
                vaccine.append(p)    
                
            pprint(prevention)    
            pprint(vaccine)
                
                
        case "avian influenza" | "influenza a/h5n1" | "influenza a/h7n9" | "influenza a/h9n2" | "influenza a/h1n1" | "influenza a/h1n2" | "influenza a/h3n5" | "influenza a/h3n2" | "influenza a/h2n2":
            url = "https://wwwnc.cdc.gov/travel/diseases/avian-bird-flu" 
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            
            data = html.find('h3', id='whocangetbirdflu').findNext('p')
            for p in data:
                p = p.text 
                prevention.append(p)
            
            data = html.find('h3', id='whatcantravelersdotopreventbirdflu').findNext('p')
            vaccine.append(data.text)    
            
            data = html.find('h4', string='Avoid touching birds and visiting places where birds live').findNext('ul')
            for links in data:
                links = links.text
                if links != "\n":
                    prevention.append(links)      
            prevention.append("Flu antiviral drugs.")       
                   
            pprint(prevention)  
            pprint(vaccine)  
        case _:
            print("No data")        
            

disease_prevention("avian influenza") 
