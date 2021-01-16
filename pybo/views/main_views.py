from flask import Blueprint, render_template
from flask.helpers import url_for
from werkzeug.utils import redirect
from pybo.models import Question

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return 'this is main_views'
    
@bp.route('/')
def index():
    return redirect(url_for('question._list')) 
    
    #question._list는 question, _list순서로 해석되어 함수명을 찾아준다. question은 등록된 블루프린트 이름, _list는 블루프린트에 등록된 함수명이라고 생각하면 된다. 현재 _list 함수에 등록된 라우트는 @bp.route('/list/') 이므로 url_for('question._list')는 bp의 접두어인 /question/과 /list/가 더해진 /quesiton/list/ URL을 반환한다.

