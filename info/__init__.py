from logging.handlers import RotatingFileHandler
from config import deta_config
from flask import  Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
import logging

db = SQLAlchemy()


def con(conf):
    Longing(conf)
    app = Flask(__name__)
    app.config.from_object(deta_config[conf])
    Session(app)
    CSRFProtect(app)
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