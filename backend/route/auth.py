from flask import Blueprint, jsonify, request, g
from flask_httpauth import HTTPTokenAuth
import jwt
from datetime import datetime, timedelta
from config import Config
from model.user import User

auth_bp = Blueprint('auth', __name__)
auth = HTTPTokenAuth('Bearer')

@auth.verify_token
def verify_token(token):
    try:
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        if 'user_id' in data:
            g.user = User.query.get(data['user_id'])  # 确保将用户对象存入g
            return g.user
    except Exception as e:
        print(f"Token验证失败: {str(e)}")
    return None
    
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if not user:  # 新增：用户不存在时返回401
        return jsonify({'message': '用户不存在'}), 401
    if not user.check_password(data.get('password')):  # 密码错误时返回401
        return jsonify({'message': '密码错误'}), 401
    
    try:
        token = jwt.encode(
            {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=24)},
            Config.SECRET_KEY,
            algorithm='HS256'
        )
        return jsonify({'token': token})
    except Exception as e:
        return jsonify({'message': 'Token生成失败'}), 500