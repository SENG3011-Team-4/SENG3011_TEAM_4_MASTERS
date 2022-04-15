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
            url = "https://www.cdc.gov/flu/avianflu/prevention.htm" 
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            
            prevention.append("It is recommended for people travelling to countries or states with bird flu outbreaks in poultry or people:")
            data = html.select("div.col-12.col-md-12 li")
            for link in data:
                link = link.text 
                prevention.append(link)
                   
            pprint(prevention)    
        case _:
            print("No data")        
            

disease_prevention("avian influenza") 