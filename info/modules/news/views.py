from . import news_blue
from info.utils.comment import user_login_data
from flask import render_template


@news_blue.route('/news/<int:id>')
@user_login_data
def news(id):
    return render_template('news/detail.html')

