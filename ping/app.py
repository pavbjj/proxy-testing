from flask import Flask, render_template

app = Flask(__name__)

@app.route('/healthcheck/')
def healthcheck():
    return 'OK', 200

@app.route('/healthcheck/ping.html')
def ping():
    return render_template('ping.html')

if __name__ == '__main__':
    app.run(debug=True, port="65432", host="0.0.0.0")

