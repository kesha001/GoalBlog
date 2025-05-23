from typing import Optional
import sqlalchemy.orm as so
import sqlalchemy as sa
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(50), unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(70), unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

    def __repr__(self):
        return f'User: {self.id} {self.username}'