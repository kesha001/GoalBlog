from typing import Optional
import sqlalchemy.orm as so
import sqlalchemy as sa
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone
from hashlib import sha256
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask import current_app, g
import json

from app.utils.search import add_to_index, delete_from_index, search_in_index



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
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(300))

    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    bio: so.Mapped[Optional[str]] = so.mapped_column(sa.String(500))

    goals: so.WriteOnlyMapped['Goal'] = so.relationship(back_populates='author')

    last_read_messages: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))

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


    messages_received: so.WriteOnlyMapped['Message'] = so.relationship(back_populates="recipient",
                                                                       foreign_keys='Message.recipient_id')
    messages_sent: so.WriteOnlyMapped['Message'] = so.relationship(back_populates="author",
                                                                       foreign_keys='Message.author_id')
    

    notifications: so.WriteOnlyMapped['Notification'] = so.relationship(back_populates='user')
    
    def __init__(self, username: str, email: str, password=None):
        self.username = username
        self.email = email
        if password:
            self.set_password(password)

    def add_notification(self, notification_name, data):
        # db.session.delete - marks for deletion, there are problems with it with elasticsearch mixin, I suppose execute exetures it without marking
        db.session.execute(self.notifications.delete().where(Notification.name == notification_name)) 

        new_notification = Notification(name=notification_name, payload=json.dumps(data))
        self.notifications.add(new_notification)

        db.session.commit()


    
    def count_unread_messages(self):
        
        last_read_messages_time = datetime(1, 1, 1) \
            if not self.last_read_messages else self.last_read_messages

        query = sa.select(sa.func.count()).select_from(
            self.messages_received.select()
            .where(Message.timestamp > last_read_messages_time)
            .subquery()
        )

        return db.session.scalar(query)
    
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



class Message(db.Model):
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(256))

    is_read: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), index=True)

    author_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey(User.id))
    recipient_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey(User.id))

    author: so.Mapped['User'] = so.relationship(back_populates='messages_sent', foreign_keys=[author_id])
    recipient: so.Mapped['User'] = so.relationship(back_populates='messages_received', foreign_keys=[recipient_id])

    def __repr__(self):
        return f'Message: {self.id} {self.body}'
    

class Notification(db.Model):
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)

    name: so.Mapped[str] = so.mapped_column(sa.String(128))
    payload: so.Mapped[str] = so.mapped_column(sa.Text)

    timestamp: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), index=True)

    user_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey(User.id))

    user: so.Mapped['User'] = so.relationship(back_populates='notifications')

    def __repr__(self):
        return f'Notification: {self.id} {self.payload}'
    


class Base(so.DeclarativeBase):
    pass


class SearchableMixin:
    
    @classmethod
    def search(cls, query, per_page, starting_num):
        
        index = getattr(cls, "__tablename__")
        result_idx, total_hits = search_in_index(index, query, per_page, starting_num)

        if not result_idx:
            return [], 0
        
        whens = {}
        for i in range(len(result_idx)):
            whens[result_idx[i]] = i
        
        query = sa.select(cls).where(
                cls.id.in_(result_idx)
            ).order_by(sa.case(whens, value=cls.id))
        found_objects = db.session.scalars(query).all()
        
        return found_objects, total_hits

    @classmethod
    def cache_sess_info(cls, session):
        db_sess_info = {}
        db_sess_info['new'] = list(session.new)
        db_sess_info['dirty'] = list(session.dirty)
        db_sess_info['deleted'] = list(session.deleted)

        session.info = db_sess_info


    @classmethod
    def insert_after_commit(cls, session):
        db_sess_info = session.info

        for object in db_sess_info['new']:
            add_to_index(object, getattr(object, "__tablename__"))
        for object in db_sess_info['dirty']:
            add_to_index(object, getattr(object, "__tablename__"))
        for object in db_sess_info['deleted']:
            delete_from_index(object, getattr(object, "__tablename__"))

        session.info = {}

    
    @classmethod
    def reindex(cls):
        all_objects = db.session.scalars(sa.select(cls))
        for object in all_objects:
            add_to_index(object, getattr(object, "__tablename__"))


    @classmethod
    def register_event_before_commit(cls):
        sa.event.listen(db.session, 'before_commit', cls.cache_sess_info)

    @classmethod
    def register_event_after_commit(cls):
        sa.event.listen(db.session, 'after_commit', cls.insert_after_commit)


class Goal(SearchableMixin, db.Model):
    __searchable__ = ['title', 'body']

    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    title: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), default="Title")
    body: so.Mapped[str] = so.mapped_column(sa.String(256))
    user_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey(User.id))
    timestamp: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), index=True)

    author: so.Mapped['User'] = so.relationship(back_populates='goals')

    language: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32))


Goal.register_event_before_commit()
Goal.register_event_after_commit()


