from typing import Optional
import sqlalchemy.orm as so
import sqlalchemy as sa
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone
from hashlib import sha256



@login_manager.user_loader
def load_user(user_id: str):
    user_id = int(user_id)
    return db.session.get(User, user_id)



class User(db.Model, UserMixin):
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(50), unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(70), unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))

    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=datetime.now(timezone.utc))
    bio: so.Mapped[Optional[str]] = so.mapped_column(sa.String(300))

    goals: so.WriteOnlyMapped['Goal'] = so.relationship(back_populates='author')

    
    def get_avatar(self, size=80):
        email_bytestring = bytes(self.email, 'utf-8')
        email_hash = sha256(email_bytestring).hexdigest()
        return f'https://gravatar.com/avatar/{email_hash}?d=monsterid&s={size}'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

    def __repr__(self):
        return f'User: {self.id} {self.username}'
    

class Goal(db.Model):
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(256))
    user_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey(User.id))
    timestamp: so.Mapped[datetime] = so.mapped_column(default=datetime.now(timezone.utc))

    author: so.Mapped['User'] = so.relationship(back_populates='goals')