from flask import Flask, make_response

app = Flask(__name__)

@app.route('/')
def hello():
    response = make_response("Hello, World!")
    response.set_cookie('my_cookie', 'Hello, Cookie!')
    response.headers['X-Custom-Header'] = 'Custom Value'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6666)

