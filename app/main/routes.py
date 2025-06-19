from app.main import main_bp
from app.main.forms import GoalForm

from flask import url_for, render_template, redirect, flash, request, abort
from flask_login import login_required, current_user
from app.models import Goal
from app import db, file_logger
import sqlalchemy as sa


@main_bp.route('/')
@main_bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = GoalForm()
    if form.validate_on_submit():
        goal = Goal()
        goal.body = form.body.data
        current_user.goals.add(goal)
        db.session.commit()

        flash(f"Postet  {form.title.data}")

        return redirect(url_for('main_bp.index'))

    goals = current_user.get_following_posts()

    followings = current_user.get_following()

    return render_template('main/index.html', goals=goals, form=form, followings=followings)


@main_bp.route('/explore', methods=['GET'])
@login_required
def explore():

    goals = db.session.scalars(
        sa.select(Goal).order_by(sa.desc(Goal.timestamp))
    ).all()

    return render_template('main/index.html', goals=goals)


# TODO: replace it with addit logger to app.logger
@main_bp.after_request
def logging_requests(response):

    response_status = response.status_code
    response_data = (request.remote_addr,
                            request.method, 
                            request.scheme, 
                            request.full_path,
                            response.status)
     
    if 500 <= response_status <= 599: 
        file_logger.error("{} {} {} {} {} INTERNAL SERVER ERROR".format(*response_data))
    if 400 <= response_status <= 499: 
        file_logger.warning("{} {} {} {} {} CLIENT ERROR".format(*response_data))
    else:
        file_logger.info("{} {} {} {} {}".format(*response_data))
    
    return response