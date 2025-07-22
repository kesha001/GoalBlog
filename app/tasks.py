from celery import shared_task
from celery.result import AsyncResult
import time
from app import db, create_app
from app.models import Task, User, Goal
import sys
from flask import current_app
import sqlalchemy as sa
from app.utils.mail import send_mail_threading
import json
# from app import celery_init_app
# from app import celery_app



def _set_task_progress(progress, task):
    task_ = AsyncResult(task.request.id)
    print(task_.info)

    if task_:
        # print("in set task progress after if task")
        # task_.info['progress'] = progress
        # print(task_.info)
        # print("TASK INFO IN SET TASK PROGRESS:  ", task_.id)
        task_db_instance = db.session.get(Task, task_.id)

        task_db_instance.user.add_notification('task_progress', {'task_id': task_.id,
                                                    'progress': progress})
        
        if progress >= 100:
            task_db_instance.completed = True
        db.session.commit()


@shared_task(ignore_result=False, bind=True)
def add_together(self, a: int, b: int) -> int:
    self.update_state(meta={"progress":0})
    for i in range(11):
        time.sleep(1)
        self.update_state(meta={"progress":i/10})
    return a + b


@shared_task(ignore_result=False, bind=True)
# @celery_app.task(ignore_result=False, bind=True)
def export_goals(self, user_id) -> int:
    
    # IF YOU NEED APP CONTEXT IN TAKS USE THESE LINES, LOOK ALSO AT CELERY_UTILS.PY
    app = create_app()
    app.app_context().push()
    self.update_state(meta={"progress":0})


    try:
        user = db.session.get(User, user_id)
        _set_task_progress(0, self)
        data = []
        i = 0

        goals_count = db.session.scalar(
            sa.select(sa.func.count()).select_from(
                user.goals.select()
                .subquery()
            )
        )
        users_goals = db.session.scalars(
            user.goals.select().order_by(Goal.timestamp)
        )
        for goal in users_goals:
            # print("in for loop")
            goal_data = {
                "title": goal.title,
                "body": goal.body,
                "timestamp": str(goal.timestamp)
            }
            data.append(goal_data)
            i += 1
            self.update_state(meta={"progress":100*i // goals_count})
            _set_task_progress(100*i // goals_count, self)
            # print("progress: ", 100*i // goals_count)
            time.sleep(1)

        send_mail_threading(
            subject="Export of users Goals",
            recipient=user.email,
            attachments=[("goals.json", "application/json" ,json.dumps({"goals": data}))],
            force_sync=True)
            

    except Exception as e:
        print(e)
        _set_task_progress(100, self)
        current_app.logger.error('Unhandled exception', exc_info=sys.exc_info())
    finally:
        # print("finally")
        _set_task_progress(100, self)