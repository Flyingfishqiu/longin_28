from flask import session,render_template,current_app,jsonify,request
from . import blu
from info.models import User,News
from info.response_code import RET
from info import constants
from info.utils.comment import user_login_data
from flask import g

@blu.route('/newslist')
def newslist():
    # 获取参数
    cid = request.args.get('cid',1)
    page = request.args.get('page',1)
    per_page = request.args.get('perpage',10)
    # 验证参数
    try:
        cid = int(cid)
        page =int(page)
        per_page =int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    if cid == 1:
        try:
            paginate = News.query.order_by(News.create_time).paginate(page,per_page,False)
        except Exception as e:
            current_app.logger.error(e)
    else:
        try:
            paginate = News.query.filter(News.category_id == cid).order_by(News.create_time.desc()).paginate(page, per_page,False)
        except Exception as e:
            current_app.logger.error(e)

    news_list = paginate.items
    # 4.2 获取总页数：为了实现上拉刷新
    total_page = paginate.pages
    # 4.3 当前在第几页
    current_page = paginate.page

    # 因为json在序列化时，只认得字典或者列表，不认识模型对象列表
    # 所以需要将模型对象列表转成字典列表
    news_dict_List = []
    for news in news_list:
        news_dict_List.append(news.to_basic_dict())

    # 构造响应json数据的字典
    data = {
        'news_dict_List': news_dict_List,
        'total_page': total_page,
        'current_page': current_page
    }

    # 5.响应新闻数据
    return jsonify(errno=RET.OK, errmsg="OK",data=data)

@blu.route('/')
@user_login_data
def index():
    # user_id = session.get('user_id',None)
    # user = None
    # try:
    #     user = User.query.get(user_id)
    #
    # except Exception as e:
    #     current_app.logger.error(e)
    # 查询新文
    news = []
    try:
        news = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)
    context = {
        'user':g.user,
        'news':news
    }

    return render_template('news/index.html',context=context)

@blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')



