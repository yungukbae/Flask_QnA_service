from enum import unique
from re import T
from sqlalchemy.orm import backref, create_session
from pybo import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200),nullable=False)
    content = db.Column(db.Text(),nullable=False)
    create_date = db.Column(db.DateTime(),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User',backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id',ondelete='CASCADE'))     #db.ForeignKey에 지정한 첫 번째 값은 연결한 모델의 속성명이고 두 번째 ondelete에 지정한 값은 삭제 연동 설정이다. 즉, 답변 모델의 quesion_id 속성은 질문 모델의 id 속성과 연결되며 ondelete='CASCADE'에 의해 데이터베이스에서 쿼리를 이용하여 질문을 삭제하면 해당 질문에 달린 답변도 함꼐 삭제된다.
    question = db.relationship('Question',backref=db.backref('answer_set'))  #quesion속성은 답변 모델에서 질문 모델을 참조하기 위해 추가했다. 예를 들어 답변 모델 객체에서 질문 모델 객체의 제목을 참조하려면 answer.question.subject처럼 할 수 있다. 이렇게 하려면 속성을 추가할 때 db.Column이 아닌 db.relationship을 사용해야한다.
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User',backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)  #unique는 같은 값을 저장할 수 없다는 뜻이다.
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)

