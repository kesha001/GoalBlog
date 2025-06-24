from typing import Optional
import sqlalchemy.orm as so
import sqlalchemy as sa
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone
from hashlib import sha256
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask import current_app



@login_manager.user_loader
def load_user(user_id: str):
    user_id = int(user_id)
    return db.session.get(User, user_id)


user_following = db.Table(
    "user_following",
    sa.Column("follower_id", sa.Integer, sa.ForeignKey("user.id"), primary_key=True),
    sa.Column("followed_id", sa.Integer, sa.ForeignKey("user.id"), primary_key=True)
)



class User(db.Model, UserMixin):
    __tablename__ = "user"

    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(50), unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(70), unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))

    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    bio: so.Mapped[Optional[str]] = so.mapped_column(sa.String(300))

    goals: so.WriteOnlyMapped['Goal'] = so.relationship(back_populates='author')

    followers: so.WriteOnlyMapped['User'] = so.relationship(
        "User",
        secondary= user_following,
        primaryjoin= lambda: User.id==user_following.c.followed_id,
        secondaryjoin= lambda: User.id==user_following.c.follower_id,
        back_populates= "following",
    )

    following: so.WriteOnlyMapped['User'] = so.relationship(
        "User",
        secondary= user_following,
        primaryjoin= lambda: User.id==user_following.c.follower_id,
        secondaryjoin= lambda: User.id==user_following.c.followed_id,
        back_populates= "followers",
    )

    def __init__(self, username: str, email: str, password=None):
        self.username = username
        self.email = email
        if password:
            self.set_password(password)

    
    def get_avatar(self, size=80):
        email_bytestring = bytes(self.email, 'utf-8')
        email_hash = sha256(email_bytestring).hexdigest()
        return f'https://gravatar.com/avatar/{email_hash}?d=monsterid&s={size}'
    
    def get_following(self):
        user = db.session.get(User, self.id)
        query = user.following.select()

        return db.session.scalars(query).all()
    
    def is_following(self, user):
        query = self.following.select().where(User.id==user.id)
        return db.session.scalar(query)
    
    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)
        
    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)
    
    def count_followers(self):
        query = sa.select(sa.func.count()).select_from(
            self.followers.select().subquery()
        )
        return db.session.scalar(query)
    
    def count_following(self):
        query = sa.select(sa.func.count()).select_from(
            self.following.select().subquery()
        )
        return db.session.scalar(query)
    
    def get_following_posts(self):
        main_user = so.aliased(User)
        users_followings = so.aliased(User) 
        
        u = sa.union_all(
        # Goals of those who main user follows
        sa.select(Goal)
            .join(main_user.following.of_type(users_followings))
            .join(users_followings.goals)
            .where(main_user.id==self.id),
        # Goals of main user
        sa.select(Goal)
            .join(main_user.goals)
            .where(main_user.id==self.id)
        )

        # goals = db.session.scalars(
        #     sa.select(Goal)
        #     .from_statement(u)
        # ).all()
        # from_statement is not flexible for further use. does not work with f ex pagination

        union_goal_alias = so.aliased(Goal, u.subquery())
        goals_query = sa.select(union_goal_alias).order_by(
            sa.desc(union_goal_alias.timestamp)
        )

        return goals_query
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def create_password_reset_token(self):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt=self.password_hash)
    
        return serializer.dumps(self.email)
    
    @classmethod
    def check_password_reset_token(cls, token, user_id):
        user = db.session.get(User, int(user_id))

        if not user:
            return None
        
        deserializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt=user.password_hash)

        try:
            email = deserializer.loads(token, max_age=current_app.config['RESET_TOKEN_MAX_AGE'])
        except(BadSignature, SignatureExpired):
            return None
    
        if email != user.email:
            return None
        
        return user

    def __repr__(self):
        return f'User: {self.id} {self.username}'




class Goal(db.Model):
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(256))
    user_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey(User.id))
    timestamp: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))

    author: so.Mapped['User'] = so.relationship(back_populates='goals')
