from flask import Flask, render_template
import sys

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('AboutUs.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/mentors')
def mentors():
    return render_template('mentors.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/apply')
def apply():
    return render_template('apply.html')

if __name__ == '__main__':
    # Set the port to use from command line argument, default to 5000
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 5000.")
    
    app.run(debug=True, port=port)
