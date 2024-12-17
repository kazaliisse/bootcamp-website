from flask import Blueprint, render_template, request, redirect, url_for, flash, Flask
import sqlite3
import secrets
from datetime import datetime, timedelta
from flask_mail import Message, Mail
from werkzeug.security import generate_password_hash, check_password_hash

password_reset_bp = Blueprint('password_reset', __name__)

# Initialize Flask app
app = Flask(__name__)

# Flask-Mail configuration for SSL
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # Use TLS, port 587
app.config['MAIL_USE_TLS'] = True  # Enable TLS
app.config['MAIL_USE_SSL'] = False  # Disable SSL
app.config['MAIL_USERNAME'] = 'bushranb8@gmail.com'  # Your Gmail address
app.config['MAIL_PASSWORD'] = 'kbyc xlok nwnb mnbh'  # Your Gmail app password
app.config['MAIL_DEFAULT_SENDER'] = 'bushranb8@gmail.com'  # Default sender email

# Initialize Flask-Mail
mail = Mail(app)

# Route to send reset code to email
# Route to send reset code to email
@password_reset_bp.route('/request-reset', methods=['GET', 'POST'])
def send_reset_code():
    if request.method == 'POST':
        email = request.form['email']
        
        # Generate a reset token (32 characters long)
        reset_token = secrets.token_urlsafe(32)
        expiration_time = datetime.now() + timedelta(minutes=30)  # Token expires in 30 minutes

        # Check if the email exists in the users table
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user:
            # Insert the reset token and expiration time into reset_tokens table
            cursor.execute("INSERT INTO reset_tokens (email, token, expiration_time) VALUES (?, ?, ?)", 
                           (email, reset_token, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()

            # Create the HTML content for the email
            email_html = f"""
            <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f4;
                            margin: 0;
                            padding: 0;
                        }}
                        .container {{
                            width: 100%;
                            max-width: 600px;
                            margin: 20px auto;
                            background-color: #ffffff;
                            padding: 20px;
                            border-radius: 8px;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        }}
                        .header {{
                            text-align: center;
                            background-color: #3498db;
                            color: white;
                            padding: 10px 0;
                            border-radius: 8px;
                        }}
                        .content {{
                            margin-top: 20px;
                            padding: 15px;
                            background-color: #f9f9f9;
                            border-radius: 8px;
                        }}
                        .button {{
                            background-color: #3498db;
                            color: white;
                            padding: 10px 20px;
                            text-decoration: none;
                            border-radius: 5px;
                            display: inline-block;
                            margin-top: 20px;
                        }}
                        .footer {{
                            text-align: center;
                            margin-top: 20px;
                            font-size: 12px;
                            color: #777;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h2>Password Reset Request</h2>
                        </div>
                        <div class="content">
                            <p>Hi there,</p>
                            <p>We received a request to reset your password. Your password reset code is:</p>
                            <h3 style="color: #3498db;">{reset_token}</h3>
                            <p>This code will expire in 30 minutes. Please use it to reset your password.</p>
                            <p>Click the button below to go to the reset page:</p>
                            <a href="{url_for('password_reset.reset_password', _external=True)}" class="button">Reset Your Password</a>
                        </div>
                        <div class="footer">
                            <p>If you did not request a password reset, please ignore this email.</p>
                        </div>
                    </div>
                </body>
            </html>
            """

            # Send the HTML email
            msg = Message("Password Reset Code", recipients=[email], html=email_html)
            msg.sender = app.config['MAIL_DEFAULT_SENDER']  # Explicitly set the sender

            try:
                print(f"Sending email to {email}")  # Debugging log
                mail.send(msg)
                print("Email sent successfully")  # Debugging log
                flash("A password reset token has been sent to your email.", "success")
                return redirect(url_for('password_reset.reset_password'))  # Redirect to password reset page
            except Exception as e:
                print(f"Failed to send email: {e}")  # Debugging log
                flash(f"Failed to send email: {e}", "error")
                return redirect(url_for('password_reset.send_reset_code'))

        else:
            flash("Email not found.", "error")
            return redirect(url_for('password_reset.send_reset_code'))

        conn.close()

    return render_template('password_reset_form.html')





# Route to reset the user's password
@password_reset_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        reset_token = request.form['reset_code']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Check if the passwords match
        if new_password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('password_reset.reset_password'))

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Validate reset token in the database
            cursor.execute("SELECT email, expiration_time FROM reset_tokens WHERE token=?", (reset_token,))
            result = cursor.fetchone()

            if not result:
                flash("Invalid or expired reset token.", "error")
                return redirect(url_for('password_reset.reset_password'))

            email, expiration_time = result
            current_time = datetime.now()

            # Check if the token has expired
            if current_time > datetime.strptime(expiration_time, '%Y-%m-%d %H:%M:%S'):
                flash("The reset token has expired.", "error")
                return redirect(url_for('password_reset.reset_password'))

            # Hash the new password before saving it
            hashed_password = generate_password_hash(new_password)

            # Update the user's password
            cursor.execute("UPDATE users SET password=? WHERE email=?", (hashed_password, email))
            conn.commit()

            # Delete the used reset token from the database
            cursor.execute("DELETE FROM reset_tokens WHERE email=?", (email,))
            conn.commit()

            flash("Your password has been reset successfully!", "success")
            return redirect(url_for('auth.login'))  # Redirect to login after successful reset
        except Exception as e:
            flash(f"An error occurred: {e}", "error")
        finally:
            conn.close()

    return render_template('reset.html')  # Form for code and new password


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5001)