from app import app
from app.forms import LoginForm, RegisterForm, EditProfileForm
from app.models import User
from flask import url_for, render_template, redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db
import sqlalchemy as sa
import flask

from datetime import datetime, timezone
from urllib.parse import urlparse

@app.route('/')
@app.route('/index')
@login_required
def index():

    goals = db.session.scalars(
        current_user.goals.select()
    ).all()


    return render_template('index.html', goals=goals)


@app.route('/user/<username>', methods=['GET'])
@login_required
def user(username):

    query = sa.select(User).where(User.username == username)
    user = db.one_or_404(query)

    goals = db.session.scalars(
        user.goals.select()
    ).all()
    
    return render_template('user.html', user=user, goals=goals)


@app.route('/user/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():

    form = EditProfileForm(original_username=current_user.username)
    if request.method == 'GET':
        # Prepopulate
        form.username.data = current_user.username
        form.bio.data = current_user.bio
        
    if form.validate_on_submit():

        current_user.username = form.username.data    
        current_user.bio = form.bio.data

        db.session.commit()

        flash('Changes saved!')
        return redirect(url_for('edit_profile'))

    return render_template('edit_profile.html', form=form)


@app.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        
        query = sa.select(User).where(User.username == form.username.data)
        user = db.session.scalars(query).one_or_none()

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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        register_form = form.data
        print(register_form)
        user = User(username=register_form['username'],
                    email=register_form['email'])
        user.set_password(register_form['password'])

        db.session.add(user)
        db.session.commit()

        flash('User registrated!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)