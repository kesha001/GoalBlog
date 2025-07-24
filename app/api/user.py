from app.api import api_bp
from flask import jsonify, json

@api_bp.route('/hello')
def hello():
    return 'Hello world'

@api_bp.route('/users', methods=['GET'])
def get_users():
    pass

@api_bp.route('/users/<id>', methods=['GET'])
def get_user(id):
    return jsonify(id)

@api_bp.route('/users/<id>/followings', methods=['GET'])
def get_users_followings(id):
    pass

@api_bp.route('/users/<id>/followers', methods=['GET'])
def get_users_followers(id):
    pass 

@api_bp.route('/users', methods=['POST'])
def create_user():
    pass

@api_bp.route('/users/<id>', methods=['PUT'])
def update_user(id):
    pass

