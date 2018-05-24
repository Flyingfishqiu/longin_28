from flask import  Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf import CSRFProtect
from flask import session
from flask_session import Session
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
# 配置信息
class Config(object):
    SECRET_KEY = 'q7pBNcWPgmF6BqB6b5VICF7z7pI+90o0O4CaJsFGjzRsYiya9SEgUDytXvzFsIaR'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI='mysql://root:mysql@127.0.0.1:3306/information_28'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = '6379'
    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True
    # 创建redis连接对象
    SESSION_REDIS = StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    # 设置

    PERMANENT_SESSION_LIFETIME = 60*60*1
app = Flask(__name__)

# 加载配置信息
app.config.from_object(Config)
Session(app)
CSRFProtect(app)
db = SQLAlchemy(app)
manage = Manager(app)
Migrate(app,db)
manage.add_command('mysql',MigrateCommand)

@app.route('/')
def index():
    session['name'] = 'qsj'
    return "index"

if __name__ == '__main__':
    manage.run()