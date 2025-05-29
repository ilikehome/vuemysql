from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate  # 新增导入
from config import Config

db = SQLAlchemy()
migrate = Migrate()  # 新增迁移实例

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True)
    db.init_app(app)
    migrate.init_app(app, db)  # 新增：关联app和db
    
    from routes import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app