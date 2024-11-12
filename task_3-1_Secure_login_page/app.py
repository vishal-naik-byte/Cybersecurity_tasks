from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Dummy user data for example purposes
USER_CREDENTIALS = {
    'username': 'user',
    'password': 'password123'  # In production, use a secure way to store passwords
}

@app.route('/')
def home():
    return "Welcome to the Home Page!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Basic authentication check
        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            flash("Login Successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid Credentials", "danger")
            return redirect(url_for('login'))
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
