import re
from flask import abort,make_response,json,jsonify,current_app,session
from info.constants import IMAGE_CODE_REDIS_EXPIRES
from info.response_code import RET
from info.utils.captcha.captcha import captcha
from . import passport_blue
from flask import request
from info import session_redis,db
import logging
import random
import datetime
from info.libs.yuntongxun.sms import CCP
from info.models import User

# 退出登陆
@passport_blue.route('/logout',methods=['POST'])
def logout():
    session.pop('user_id')
    session.pop('nick_name')
    session.pop('mobile')
    return jsonify(errno=RET.OK, errmsg="ok")

# 登陆
@passport_blue.route('/long',methods=['POST'])
def long():
    # 获取参数
    json_dict = request.json
    mobile = json_dict.get('mobile')
    password = json_dict.get('password')
    if not all([mobile,password]):
        return jsonify(errno=RET.PARAMERR, errmsg="缺省参数")
    if not (re.match('^1[3-8]\d{9}$', mobile)):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式错误")
    # 查询参数
    try:
        user = User.query.filter(User.mobile == mobile).first()

    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(errno=RET.PARAMERR, errmsg="用户名或密码错误")
    if not user:
        return jsonify(errno=RET.NODATA, errmsg="用户名不存在")
    if not user.check_passowrd(password):
        return jsonify(errno=RET.NODATA, errmsg="用户名不存在")

    session['user_id'] = user.id
    session['nick_name'] = user.nick_name
    session['mobile'] = user.mobile
    try:
        user.last_login = datetime.datetime.now()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="更新时间失败")
    return jsonify(errno=RET.OK, errmsg="ok")

@passport_blue.route('/image_cold')
def image_cold():
    # 1获取请求参数
    imageCodeId = request.args.get('imageCodeId')
    # 2.验证请求参数
    if not imageCodeId:
        abort(403)
    # 3.生成验证码
    name,text,image = captcha.generate_captcha()
    try:
        # 4.存储验证码
        session_redis.set('imageCode'+imageCodeId,text,IMAGE_CODE_REDIS_EXPIRES)
        current_app.logger.debug(text)
    except Exception as e:
        logging.error("验证码存储错误")
        return RET.SESSIONERR
    # 修改验证码为png格式
    response = make_response(image)
    response.headers['Content-Type'] = 'image/jpg'
    # 5.返回验证码
    return response

@passport_blue.route('/sms_code', methods=['POST'])
def sms_code():
    # 获取请求参数
    requ_data = request.data
    json_str = json.loads(requ_data)
    mobile = json_str.get('mobile')
    imageCode = json_str.get('imageCode')
    imageCode_ID = json_str.get('imageCode_ID')
    # 验证参数是否存在
    if not all([mobile,imageCode,imageCode_ID]):
        return jsonify(errno = RET.PARAMERR,errmsg = "参数错误")
    if not (re.match('^1[3-8]\d{9}$',mobile)):
        return jsonify(errno = RET.PARAMERR,errmsg = "手机号格式错误")
    #从数据库中获取
    try:
        redis_imageCode_ID = session_redis.get('imageCode'+imageCode_ID)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR,errmsg = "验证码错误")
    if not redis_imageCode_ID:
        return jsonify(errno = RET.NODATA,errmsg = "验证码不存在")
    # 与客户端的验证码比较
    if redis_imageCode_ID.lower() != imageCode.lower():
        return jsonify(errno = RET.PARAMERR,errmsg = "验证码输入不一致")
    sms_code = "%06d"%random.randint(0,999999)
    current_app.logger.debug(sms_code)
    # 调用cpp发送短信
    # sms = CCP().send_template_sms(mobile, [sms_code, '5'], '1')
    # if sms != 0:
    #     return jsonify(errno=RET.THIRDERR, errmsg="验证码发送失败")
    try:
        session_redis.set("sms:"+mobile,sms_code,IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="短信存储错误")

    return jsonify(errno = RET.OK,errmsg = "验证码发送成功")

# 注册
@passport_blue.route('/longin',methods=['POST'])
def longin():
    # 获取请求参数
    json_dic = request.json
    mobile = json_dic.get('mobile')
    smscode = json_dic.get('smscode')
    password = json_dic.get('password')
    # 验证参数是否存在
    if not all([mobile,smscode,password]):
        return   jsonify(errno=RET.NODATA, errmsg="缺少参数")
    if not (re.match('^1[3-8]\d{9}$',mobile)):
        return jsonify(errno = RET.PARAMERR,errmsg = "手机号格式错误")
    # 从数据库中获取验证码
    try:
        sms_code_server = session_redis.get("sms:"+mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="短信验证码错误")
    if not sms_code_server:
        return jsonify(errno=RET.NODATA, errmsg="短信验证码不存在")

    if sms_code_server != smscode:
        return jsonify(errno=RET.PARAMERR, errmsg="验证码输入有误")
    else:
        user = User()
        user.mobile = mobile
        user.nick_name = mobile
        user.password = password
        user.last_login =datetime.datetime.now()

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="存入数据库错误")

    # 存入session中
    session['user_id']=user.id
    session['nick_name'] = user.nick_name
    session['mobile'] = user.mobile


    return jsonify(errno=RET.OK, errmsg='ok')
