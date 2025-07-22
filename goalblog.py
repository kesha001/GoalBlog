from app import create_app 
import sqlalchemy.orm as so
import sqlalchemy as sa
from app import db

app = create_app()
celery_app = app.extensions["celery"]

@app.shell_context_processor
def shell():
    return {
        "db": db, "sa": sa, "so": so,  
    }