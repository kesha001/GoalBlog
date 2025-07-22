from celery import Celery, Task
# from app import celery_app

def celery_init_app(app) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            # THIS IS HOW SHOULD IT WORK AS OF FLASK CELERY TUTORIAL, BUT IT GIVES Popped wrong app context ERROR, 
            # I REMOVED IT AND ADDED AND ADDED app = create_app() app.app_context().push() INSIDE OF DIFFERENT TASK IN TASKS
            # with app.app_context():
                # print(app.app_context())
            return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask,
                        broker=app.config["CELERY_BROKER_URI"], 
                        backend=app.config["CELERY_BACKEND_URI"],
                        include=["app.tasks"]
                        )
    celery_app.conf.update(app.config)
    celery_app.set_default()
    print(app.app_context())
    # celery_app.add_defaults(app.config)
    app.extensions["celery"] = celery_app

    print(celery_app.conf['SQLALCHEMY_DATABASE_URI'])
    return celery_app