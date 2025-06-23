from app.models import User
from app import db
from flask_login import login_required, current_user
import sqlalchemy as sa
from flask import url_for, render_template, redirect, flash, request, current_app

from app.user import user_bp
from app.user.forms import EditProfileForm, FollowForm

from datetime import datetime, timezone


@user_bp.route('/user/<username>', methods=['GET'])
@login_required
def user(username):
    query = sa.select(User).where(User.username == username)
    user = db.one_or_404(query)

    goals_query = user.goals.select()

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['GOALS_PER_PAGE']
    goals = db.paginate(goals_query, 
                        page=page,
                        per_page=per_page,
                        error_out=False
    )

    form = FollowForm()

    prev_url = url_for('user_bp.user', page=goals.prev_num, username=username)\
                if goals.has_prev else None
    next_url = url_for('user_bp.user', page=goals.next_num, username=username)\
                if goals.has_next else None
    
    return render_template('user/user.html', user=user, goals=goals, form=form,
                           prev_url=prev_url, next_url=next_url)


@user_bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):

    form = FollowForm()

    if form.validate_on_submit():
        query = sa.select(User).where(User.username == username)
        user = db.session.scalar(query)
        if not user:
            flash(f'{user.username} not found')
            return redirect(url_for('main_bp.index'))
        elif current_user.id == user.id:
            flash(f'{user.username}, can not follow yourself')
            return redirect(url_for('user_bp.user', username=username))
        else:
            current_user.follow(user)
            db.session.commit()
            flash(f'{user.username} has been followed')
            return redirect(url_for('user_bp.user', username=username))
            
    return redirect(url_for('main_bp.index'))
    
    

@user_bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):

    form = FollowForm()

    if form.validate_on_submit():
        query = sa.select(User).where(User.username == username)
        user = db.session.scalar(query)
        if not user:
            flash(f'{user.username} not found')
            return redirect(url_for('main_bp.index'))
        elif current_user.id == user.id:
            flash(f'{user.username}, can not unfollow yourself')
            return redirect(url_for('user_bp.user', username=username))
        else:
            current_user.unfollow(user)
            db.session.commit()
            flash(f'{user.username} has been unfollowed')
            return redirect(url_for('user_bp.user', username=username))
            
    return redirect(url_for('main_bp.index'))
    
    
    

@user_bp.route('/user/edit_profile', methods=['GET', 'POST'])
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
        return redirect(url_for('user_bp.edit_profile'))

    return render_template('user/edit_profile.html', form=form)


@user_bp.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
