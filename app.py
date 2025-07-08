from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from datetime import datetime

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
app.config['SECRET_KEY'] = '8001fcf07d8a7ed4208c4a91f5ca0782'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Date posted('{self.date_posted}', Id: '{self.id}')"

# both routes lead to homepage
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', posts=posts, title="Scroll Latest")

# about page route
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    form  = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title="Register", form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form  = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'admin':
            flash(f'You have been logged In!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsucessful! Please check username and password', 'danger')
    return render_template('login.html', title="Log In", form=form)

if __name__ == "__main__":
    # debug=True for reflecting changes to server on save
    app.run(debug=True)