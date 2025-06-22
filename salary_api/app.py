from flask import Flask, jsonify
from flask import request
import requests

app = Flask(__name__)

# Routes for interacting with microservices

@app.route('/calculate_salary', methods=['POST'])
def calculate_salary():
    data = request.get_json()
    response = requests.post('http://localhost:5001/calculate', json=data)
    return response.json(), response.status_code

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response = requests.post('http://localhost:5002/login', json=data)
    return response.json(), response.status_code

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    response = requests.post('http://localhost:5002/signup', json=data)
    return response.json(), response.status_code

if __name__ == '__main__':
    app.run(debug=True)

