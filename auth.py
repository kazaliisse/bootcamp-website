from flask import Flask, Blueprint, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from flask_mail import Mail, Message
import os
import random
import string
import hashlib

# Initialize the blueprint
auth = Blueprint('auth', __name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'noorhafowbare@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'qjmnwlgthsskjbwy'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'noorhafowbare@gmail.com'  # Replace with your email
mail = Mail(app) 


# Database helper functions
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route for login
@auth.route('/login', methods=['GET', 'POST'])  # Ensure both GET and POST are allowed
def login():
    if request.method == 'POST':  # Handle POST request
        data = request.get_json()  # Get the JSON data from the request
        email = data.get('email')
        password = data.get('password')

        # Check if email and password are provided
        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required."}), 400

        # Query the database for the user
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        # Verify the user's password
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']  # Store user_id in session
            return jsonify({"success": True, "message": "Login successful"})
        
        return jsonify({"success": False, "message": "Invalid credentials."}), 401

    return render_template('auth.html')  # Handle GET request and render login page

@auth.route('/logout')
def logout():
    session.pop('user_id', None)  # Clear the session
    return redirect(url_for('auth.login'))  # Redirect to login page

# Route for sign-up
@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    # Check if email already exists in the database
    conn = get_db_connection()
    existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    if existing_user:
        return jsonify({"success": False, "message": "Email already exists."}), 409  # Conflict error

    # Hash the password before storing
    hashed_password = generate_password_hash(password)

    # Insert new user into the database
    conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed_password))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "User successfully created"})

# Route for checking login status (optional)
@auth.route('/status', methods=['GET'])
def status():
    if 'user_id' in session:
        return jsonify({"success": True, "message": "Logged in"})
    return jsonify({"success": False, "message": "Not logged in"})


# Register the blueprint for auth routes
app.register_blueprint(auth, url_prefix='/auth')

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5001)
