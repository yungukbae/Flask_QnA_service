from flask import Blueprint, render_template
from pybo.models import Question

bp = Blueprint('question',__name__, url_prefix='/question')

@bp.route('/list/')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc()) 
    #Question.query.order_by(Question.create_date.desc()) => Question.qeury.order_by(create_date의 desc(역순)으로 정렬해라)
    #Question.query.order_by(Question.create_date.asc()) => 작성 일시 순으로 정렬해라
    return render_template('question/question_list.html',question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id) #get_or_404는 해당 데이터를 찾을 수 없는 경우 404페이지를 출력해준다.
    return render_template('question/question_detail.html',question=question)