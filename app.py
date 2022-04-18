from flask import Flask, render_template
#from PHASE_1.API_SourceCode.medicine import common_disease_search, location_medication
import requests

app = Flask(__name__)

@app.route("/")
def home():
    example = {
        "location": "Australia",
        "disease": ["COVID-19", "Influenza"]
    }
    return render_template('home.html', data=example)

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/healthcheck")
def healthCheck():
    r = requests.get('http://54.206.19.126/healthcheck')
    return render_template('healthcheck.html', data=r.text)

@app.route("/search")
def search():
    return render_template('search.html')

@app.route("/settings")
def settings():
    return render_template('settings.html')

@app.route("/report")
def report():
    return render_template('report.html')

if __name__ == '__main__':
   app.run()