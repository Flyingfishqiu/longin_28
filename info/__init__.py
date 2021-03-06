from logging.handlers import RotatingFileHandler
from config import deta_config
from flask import  Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
from redis import StrictRedis
import logging
from flask_wtf import csrf

db = SQLAlchemy()

session_redis = None

def con(conf):
    Longing(conf)
    app = Flask(__name__)
    app.config.from_object(deta_config[conf])
    # 创建redis连接对象
    global session_redis
    session_redis = StrictRedis(host=deta_config[conf].REDIS_HOST, port=deta_config[conf].REDIS_PORT,decode_responses=True)
    from .modules.index import blu
    app.register_blueprint(blu)
    from .modules.passport import passport_blue
    app.register_blueprint(passport_blue)
    from .modules.news import news_blue
    app.register_blueprint(news_blue)
    from info.utils.comment import do_rank
    app.add_template_filter(do_rank,'rank')
    Session(app)
    CSRFProtect(app)
    @app.after_request
    def after(respose):
        # 生成csrf随机值
        csrf_token = csrf.generate_csrf()
        # 将csrf_toke写入cookie
        respose.set_cookie('csrf_token',csrf_token)
        return respose

    db.init_app(app)
    return app


def Longing(conf):
    # 设置日志的记录等级
    logging.basicConfig(level=deta_config[conf].CONFIG_LEVEL) # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*10, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)