from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)

# Secret key for session management (required for flash messages)
app.secret_key = 'your_secret_key'

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('database.db')
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

    conn.commit()
    conn.close()

# Route to view contacts in the admin panel
@app.route('/admin/contacts')
def view_contacts():
    conn = get_db_connection()
    contacts = conn.execute('SELECT * FROM contacts').fetchall()
    conn.close()
    return render_template('contacts.html', contacts=contacts)

# Route to view applications in the admin panel
@app.route('/admin/applications')
def view_applications():
    conn = get_db_connection()
    applications = conn.execute('SELECT * FROM applications').fetchall()
    conn.close()
    return render_template('applications.html', applications=applications)

# Route to edit an application
@app.route('/admin/edit_application/<int:id>', methods=['GET', 'POST'])
def edit_application(id):
    conn = get_db_connection()
    application = conn.execute('SELECT * FROM applications WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        county = request.form['county']
        course = request.form['course']

        conn.execute('UPDATE applications SET first_name = ?, last_name = ?, email = ?, phone = ?, gender = ?, county = ?, course = ? WHERE id = ?',
                     (first_name, last_name, email, phone, gender, county, course, id))
        conn.commit()
        conn.close()

        flash('Application updated successfully!', 'success')
        return redirect(url_for('view_applications'))

    conn.close()
    return render_template('edit_application.html', application=application)

# Route to delete an application
@app.route('/admin/delete_application/<int:id>', methods=['POST'])
def delete_application(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM applications WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Application deleted successfully!', 'success')
    return redirect(url_for('view_applications'))

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# About Us page route
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
        try:
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

            flash('Contact form submitted successfully!', 'success')

        except Exception as e:
            flash(f'Error: {e}', 'danger')

        # After saving the form data, redirect to the contact page with a success message
        return redirect(url_for('contact'))

    return render_template('contact.html')

# Apply page route with POST method to handle form submission
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        try:
            # Check if the request is JSON
            if request.is_json:
                data = request.get_json()
                first_name = data['firstName']
                last_name = data['lastName']
                email = data['email']
                phone = data['phone']
                gender = data['gender']
                county = data['county']
                course = data['course']
            else:
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

            flash('Application form submitted successfully!', 'success')

            return {"message": "Application submitted successfully!"}, 200

        except Exception as e:
            flash(f'Error: {e}', 'danger')
            return {"message": str(e)}, 500

    return render_template('apply.html')

# Initialize the database and run the app
if __name__ == '__main__':
    init_db()  # Initialize the database and create tables if they don't exist
    app.run(debug=True, port=5001)  # Change the port to 5001

