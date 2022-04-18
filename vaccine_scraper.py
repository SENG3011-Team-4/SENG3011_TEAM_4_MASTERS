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
        
        case "zika":
            url = "https://www.cdc.gov/zika/prevention/index.html"    
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            
            data = html.select("div.col-md-12.splash-col ul")
            for p in data:
                p = p.text
                l = p.split("\n")
                l = l[1:-1]
                count = 0
                for points in l:
                    if count > 4:
                        break 
                    elif count < 4:
                        prevention.append(points)
                    else:
                        vaccine.append(points)   
                    count += 1     
            
            pprint(prevention)
            pprint(vaccine)
            
        case "covid-19":
            url = "https://www.healthdirect.gov.au/covid-19/how-to-avoid-covid-19"
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            
            data = html.find('h2', id='hygiene')
            prevention.append(data.findNext('p').text)
            prevention.append(data.findNext('p').findNext('p').text)
            
            points = data.findNext('ul')
            for links in points:
                links = links.text
                if links != '\n':
                    prevention.append(links)
                    
            data = html.find('h2', id='mask')
            prevention.append(data.findNext('p').text) 
            
            data = html.find('h2', id='vaccination')
            vaccine.append(data.findNext('p').text)
            vaccine.append(data.findNext('p').findNext('p').text)       
            
            data = html.find('h2', id='distancing')
            prevention.append(data.findNext('p').findNext('p').text)
            points = data.findNext('ul')
            for links in points:
                links = links.text
                if links != '\n' and links != " ":
                    prevention.append(links)
            
            pprint(prevention)
            pprint(vaccine)
            
        case "human papillomavirus (hpv)":
            url = "https://www.healthdirect.gov.au/human-papillomavirus-hpv-vaccine"
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')   
            
            data = html.find('h2', id='prevented')
            prevention.append(data.findNext('p').text)
            prevention.append(data.findNext('p').findNext('p').text)
            prevention.append(data.findNext('p').findNext('p').findNext('p').text)
            
            para = data.findNext('p').findNext('p').findNext('p')
            vaccine.append(para.findNext('p').text)
            points = data.findNext('ul')
            for links in points:
                links = links.text
                if links != '\n' and links != " ":
                    vaccine.append(links)
                    
            data = html.find('h2', id='treated')
            prevention.append(data.findNext('p').text)    
            prevention.append(data.findNext('p').findNext('p').text)
            prevention.append(data.findNext('p').findNext('p').findNext('p').text)    
            
            pprint(prevention)
            pprint(vaccine)
                       
        case "chikungunya":
            url = "https://www.healthdirect.gov.au/chikungunya-virus"        
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')       
            
            data = html.find('h2', id='diagnosed-treated').findNext('p')
            prevention.append(data.text)
            prevention.append(data.findNext('p').text)
            prevention.append(data.findNext('p').findNext('p').text)
            prevention.append(data.findNext('p').findNext('p').findNext('p').text)
            
            data = html.find('h2', id='prevented')
            prevention.append(data.findNext('p').text)
            points = data.findNext('ul')
            for links in points:
                links = links.text
                if links != '\n' and links != " ":
                    prevention.append(links)

            vaccine.append("There is no vaccine to prevent chikungunya.")
            
            pprint(prevention)
            pprint(vaccine)
            
        case "tuberculosis":
            url = "https://www.healthdirect.gov.au/tuberculosis"
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            
            data = html.find('h2', id='spread')
            prevention.append(data.findNext('p').text)
            
            data = html.find('h2', id='treated') 
            para = data.findNext('p')
            count = 0
            while count < 5:
                prevention.append(para.text)
                count += 1
                para = para.findNext('p')
                
            points = data.findNext('ul')
            for links in points:
                links = links.text
                if links != "\n" and links != " ":
                    prevention.append(links)
                    
            data = html.find('h2', id='prevented')
            vaccine.append(data.findNext('p').text)    
            vaccine.append(data.findNext('ul').findNext('p').text)        
               
            pprint(prevention)
            pprint(vaccine)   
            
        case "salmonella":
            url = "https://www.healthdirect.gov.au/salmonella" 
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            
            data = html.find('h2', id='prevented')
            prevention.append(data.findNext('p').text)
            points = data.findNext('ul')
            for links in points:
                links = links.text
                if links != "\n" and links != " ":
                    prevention.append(links)
                    
            data = html.find('h2', id='treated').findNext('p')
            count = 0
            while count < 4:
                prevention.append(data.text)
                count += 1
                data = data.findNext('p')
                    
            
            vaccine.append("No vaccine")
            pprint(prevention)
            pprint(vaccine)   
                       
        case _:
            print("No data")        
            
disease_prevention("salmonella") 
