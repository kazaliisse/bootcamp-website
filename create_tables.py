import sqlite3

try:
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create a contacts table
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        reason TEXT NOT NULL
                    )''')

    # Create an applications table
    cursor.execute('''CREATE TABLE IF NOT EXISTS applications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        gender TEXT NOT NULL,
                        county TEXT NOT NULL,
                        course TEXT NOT NULL
                    )''')

    # Commit the changes
    conn.commit()
    print("Tables created successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the connection
    conn.close()
