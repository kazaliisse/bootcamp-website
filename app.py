from flask import Flask, render_template, request, redirect, url_for, session, flash
from auth import auth  # Importing the auth blueprint

from flask_mail import Mail, Message  # Importing Flask-Mail
import sqlite3

app = Flask(__name__)

# Secret key for session management (required for flash messages)
app.secret_key = '64f6c772360b516a3807929b92468124af4aa4ba4ab61cdd3b1f18e46e194457'
# Register the auth blueprint with the app
app.register_blueprint(auth, url_prefix='/auth')





# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'noorhafowbare@gmail.com'  
app.config['MAIL_PASSWORD'] = 'qjmnwlgthsskjbwy'  

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
def send_confirmation_email(email, first_name, course):
    try:
        msg = Message(
            'Congratulations on Your Admission!',
            sender='noorhafowbare@gmail.com',  
            recipients=[email]
        )
        msg.body = f"Hello {first_name},\n\nCongratulations! Your admission application for the {course} course has been received successfully. We are excited to have you join us.\n\nBest regards,\nThe Team"
        mail.send(msg)
        print("Confirmation email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Route to view contacts in the admin panel with pagination
@app.route('/admin/contacts')
def view_contacts():
    # Search functionality
    search = request.args.get('search', '')  
    page = request.args.get('page', 1, type=int)
    # Number of records per page
    per_page = 10  
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
# Route to view applications in the admin panel with pagination and search
@app.route('/admin/applications')
def view_applications():
    search = request.args.get('search', '')  # Search functionality
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of records per page
    offset = (page - 1) * per_page

    conn = get_db_connection()
    search_query = f"%{search}%"  # Format search term for SQL LIKE
    applications = conn.execute(
        'SELECT * FROM applications WHERE first_name LIKE ? OR last_name LIKE ? LIMIT ? OFFSET ?',
        (search_query, search_query, per_page, offset)
    ).fetchall()

    # Get total number of applications for pagination
    total_query = 'SELECT COUNT(*) FROM applications WHERE first_name LIKE ? OR last_name LIKE ?'
    total = conn.execute(total_query, (search_query, search_query)).fetchone()[0]
    conn.close()

    return render_template('applications.html', applications=applications, page=page, per_page=per_page, total=total, search=search)

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

# Root route to redirect to home
@app.route('/')
def root():
    return redirect(url_for('home'))

# Home route that checks for user authentication
@app.route('/home')
def home():
    # Ensure user is authenticated
    if 'user_id' not in session:  # If user is not logged in
        return redirect(url_for('auth.login'))  # Redirect to login
    return render_template('index.html')  # Render home page for authenticated users


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
    if 'user_id' not in session:  # Check if the user is logged in
        return redirect(url_for('auth.login'))  # Redirect to login page if not logged in

    if request.method == 'POST':  # If form is submitted
        try:
            # Retrieve form data
            first_name = request.form['first-name']
            last_name = request.form['last-name']
            email = request.form['email']
            phone = request.form['phone']
            reason = request.form['reason']

            # Connect to the database and save the form data
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO contacts (first_name, last_name, email, phone, reason)
                VALUES (?, ?, ?, ?, ?)
            """, (first_name, last_name, email, phone, reason))
            conn.commit()
            conn.close()

            flash('Contact form submitted successfully!', 'success')  # Success message

        except Exception as e:
            flash(f'Error: {e}', 'danger')  # Error message if something goes wrong

        return redirect(url_for('contact'))  # Redirect to the contact page after form submission

    # For GET request, render the contact form
    return render_template('contact.html')



# Apply page route with POST method to handle form submission
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    # Ensure user is logged in before accessing the apply page
    if 'user_id' not in session:  # Check if user is logged in
        flash('You must be logged in to apply.', 'warning')
        return redirect(url_for('auth.login'))  # Redirect to login page if not logged in
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
            send_confirmation_email(email, first_name, course)

            flash('Application form submitted successfully! A confirmation email has been sent.', 'success')
            return {"message": "Application submitted successfully!"}, 200

        except Exception as e:
            flash(f'Error: {e}', 'danger')
            return {"message": str(e)}, 500

    return render_template('apply.html')
#auth
@app.route('/auth')
def auth():
    # Your view logic here
    return render_template('auth.html')


# Initialize the database and run the app
if __name__ == '__main__':
    init_db()  
    app.run(debug=True, port=5001)  
