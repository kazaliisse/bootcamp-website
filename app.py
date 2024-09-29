from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('database.db')  # Update the path if needed
    conn.row_factory = sqlite3.Row
    return conn

# Function to initialize the database and create tables
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create contacts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            reason TEXT NOT NULL
        )
    ''')

    # Create applications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            gender TEXT NOT NULL,
            county TEXT NOT NULL,
            course TEXT NOT NULL
        )
    ''')

    conn.commit()  # Commit the changes
    conn.close()  # Close the connection

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# About page route
@app.route('/about')
def about():
    return render_template('AboutUs.html')

# Courses page route
@app.route('/courses')
def courses():
    return render_template('courses.html')

# Mentors page route
@app.route('/mentors')
def mentors():
    return render_template('mentors.html')

# Contact Us page route with POST method to handle form submission
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email = request.form['email']
        phone = request.form['phone']
        reason = request.form['reason']

        # Connect to the database and save the form data
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (first_name, last_name, email, phone, reason) VALUES (?, ?, ?, ?, ?)",
                       (first_name, last_name, email, phone, reason))
        conn.commit()
        conn.close()

        # After saving the form data, redirect to a success page or back to the contact page
        return redirect(url_for('contact'))

    return render_template('contact.html')

# Apply page route with POST method to handle form submission
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        try:
            first_name = request.form['first-name']
            last_name = request.form['last-name']
            email = request.form['email']
            phone = request.form['phone']
            gender = request.form['gender']
            county = request.form['county']
            course = request.form['course']

            # Connect to the database and save the application data
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO applications (first_name, last_name, email, phone, gender, county, course) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (first_name, last_name, email, phone, gender, county, course))
            conn.commit()
            conn.close()

            # After saving the form data, redirect to a success page or back to the apply page
            return redirect(url_for('apply'))  # You could redirect to a success page if desired

        except Exception as e:
            print(f"Error: {e}")  # Log the error to console

    return render_template('apply.html')

if __name__ == '__main__':
    init_db()  # Initialize the database and create tables if they don't exist
    app.run(debug=True)
