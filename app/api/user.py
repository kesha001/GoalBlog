from app.api import api_bp
from flask import jsonify, json, request, current_app, url_for
from app import db
import sqlalchemy as sa
from app.models import User
from app.api.errors import handle_bad_request

@api_bp.route('/hello')
def hello():
    return 'Hello world'

@api_bp.route('/users', methods=['GET'])
def get_users():
    query = sa.select(User)
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 5, type=int), 50)
    return User.collection_to_dict(query, page=page, per_page=per_page, endpoint='api_bp.get_users')

@api_bp.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = db.get_or_404(User, id)

    return user.to_dict()

@api_bp.route('/users/<id>/followings', methods=['GET'])
def get_users_followings(id):
    user = db.get_or_404(User, id)
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 5, type=int), 50)
    query = user.following.select()
    return User.collection_to_dict(query, page=page, per_page=per_page, endpoint='api_bp.get_users_followings')



@api_bp.route('/users/<id>/followers', methods=['GET'])
def get_users_followers(id):
    user = db.get_or_404(User, id)
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 5, type=int), 50)
    query = user.followers.select()
    return User.collection_to_dict(query, page=page, per_page=per_page, endpoint='api_bp.get_users_followers', id=id)


@api_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    for field in ["username", "email", "password"]:
        if field not in data:
            return handle_bad_request(f"{field} field is required")

    username_exists = db.session.scalar(sa.select(User).where(User.username==data['username']))  
    if username_exists:
        return handle_bad_request("Use another username")

    email_exists = db.session.scalar(sa.select(User).where(User.email==data['email']))  
    if email_exists:
        return handle_bad_request("Use another email")
    
    new_user = User()
    new_user.from_dict(data, new_user=True)

    db.session.add(new_user)
    db.session.commit()

    return new_user.to_dict(), 201, {"Response": "Created", "Description": "The user has been created"}
    

@api_bp.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    print(data)
    user = db.get_or_404(User, id)

    if 'username' in data:
        new_username_exists = user.username != data['username'] and \
            db.session.scalar(sa.select(User).where(User.username==data['email'])) 
        if new_username_exists:
            return handle_bad_request("Use another username")  

    if 'email' in data:
        new_email_exists = user.email != data['email'] and \
            db.session.scalar(sa.select(User).where(User.email==data['email'])) 
        if new_email_exists:
            return handle_bad_request("Use another email")

    user.from_dict(data, new_user=False)

    db.session.commit()    

    return user.to_dict()

