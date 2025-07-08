from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# dummy data is a list of dictionaries
posts = [
    {
        'author': 'Abdus Salam',
        'content': 'This App is so lit',
        'date_posted': '15:02, 8 July 2025'
    }
    ,
    {
        'author': 'Joe Goldberg',
        'content': 'Hello, You',
        'date_posted': '14:30, 4 July 2025'
    }
]


app = Flask(__name__)

# both routes lead to homepage
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', posts=posts)

# about page route
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    # debug=True for reflecting changes to server on save
    app.run(debug=True)