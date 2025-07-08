from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# both routes lead to homepage
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

# about page route
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    # debug=True for reflecting changes to server on save
    app.run(debug=True)