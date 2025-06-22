import os
import time
from flask import Flask, redirect

app = Flask(__name__)
url=os.environ['URL']
url2=os.environ['URL2']

@app.route('/')
def hello():
    time.sleep(60)
    return redirect(url, code=302)

@app.route('/test')
def hello2():
    return redirect(url2, code=302)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
