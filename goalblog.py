from app import app 
import sqlalchemy.orm as so
import sqlalchemy as sa
from app import db


@app.shell_context_processor
def shell():
    return {
        "db": db, "sa": sa, "so": so
    }