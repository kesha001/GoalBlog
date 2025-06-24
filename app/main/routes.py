from app.main import main_bp
from app.main.forms import GoalForm

from flask import url_for, render_template, redirect, flash, request, abort, current_app
from flask_login import login_required, current_user
from app.models import Goal
from app import db
import sqlalchemy as sa


@main_bp.route('/')
@main_bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = GoalForm()
    if form.validate_on_submit():
        goal = Goal()
        goal.body = form.body.data
        goal.title = form.title.data
        current_user.goals.add(goal)
        db.session.commit()

        flash(f"Postet  {form.title.data}")

        return redirect(url_for('main_bp.index'))

    goals_query = current_user.get_following_posts()

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['GOALS_PER_PAGE']
    goals = db.paginate(goals_query, 
                        page=page,
                        per_page=per_page,
                        error_out=False
    )
    prev_url = url_for('main_bp.index', page=goals.prev_num)\
                if goals.has_prev else None
    next_url = url_for('main_bp.index', page=goals.next_num)\
                if goals.has_next else None
    
    return render_template('main/index.html', goals=goals, form=form,
                           prev_url=prev_url, next_url=next_url)


@main_bp.route('/explore', methods=['GET'])
@login_required
def explore():

    goals_query = sa.select(Goal).order_by(sa.desc(Goal.timestamp))

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['GOALS_PER_PAGE']
    goals = db.paginate(goals_query, 
                        page=page,
                        per_page=per_page,
                        error_out=False
    )

    prev_url = url_for('main_bp.explore', page=goals.prev_num)\
                if goals.has_prev else None
    next_url = url_for('main_bp.explore', page=goals.next_num)\
                if goals.has_next else None

    return render_template('main/index.html', goals=goals, is_explore=True,
                           prev_url=prev_url, next_url=next_url)


# @main_bp.after_request
# def logging_requests(response):

#     response_status = response.status_code
#     response_data = (request.remote_addr,
#                             request.method, 
#                             request.scheme, 
#                             request.full_path,
#                             response.status)
     
#     if 500 <= response_status <= 599: 
#         file_logger.error("{} {} {} {} {} INTERNAL SERVER ERROR".format(*response_data))
#     if 400 <= response_status <= 499: 
#         file_logger.warning("{} {} {} {} {} CLIENT ERROR".format(*response_data))
#     else:
#         file_logger.info("{} {} {} {} {}".format(*response_data))
    
#     return response