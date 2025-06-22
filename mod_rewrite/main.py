from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/wps-portal/news')
def news():
   return render_template('news.html')

@app.route('/wps-portal/create')
def create():
   return render_template('create.html')

app.run(host='0.0.0.0', port=81)
