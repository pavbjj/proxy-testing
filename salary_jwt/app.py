from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Sample user credentials
USER_CREDENTIALS = {
    'username': 'admin',
    'password': 'password1234'
}

# Function to generate JWT token
def generate_token(username):
    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    payload = {
        'username': username,
        'exp': expiration_date
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

# Function to verify JWT token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated

# Login route to get JWT token
@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or auth.username != USER_CREDENTIALS['username'] or auth.password != USER_CREDENTIALS['password']:
        return jsonify({'message': 'Invalid credentials!'}), 401

    token = generate_token(auth.username)
    return jsonify({'token': token})

# Salary calculator route (protected with JWT token)
@app.route('/salary', methods=['POST'])
@token_required
def calculate_salary():
    data = request.get_json()

    if 'salary' not in data:
        return jsonify({'message': 'Salary parameter is missing!'}), 400

    salary = data['salary']
    # Perform salary calculation logic here (example: tax calculations, deductions, etc.)
    # For simplicity, let's assume a 20% tax rate
    tax_amount = 0.20 * salary
    net_salary = salary - tax_amount

    return jsonify({
        'gross_salary': salary,
        'tax_amount': tax_amount,
        'net_salary': net_salary
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8076)

