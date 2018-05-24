from flask import  Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
# 配置信息
class Config(object):
    SQLALCHEMY_DATABASE_URI='mysql://root:mysql@127.0.0.1:3306/information_28'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = '6379'

app = Flask(__name__)
db = SQLAlchemy(app)
#创建redis连接对象
stict = StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_HOST)
# 加载配置信息
app.config.from_object(Config)
@app.route('/')
def index():
    return "index"

if __name__ == '__main__':
    app.run()