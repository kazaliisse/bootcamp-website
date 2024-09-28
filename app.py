from flask import Flask, render_template

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
    app.run(debug=True)
