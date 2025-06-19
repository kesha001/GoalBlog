from app.auth.forms import LoginForm, RegisterForm
from app.auth import auth_bp
from app.models import User
from app import db
from flask import url_for, render_template, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
import sqlalchemy as sa
import flask
from urllib.parse import urlparse


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))
    form = LoginForm()
    if form.validate_on_submit():
        
        query = sa.select(User).where(User.username == form.username.data)
        user = db.session.scalars(query).one_or_none()

        if not user or not user.check_password(form.password.data):
            flash('Wrong username or password')
            return redirect(url_for('auth_bp.login'))
        
        login_user(user, remember=form.remember_me.data)
        
        next_url = flask.request.args.get('next')
        next_url_parced = urlparse(next_url)

        if next_url_parced.scheme or next_url_parced.netloc:
            return flask.abort(400)

        flash('Succesfully logged in!')
        return redirect(next_url or url_for('main_bp.index'))
    return render_template('auth/login.html', form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for('auth_bp.login'))
    return render_template('auth/register.html', form=form)