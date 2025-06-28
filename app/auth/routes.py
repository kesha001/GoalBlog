from app.auth.forms import LoginForm, RegisterForm, RequestResetPasswordForm, ResetPasswordForm
from app.auth import auth_bp
from app.utils.mail import send_mail_threading
from app.models import User
from app import db
from flask import url_for, render_template, redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user
import sqlalchemy as sa
import flask
from urllib.parse import urlparse

from flask_babel import _


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))
    form = LoginForm()
    if form.validate_on_submit():
        
        query = sa.select(User).where(User.username == form.username.data)
        user = db.session.scalars(query).one_or_none()

        if not user or not user.check_password(form.password.data):
            flash(_('Wrong username or password'))
            return redirect(url_for('auth_bp.login'))
        
        login_user(user, remember=form.remember_me.data)
        
        next_url = flask.request.args.get('next')
        next_url_parced = urlparse(next_url)

        if next_url_parced.scheme or next_url_parced.netloc:
            return flask.abort(400)

        flash(_('Succesfully logged in!'))
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

        flash(_('User registrated!'))
        return redirect(url_for('auth_bp.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/request_reset_password', methods=['GET', 'POST'])
def request_reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))
    
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        email = form.data['email']
        user = db.session.scalar(sa.select(User).where(User.email == email))
        if user:
            send_reset_password_url(user)
        flash(_("The reset link has been sent to the email"))
        return redirect(url_for('auth_bp.login'))

    return render_template('auth/request_reset_password.html', form=form)

@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))
    token = request.args['token']
    user_id =  request.args['user_id']

    user = User.check_password_reset_token(token, user_id)

    if not user:
        flash(_("Reset password error"), category='error')
        return redirect(url_for('auth_bp.login'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        reset_form = form.data
        user.set_password(reset_form['password'])
        db.session.commit()

        flash(_("Password successfully changed"), category='info')

        return redirect(url_for('auth_bp.login'))

    return render_template('auth/reset_password.html', form=form)


def send_reset_password_url(user):
    reset_password_url = url_for(
        'auth_bp.reset_password',
        token=user.create_password_reset_token(),
        user_id=user.id,
        _external=True
    )

    email_body_html = render_template("auth/_reset_password_email.html", 
                                 reset_password_url=reset_password_url)

    send_mail_threading(
        subject="Test Password Reset",
        recipient=user.email,
        html=email_body_html
    )
