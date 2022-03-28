from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/healthcheck")
def healthCheck():
    return render_template('healthcheck.html')

@app.route("/search")
def search():
    return render_template('search.html')

if __name__ == '__main__':
   app.run()