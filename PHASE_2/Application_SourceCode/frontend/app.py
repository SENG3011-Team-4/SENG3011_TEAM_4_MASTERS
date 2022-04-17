import sys
from flask import Flask, render_template, request, url_for
from PHASE_1.API_SourceCode.medicine import common_disease_search, location_medication
import requests

sys.path.insert(0, sys.path[0]+'\PHASE_1\API_SourceCode')

for path in sys.path:
    print(path)

from auth import auth_login_v1
from medicine import common_disease_search, location_medication

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

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
    #exec(open("./PHASE_1/medicine.py").read())
    return render_template('search.html')

@app.route("/settings")
def settings():
    return render_template('settings.html')

@app.route("/report")
def report():
    return render_template('report.html')

if __name__ == '__main__':
   app.run()