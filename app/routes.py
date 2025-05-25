from app import app
from app.forms import LoginForm, RegisterForm
from app.models import User
from flask import url_for, render_template, redirect, flash
from flask_login import login_user, login_required
from app.models import User
from app import db
import sqlalchemy as sa
import flask

from urllib.parse import urlparse

@app.route('/')
@app.route('/index')
@login_required
def index():
    print(url_for('index'))

    user = {'username': 'John'}
    # list of goals , think about structure of these goals
    # it should be a group of goals with title and goals inside
    goals = [
    
    {
        "author": {'username': 'John'},
        "title": "Make a goal",
        "body": "make that goal is on webpage"
    },
    {
        "author": {'username': 'Susan'},
        "title": "Find a job",
        "body": "learn, get skills, pass intervju"
    },
    ]


    return render_template('index.html', user=user, goals=goals)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        query = sa.select(User).where(User.username == form.username.data)
        user = db.one_or_404(query)

        # print(f"form.username.data {form.username.data}")
        # print(f"form.password.data {form.password.data}")
        # print(f"form.password.data {form.remember_me.data}")

        if not user or not user.check_password(form.password.data):
            flash('Wrong username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        
        next_url = flask.request.args.get('next')
        next_url_parced = urlparse(next_url)

        if next_url_parced.scheme or next_url_parced.netloc:
            return flask.abort(400)

        flash('Succesfully logged in!')
        return redirect(next_url or url_for('index'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash('User registrated!')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)