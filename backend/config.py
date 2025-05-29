import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://shenhao:shenhaO123#@rm-bp18m5mdhgk22t81lxo.mysql.rds.aliyuncs.com/vuemysql"
    SQLALCHEMY_TRACK_MODIFICATIONS = False