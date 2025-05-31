from flask import Blueprint, jsonify, request
from model.user import User
from app import db
from route.auth import auth

user_bp = Blueprint('user', __name__)

# 用户管理接口（示例）
@user_bp.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username} for u in users])

# 用户新增接口
@user_bp.route('/users', methods=['POST'])
@auth.login_required
def create_user():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': '缺少必要参数'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': '用户名已存在'}), 400
    
    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'id': new_user.id, 'username': new_user.username}), 201

# 用户编辑接口
@user_bp.route('/users/<int:id>', methods=['PUT'])
@auth.login_required
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    if 'username' in data:
        if User.query.filter_by(username=data['username']).first() and data['username'] != user.username:
            return jsonify({'message': '用户名已存在'}), 400
        user.username = data['username']
    
    if 'password' in data:
        user.set_password(data['password'])
    
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username})

# 用户删除接口
@user_bp.route('/users/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': '用户删除成功'}), 200
