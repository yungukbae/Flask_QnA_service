from datetime import datetime
from operator import methodcaller
from flask import Blueprint, url_for,request,render_template
from jinja2.utils import contextfunction
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question, Answer
from ..forms import AnswerForm

bp = Blueprint('answer',__name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>',methods=('POST',))
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now())
        question.answer_set.append(answer)
        db.session.commit()
        return redirect(url_for('question.detail',question_id=question_id))
    return redirect(url_for('question.detail',question_id=question_id))

#form 엘리먼트를 통해 전달된 데이터들은 create 함수에서 request 객체로 얻을 수 있다. request.form['content'] 코드는 POST 폼 방식으로 전송된 데이터 항목 중 name 속성이 'content'인 값을 의미한다.
