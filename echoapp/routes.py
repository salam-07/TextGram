from flask import render_template, url_for, redirect, flash, request
from echoapp import app, db, bcrypt
from echoapp.models import User, Post
from echoapp.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form  = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Couldn't Log in! Check username and password.", 'danger')
    return render_template('login.html', title="Log In", form=form)

@app.route('/account')
@login_required
def account():
    image_file = url_for('static', filename="profile_pics/" + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))