from datetime import datetime
from flask import Blueprint, render_template, request,url_for
from werkzeug.utils import redirect
from .. import db
from ..models import Answer, Question
from ..forms import QuestionForm, AnswerForm


bp = Blueprint('question',__name__, url_prefix='/question')

@bp.route('/list/')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc()) 
    #Question.query.order_by(Question.create_date.desc()) => Question.qeury.order_by(create_date의 desc(역순)으로 정렬해라)
    #Question.query.order_by(Question.create_date.asc()) => 작성 일시 순으로 정렬해라
    return render_template('question/question_list.html',question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id) #get_or_404는 해당 데이터를 찾을 수 없는 경우 404페이지를 출력해준다.
    return render_template('question/question_detail.html',question=question, form=form)

@bp.route('/create/',methods=('GET','POST'))
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
            question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('main.index'))
    return render_template('question/question_form.html',form=form)

