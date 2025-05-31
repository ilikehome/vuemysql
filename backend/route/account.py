from flask import Blueprint, jsonify, request, g
from model.account import Account
from app import db
from route.auth import auth

account_bp = Blueprint('account', __name__)
# 账目列表接口（带用户筛选）
@account_bp.route('/accounts', methods=['GET'])
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
@account_bp.route('/accounts', methods=['POST'])
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
@account_bp.route('/accounts/<int:id>', methods=['PUT'])
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
@account_bp.route('/accounts/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_account(id):
    account = Account.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    return jsonify({'message': '账目删除成功'}), 200