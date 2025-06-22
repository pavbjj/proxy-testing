from flask import Flask, render_template, request

app = Flask(__name__)

# Path: /uk-lower/admin
@app.route('/uk-lower/admin', methods=['GET', 'POST'])
def uk_lower_admin():
    if request.method == 'GET':
        # Render random HTML for GET request
        return render_template('uk_lower_admin_get.html')
    elif request.method == 'POST':
        # Handle file upload for POST request
        if 'file' in request.files:
            file = request.files['file']
            file.save(f'uploads/{file.filename}')
            return 'File uploaded successfully!'
        else:
            return 'No file in the request.'

# Path: /us-prod/test
@app.route('/us-prod/test', methods=['GET', 'POST'])
def us_prod_test():
    if request.method == 'GET':
        # Render random HTML for GET request
        return render_template('us_prod_test_get.html')
    elif request.method == 'POST':
        # Handle file upload for POST request
        if 'file' in request.files:
            file = request.files['file']
            file.save(f'uploads/{file.filename}')
            return 'File uploaded successfully!'
        else:
            return 'No file in the request.'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5633)

