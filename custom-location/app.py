from flask import Flask, redirect

app = Flask(__name__)

@app.route('/set-location', methods=['GET'])
def set_location():
    # Set the desired location manually
    desired_location = "https://example.com"

    # Return a response with the Location header
    response = redirect(desired_location)
    return response

@app.route('/')
def home():
    return "Welcome to the Flask app! Use /set-location to test the location header."

if __name__ == '__main__':
    app.run(debug=True, port=5099)

