from datetime import datetime
from operator import methodcaller
from flask import Blueprint, url_for,request,render_template,g,flash
from jinja2.utils import contextfunction
from werkzeug.utils import redirect
from .auth_views import login, login_required
from pybo import db
from pybo.models import Question, Answer
from ..forms import AnswerForm

bp = Blueprint('answer',__name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>',methods=('POST',))
@login_required
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        question.answer_set.append(answer)
        db.session.commit()
        return redirect('{}#answer_{}'.format(
            url_for('question.detail',question_id=question_id), answer.id))
    return redirect(url_for('question.detail',question_id=question_id))

#form 엘리먼트를 통해 전달된 데이터들은 create 함수에서 request 객체로 얻을 수 있다. request.form['content'] 코드는 POST 폼 방식으로 전송된 데이터 항목 중 name 속성이 'content'인 값을 의미한다.
@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=answer.question.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#answer_{}'.format(
            url_for('question.detail',question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', answer=answer, form=form)

@bp.route('/delete/<int:answer_id>')
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제 권한이 없습니다.')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))