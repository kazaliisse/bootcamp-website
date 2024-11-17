import sqlite3

try:
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create a users table for authentication
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL
                    )''')

    # Create a contacts table
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        reason TEXT NOT NULL
                    )''')

    # Create an applications table with a status column
    cursor.execute('''CREATE TABLE IF NOT EXISTS applications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        gender TEXT NOT NULL,
                        county TEXT NOT NULL,
                        course TEXT NOT NULL,
                        status TEXT DEFAULT 'Pending' -- Status column added
                    )''')

    # Create a reset_tokens table
    cursor.execute('''CREATE TABLE IF NOT EXISTS reset_tokens (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT NOT NULL,
                        token TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

    # Commit the changes
    conn.commit()
    print("Tables created successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the connection
    conn.close()
