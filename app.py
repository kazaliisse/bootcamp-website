from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from auth import auth  # Importing the auth blueprint
import smtplib  # Add this line for sending emails
from flask_mail import Mail, Message  # Importing Flask-Mail
import sqlite3
from email.mime.text import MIMEText  # For plain text email body
from email.mime.multipart import MIMEMultipart  # For complex email messages
import os
from werkzeug.utils import secure_filename

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
            'Application Received!',
            sender='noorhafowbare@gmail.com',  
            recipients=[email]
        )
        msg.body = f"Hello {first_name},\n\nThank you for applying for the {course} at Al Noor Bootcamp. We have successfully received your application, and our team is currently reviewing it. We will notify you of the outcome within 24Hrs. Please feel free to contact us if you have any questions in the meantime. Thank you for choosing Al Noor Bootcamp to advance your skills.\n\nBest regards,\nThe Al Noor Bootcamp Team"
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
    per_page = 80  # Number of records per page
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

# Function to send an email
def send_email(to_email, subject, body):
    try:
        sender_email = "noorhafowbare@gmail.com"  # Replace with your email
        sender_password = "qjmnwlgthsskjbwy"  # Replace with your email password
        
        # Setting up the email server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Sending email
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to fetch an application by ID
def query_database_by_id(application_id):
    """
    Fetch an application record by its ID from the database.

    Parameters:
        application_id (int): The ID of the application to retrieve.

    Returns:
        dict: A dictionary containing the application data, or None if not found.
    """
    try:
        conn = sqlite3.connect('database.db')  # Connect to your database
        conn.row_factory = sqlite3.Row  # Fetch rows as dictionaries
        cursor = conn.cursor()
        
        # Query to fetch application by ID
        cursor.execute("SELECT * FROM applications WHERE id = ?", (application_id,))
        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None
    except Exception as e:
        print(f"Error fetching application by ID: {e}")
        return None

# Function to update the application status
def update_application_status(application_id, status):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE applications SET status = ? WHERE id = ?", (status, application_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error updating application status: {e}")

# Admin page route
@app.route('/admin')
def admin_page():
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM applications")
        applications = cursor.fetchall()
        conn.close()
        return render_template('admin.html', applications=applications)
    except Exception as e:
        flash(f"Error loading admin page: {e}", "danger")
        return redirect(url_for('home'))

# Accept application route
@app.route('/accept_application/<int:application_id>', methods=['POST'])
def accept_application(application_id):
    application = query_database_by_id(application_id)
    if application:
        send_email(
    application['email'], 
    "Congratulations – You’ve Been Accepted!", 
    f"""Dear {application['first_name']} {application['last_name']}, 

Congratulations! After reviewing your application, we are thrilled to inform you that you have been accepted into the {application['course']} at Al Noor Bootcamp. This is the first step towards an exciting learning journey, and we are honored to have you join our program. To finalize your enrollment, please complete the following steps:

1. Please proceed with your admission fee payment through the following account:
   - Account Number: 212121
   - Business Number: 888888
If you need any assistance or have questions, feel free to reach out to us at noorhafowbare@gmail.com.

We look forward to welcoming you to Al Noor Bootcamp!"""
)
        update_application_status(application_id, "Accepted")
        flash("Application Accepted and Email Sent!", "success")
    else:
        flash("Application not found.", "danger")
    return redirect(url_for('view_applications'))

# Decline application route
@app.route('/decline_application/<int:application_id>', methods=['POST'])
def decline_application(application_id):
    application = query_database_by_id(application_id)
    if application:
        send_email(
            application['email'], 
            "Update on Your Application", 
            f"Dear {application['first_name']} {application['last_name']},\n\nWe regret to inform you that your application was not accepted. "

        )
        update_application_status(application_id, "Declined")
        flash("Application Declined and Email Sent!", "success")
    else:
        flash("Application not found.", "danger")
    return redirect(url_for('view_applications'))

@app.route('/delete_application/<int:id>', methods=['POST'])
def delete_application(id):
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete the application from the database
        cursor.execute("DELETE FROM applications WHERE id = ?", (id,))
        conn.commit()

        # Close the database connection
        conn.close()

        flash('Application deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting application: {e}', 'danger')

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

# Ensure your UPLOAD_FOLDER and ALLOWED_EXTENSIONS are defined correctly
UPLOAD_FOLDER = 'uploads/'  # Folder where files will be saved
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Apply page route with POST method to handle form submission
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    # Ensure user is logged in before accessing the apply page
    if 'user_id' not in session:  # Check if user is logged in
        flash('You must be logged in to apply.', 'warning')
        return redirect(url_for('auth.login'))  # Redirect to login page if not logged in

    # Define the list of courses
    courses = [
        "Web Development",
        "Data Science",
        "Cybersecurity",
        "Mobile App Development",
        "Digital Marketing",
        "E-Commerce"
    ]

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

            # Handle file upload
            file = request.files.get('resume')  # Ensure you're getting the file from the form
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                print(f"File saved at: {file_path}")  # Debugging line
            else:
                file_path = None  # If no file was uploaded or file is not allowed
                print("No valid file path")

            # Connect to the database and save the application data
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                    INSERT INTO applications (first_name, last_name, email, phone, gender, county, course, resume_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (first_name, last_name, email, phone, gender, county, course, file_path))
            conn.commit()
            conn.close()

            # Send confirmation email
            send_confirmation_email(email, first_name, course)

            flash('Application form submitted successfully! A confirmation email has been sent.', 'success')
            # return {"message": "Application submitted successfully!"}, 200

        except Exception as e:
            flash(f'Error: {e}', 'danger')
            return {"message": str(e)}, 500

    # Pass the courses list to the template
    return render_template('apply.html', courses=courses)


@app.route('/uploads/<filename>')
def download_file(filename):
    # Ensure the file exists and is in the UPLOAD_FOLDER
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        flash(f"Error: {e}", 'danger')
        return redirect(url_for('home'))  # Or any other appropriate redirect
#auth
@app.route('/auth')
def auth():
    # Your view logic here
    return render_template('auth.html')


# Initialize the database and run the app
if __name__ == '__main__':
    init_db()  
    app.run(debug=True, port=5001)  