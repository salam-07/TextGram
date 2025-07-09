from flask import render_template, url_for, redirect, flash
from echoapp import app, db, bcrypt
from echoapp.models import User, Post
from echoapp.forms import RegistrationForm, LoginForm

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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'You are now part of Echo! Log in to continue.', 'success')
        return redirect(url_for('login'))
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