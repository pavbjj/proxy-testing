from flask import Flask, render_template, request

app = Flask(__name__)

# Function to calculate future value
def calculate_future_value(P, r, C, t):
    r = r / 100  # Convert interest rate to decimal
    return P * (1 + r)**t + (C * ((1 + r)**t - 1) / r)

@app.route('/')
def index():
    return render_template('index.html', form_data=None)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        P = float(request.form['principal'])
        r = float(request.form['rate'])
        C = float(request.form['contribution'])
        t = int(request.form['years'])
        final_amount = calculate_future_value(P, r, C, t)
        return render_template('result.html', amount=round(final_amount, 2), form_data=request.form)
    except ValueError:
        return "Invalid input. Please enter numeric values only.", 400

@app.route('/back', methods=['POST'])
def back_to_calculator():
    form_data = request.form
    return render_template('index.html', form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5551)

