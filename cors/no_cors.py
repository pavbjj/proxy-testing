from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, CORS Test!"

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'This is sample data from the API.'}
    return jsonify(data)

@app.route('/api/post', methods=['POST'])
def post_data():
    request_data = request.get_json()
    return jsonify(request_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6666)

