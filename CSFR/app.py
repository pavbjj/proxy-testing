from flask import Flask, render_template, request, redirect, url_for, session, flash

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

users = [
    {'username': 'user1', 'password': generate_password_hash('password1')},
    {'username': 'user2', 'password': generate_password_hash('password2')}
]

@app.route('/')
def index():
    return 'Welcome to the Flask User Management App!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = next((user for user in users if user['username'] == username), None)

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f'Welcome to the dashboard, {session["username"]}! <a href="/logout">Logout</a> | <a href="/delete">Delete Account</a>'
    else:
        flash('You need to login first', 'warning')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/delete', methods=['GET', 'POST'])
def delete_account():
    if 'username' in session:
        if request.method == 'POST':
            username = session['username']
            users[:] = [user for user in users if user['username'] != username]
            session.pop('username', None)
            flash('Account deleted successfully', 'success')
            return redirect(url_for('login'))
        return render_template('delete.html')
    else:
        flash('You need to login first', 'warning')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5544)

