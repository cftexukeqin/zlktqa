import os

# 数据库连接配置
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'zlktqa_demo'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
#str = "mysql+pymysql://root:123456@localhost:3306/db_demo5?charset=utf8"

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# debug 开启
DEBUG = True
# session 设置
SECRET_KEY = os.urandom(24)