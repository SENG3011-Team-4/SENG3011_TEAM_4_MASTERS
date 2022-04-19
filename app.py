import sys
from flask import Flask, render_template, request, url_for
#from PHASE_1.API_SourceCode.medicine import common_disease_search, location_medication
import requests
import json
from urllib.parse import urlencode


sys.path.insert(0, sys.path[0]+'\PHASE_1\API_SourceCode')

for path in sys.path:
    print(path)

from auth import auth_login_v1
from medicine import common_disease_search, location_medication, diseases_at_location, find_country
from vaccine_scraper import disease_prevention

app = Flask(__name__)

@app.route("/")
def home():
    diseases = diseases_at_location()
    return render_template('home.html', data=diseases)

@app.route("/dashboardSearch",  methods=["POST"])
def dashboardSearch():
    lat = request.form['lat']
    lng = request.form['lng']
    diseases = diseases_at_location()
    # match lat and lng to country
    country = find_country(int(lat), int(lng))
    country_info = next((item for item in diseases if item["country"] == country), None)
    diseases = country_info['diseases']
    for disease in diseases:
        prevention_info, vaccine_info = disease_prevention(disease)
        prevention_info_string = ''
        for string in prevention_info:
            prevention_info_string = prevention_info_string + string
        for string2 in vaccine_info:
            vaccine_info_string = vaccine_info_string + string_2
    response = requests.get('http://54.206.19.126/search/twitter', params={"location": country, "disease": "covid"})
    info = response.json()
    embed_code_string = ''
    for key in info:
        embed_code = get_embed_code(info[key]['url'])
        embed_code = embed_code.replace(';', '#')
        embed_code_string = embed_code_string + embed_code + '\n'
    print(embed_code_string)
    return render_template('home.html', data=diseases, tweets=info, ecs=embed_code_string)

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/authenticate", methods=["POST","GET"])
def authenticate():
    name = request.form['uname']
    password = request.form['psw']
    try:
        auth_login_v1(name, password)
        return render_template('home.html')
    except:
        print("Invalid Credentials")
        return render_template('login.html',info="Invalid Password")


@app.route("/healthcheck")
def healthCheck():
    r = requests.get('http://54.206.19.126/healthcheck')
    return render_template('healthcheck.html', data=r.text)

@app.route("/search")
def search():
    return render_template('search.html')

@app.route("/searchDisease", methods=["POST"])
def searchDisease():
    location = request.form['location']
    diseases = diseases_at_location([location])
    return render_template('report.html', data=location, content=diseases)

@app.route("/settings")
def settings():
    return render_template('settings.html')

@app.route("/report")
def report():
    return render_template('report.html')

def get_embed_code(url):
#url = 'https://twitter.com/jack/status/20'
    query_string = urlencode({'url': url}) # 'omit_script': 1
    oembed_url = f"https://publish.twitter.com/oembed?{query_string}"

    r = requests.get(oembed_url)
    if r.status_code == 200:
        result = r.json()
        html = result['html'].strip()
        
    return html

if __name__ == '__main__':
   app.run()