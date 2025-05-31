from datetime import datetime
from app import db  # 修改导入路径

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.Enum('income', 'expense', name='account_type'), nullable=False)
    remark = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('accounts', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)