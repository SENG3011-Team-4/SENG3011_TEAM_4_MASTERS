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
            prevention.append(data.text)
            
            data = html.find('h3', id='whatcantravelersdotopreventbirdflu').findNext('p')
            vaccine.append(data.text)    
            
            data = html.find('h4', string='Avoid touching birds and visiting places where birds live').findNext('li')
            count = 0
            while count < 3:
                prevention.append(data.text)
                data = data.findNext('li')
                count += 1     
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
            
            points = data.findNext('li')
            count = 0 
            while count < 4:
                prevention.append(points.text)
                count += 1
                points = points.findNext('li')
                    
            data = html.find('h2', id='mask')
            prevention.append(data.findNext('p').text) 
            
            data = html.find('h2', id='vaccination')
            vaccine.append(data.findNext('p').text)
            vaccine.append(data.findNext('p').findNext('p').text)       
            
            data = html.find('h2', id='distancing')
            prevention.append(data.findNext('p').findNext('p').text)
            points = data.findNext('li')
            count = 0
            while count < 5:
                prevention.append(points.text)
                count += 1
                points = points.findNext('li')
            
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
            points = data.findNext('li')
            count = 0
            while count < 3:
                vaccine.append(points.text)
                points = points.findNext('li')
                count += 1
                    
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
            count = 0
            while count < 5:
                prevention.append(points.text)
                points = points.findNext('li')
                count += 1

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
            count = 0
            while count < 3:
                prevention.append(points.text)
                points = points.findNext('li')
                count += 1
                    
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
            points = data.findNext('li')
            count = 0
            while count < 3:
                prevention.append(points.text)
                points = points.findNext('li')
                count += 1
                    
            data = html.find('h2', id='treated').findNext('p')
            count = 0
            while count < 4:
                prevention.append(data.text)
                count += 1
                data = data.findNext('p')
                    
            
            vaccine.append("No vaccine")
            pprint(prevention)
            pprint(vaccine)   
            
        case "influenza":
            url = "https://www.healthdirect.gov.au/flu"
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            
            data = html.find('h2', id='treatment')
            prevention.append(data.findNext('p').text)
            prevention.append(data.findNext('p').findNext('p').text)
            
            points = data.findNext('li')
            count = 0
            while count < 6:
                prevention.append(points.text)
                points = points.findNext('li')
                count += 1
                    
            data = html.find('h2', id='prevention').findNext('p')
            count = 0
            while count < 2:
                vaccine.append(data.text)
                data = data.findNext('p')
                count += 1
                
            count = 0
            while count < 2:
                prevention.append(data.text)
                data = data.findNext('p')
                count += 1    
                    
            data = html.find('h2', id='vaccine')
            vaccine.append(data.findNext('p').text)        
                         
            pprint(prevention)
            pprint(vaccine)             
                       
        case "measles":
            url = "https://www.healthdirect.gov.au/measles"
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            
            data = html.find('h2', id='prevented').findNext('p')
            count = 0
            while count < 3:
                vaccine.append(data.text)
                data = data.findNext('p')
                count += 1       
                
            vaccine.append(data.findNext('p').findNext('p').text) 
            vaccine.append(data.findNext('p').findNext('p').findNext('p').text)                           
        
            data = html.find('h2', id='treated')
            prevention.append(data.findNext('p').text)
            prevention.append(data.findNext('p').findNext('p').text)
            points = data.findNext('li')
            count = 0
            while count < 3:
                prevention.append(points.text)
                points = points.findNext('li')
                count += 1
            
            prevention.append(data.findNext('p').findNext('p').findNext('p').text)        
        
            pprint(prevention)   
            pprint(vaccine)    
               
        case "ebola haemorrhagic fever":
            url = "https://www.healthdirect.gov.au/ebola-virus"
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            
            data = html.find('h2', id='risk').findNext('p')
            prevention.append(data.text)
            prevention.append(data.findNext('p').text)
            prevention.append(data.findNext('p').findNext('p').text)
            
            data = html.find('h2', id='diagnosed').findNext('p').findNext('p')
            vaccine.append(data.findNext('p').text)
            vaccine.append(data.findNext('p').findNext('p').text)
            
            
            pprint(prevention)
            pprint(vaccine)
                       
        case "sars":
            url = "https://www.healthdirect.gov.au/severe-acute-respiratory-syndrome-sars"
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            
            data = html.find('h2', id='prevent')
            vaccine.append(data.findNext('p').text)
            prevention.append(data.findNext('p').findNext('p').text)
            prevention.append(data.findNext('p').findNext('p').findNext('p').text)
            points = data.findNext('li')
            count = 0
            while count < 5:
                prevention.append(points.text)
                points = points.findNext('li')
                count += 1
                    
            data = html.find('h2', id='treatment')
            prevention.append(data.findNext('p').text)        
            
            pprint(prevention)
            pprint(vaccine)    
                       
        case "meningitis":
            url = "https://www.healthdirect.gov.au/meningitis"
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            
            data = html.find('h2', id='prevented')
            prevention.append(data.findNext('p').text)
            points = data.findNext('li')
            count = 0
            while count < 4:
                prevention.append(points.text)
                points = points.findNext('li')
                count += 1
            prevention.append(data.findNext('p').findNext('p').text) 
            
            data = html.find('h3', string='Meningococcal vaccine')
            vaccine.append(data.findNext('p').text)       
            points = data.findNext('li')
            count = 0
            while count < 8:
                vaccine.append(points.text)
                points = points.findNext('li')
                count += 1        
            
            pprint(prevention)
            pprint(vaccine)        
        
        case "dengue":
            url = "https://www.healthdirect.gov.au/dengue-fever"
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            
            data = html.find('h2', id='prevented')
            prevention.append(data.findNext('p').text)
            prevention.append(data.findNext('p').findNext('p').text)
            
            points = data.findNext('li')
            count = 0
            while count < 5:
                prevention.append(points.text)
                points = points.findNext('li')
                count += 1
                
            vaccine.append("There is no vaccine to prevent dengue fever.")   
            
            pprint(prevention)
            pprint(vaccine)                
            
        case "rotavirus":
            url = "https://www.healthdirect.gov.au/rotavirus"
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            
            data = html.find('h3', string="Rotavirus vaccine")  
            prevention.append(data.findNext('p').findNext('p').text)
            points = data.findNext('li')
            count = 0
            while count < 5:
                prevention.append(points.text)
                points = points.findNext('li')
                count += 1
                
            data = html.find('h2', id='prevented')
            vaccine.append(data.findNext('p').text)
            
            pprint(prevention)
            pprint(vaccine)      
                       
        case "cholera":
            url = "https://www.healthdirect.gov.au/cholera"   
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            
            data = html.find('h2', id='prevented').findNext('p')
            count = 0
            while count < 4:
                prevention.append(data.text)
                data = data.findNext('p')
                count += 1
            vaccine.append(data.text)
            vaccine.append(data.findNext('p').text) 
            
            pprint(prevention)
            pprint(vaccine)           
            
        case "botulism":
            url = "https://www.healthdirect.gov.au/botulism"
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            
            data = html.find('h2', string='Botulism prevention')
            prevention.append(data.findNext('p').text)
            points = data.findNext('li')
            count = 0
            while count < 5:
                prevention.append(points.text)
                points = points.findNext('li')
                count += 1
            vaccine.append("There is no vaccine for botulism.")    
            pprint(prevention)
            pprint(vaccine)             
                       
        case _:
            pprint(prevention)
            pprint(vaccine)        
            
    return (prevention, vaccine)

#disease_prevention("influenza a/h5n1")