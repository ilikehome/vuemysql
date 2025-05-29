from flask import Blueprint, jsonify, request, g
from flask_httpauth import HTTPTokenAuth
from models import db, User, Account  # 仅保留必要导入
import jwt
from datetime import datetime, timedelta
from config import Config

# 移除 from app import create_app 和 app = create_app()
auth = HTTPTokenAuth('Bearer')
bp = Blueprint('api', __name__)  # 仅定义蓝图，不依赖app实例

# Token验证
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

# 登录接口
@bp.route('/login', methods=['POST'])
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

# 用户管理接口（示例）
@bp.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username} for u in users])

# 用户新增接口
@bp.route('/users', methods=['POST'])
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
@bp.route('/users/<int:id>', methods=['PUT'])
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
@bp.route('/users/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': '用户删除成功'}), 200

# 账目列表接口（带用户筛选）
@bp.route('/accounts', methods=['GET'])
@auth.login_required
def get_accounts():
    try:
        accounts = Account.query.filter_by(user_id=g.user.id).all()
        return jsonify([{
            'id': a.id,
            'amount': a.amount,
            'type': a.type,
            'remark': a.remark,
            'created_at': a.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for a in accounts])
    except Exception as e:
        print(f"数据库查询错误: {str(e)}")
        return jsonify({'message': f'服务器内部错误: {str(e)}'}), 500

# 新增账目接口
@bp.route('/accounts', methods=['POST'])
@auth.login_required
def create_account():
    data = request.get_json()
    if not data or 'amount' not in data or 'type' not in data:
        return jsonify({'message': '缺少必要参数'}), 400
    
    # 强化类型验证
    if data['type'] not in ['income', 'expense']:
        return jsonify({'message': '类型必须是income或expense'}), 400
        
    # 确保金额为浮点数
    try:
        amount = float(data['amount'])
    except (ValueError, TypeError):
        return jsonify({'message': '金额必须是数字'}), 400
    
    new_account = Account(
        amount=float(data['amount']),  # 确保转换为float
        type=data['type'],
        remark=data.get('remark'),
        user_id=g.user.id
    )
    db.session.add(new_account)
    db.session.commit()
    
    return jsonify({
        'id': new_account.id,
        'amount': new_account.amount,
        'type': new_account.type,
        'remark': new_account.remark
    }), 201

# 编辑账目接口
@bp.route('/accounts/<int:id>', methods=['PUT'])
@auth.login_required
def update_account(id):
    account = Account.query.get_or_404(id)
    data = request.get_json()
    
    if 'amount' in data:
        account.amount = data['amount']
    if 'type' in data:
        account.type = data['type']
    if 'remark' in data:
        account.remark = data['remark']
    
    db.session.commit()
    return jsonify({
        'id': account.id,
        'amount': account.amount,
        'type': account.type,
        'remark': account.remark
    })

# 删除账目接口
@bp.route('/accounts/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_account(id):
    account = Account.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    return jsonify({'message': '账目删除成功'}), 200