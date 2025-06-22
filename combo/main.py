import os
from flask import Flask, redirect, request, jsonify

app = Flask(__name__)
url = os.environ.get('URL', 'http://ccie.pl')


@app.route('/')
def main():
    return "Usage: Paths '/headers', '/redirect', '/status'"


@app.route('/headers')
def headers():
    return dict(request.headers)


@app.route('/redirect')
def redirect_request():
    return redirect(url, code=302)


@app.route('/status')
def random_status_code():
    if 'code' in request.headers:
        try:
            codes = request.headers['code']
            data = {'F5 response code': codes}
            return jsonify(data), codes
        except:
            error_msg = {'error': 'bad request'}
            return jsonify(error_msg)
    else:
        error_msg = {'error': 'bad request'}
        return jsonify(error_msg)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5100.
    port = int(os.environ.get('PORT', 5100))
    app.run(host='0.0.0.0', port=port)
