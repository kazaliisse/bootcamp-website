from flask import Flask, render_template, request, redirect, url_for, flash

from flask_mail import Mail, Message  # Importing Flask-Mail
import sqlite3

app = Flask(__name__)

# Secret key for session management (required for flash messages)
app.secret_key = '64f6c772360b516a3807929b92468124af4aa4ba4ab61cdd3b1f18e46e194457'

#open

#close

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # or your preferred SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'noorhafowbare@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'qjmnwlgthsskjbwy'  # Replace with your app password

# Initialize Mail
mail = Mail(app)


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

    # Function to send confirmation email
def send_confirmation_email(email, first_name):
    try:
        msg = Message(
            'Congratulations on Your Admission!',
            sender='noorhafowbare@gmail.com',  # Your email address
            recipients=[email]
        )
        msg.body = f"Hello {first_name},\n\nCongratulations! Your admission application has been received successfully. We are excited to have you join us.\n\nBest regards,\nThe Team"
        mail.send(msg)
        print("Confirmation email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Route to view contacts in the admin panel with pagination
@app.route('/admin/contacts')
def view_contacts():
    search = request.args.get('search', '')  # Search functionality
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of records per page
    offset = (page - 1) * per_page

    conn = get_db_connection()
    query = 'SELECT * FROM contacts WHERE first_name LIKE ? OR last_name LIKE ? LIMIT ? OFFSET ?'
    search_param = f"%{search}%"
    contacts = conn.execute(query, (search_param, search_param, per_page, offset)).fetchall()

    # Get total number of contacts for pagination
    total_query = 'SELECT COUNT(*) FROM contacts WHERE first_name LIKE ? OR last_name LIKE ?'
    total = conn.execute(total_query, (search_param, search_param)).fetchone()[0]
    conn.close()

    return render_template('contacts.html', contacts=contacts, page=page, per_page=per_page, total=total)

# Route to edit a contact
@app.route('/admin/edit_contact/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    conn = get_db_connection()
    contact = conn.execute('SELECT * FROM contacts WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email = request.form['email']
        phone = request.form['phone']
        reason = request.form['reason']

        conn.execute('UPDATE contacts SET first_name = ?, last_name = ?, email = ?, phone = ?, reason = ? WHERE id = ?',
                     (first_name, last_name, email, phone, reason, id))
        conn.commit()
        conn.close()

        flash('Contact updated successfully!', 'success')
        return redirect(url_for('view_contacts'))

    conn.close()
    return render_template('edit_contact.html', contact=contact)

# Route to delete a contact
@app.route('/admin/delete_contact/<int:id>', methods=['POST'])
def delete_contact(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM contacts WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash('Contact deleted successfully!', 'success')
    return redirect(url_for('view_contacts'))

# Route to view applications in the admin panel with pagination
@app.route('/admin/applications')
def view_applications():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of records per page
    offset = (page - 1) * per_page

    conn = get_db_connection()
    applications = conn.execute('SELECT * FROM applications LIMIT ? OFFSET ?', (per_page, offset)).fetchall()
    conn.close()

    return render_template('applications.html', applications=applications, page=page, per_page=per_page)

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

        return redirect(url_for('contact'))

    return render_template('contact.html')

# Apply page route with POST method to handle form submission
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        try:
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

              # Send confirmation email
            send_confirmation_email(email, first_name)

            flash('Application form submitted successfully! A confirmation email has been sent.', 'success')
            return {"message": "Application submitted successfully!"}, 200

        except Exception as e:
            flash(f'Error: {e}', 'danger')
            return {"message": str(e)}, 500

    return render_template('apply.html')

# Initialize the database and run the app
if __name__ == '__main__':
    init_db()  
    app.run(debug=True, port=5001)  
