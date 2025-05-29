from datetime import datetime
from app import db
import bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)  # 保持字段名不变但存储明文
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str):
        self.password_hash = password  # 直接存储明文

    def check_password(self, password: str):
        return self.password_hash == password  # 直接比较明文

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.Enum('income', 'expense', name='account_type'), nullable=False)  # 确保枚举值正确
    remark = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('accounts', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)