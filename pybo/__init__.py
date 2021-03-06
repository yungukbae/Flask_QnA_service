from flask import Flask, app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

import config

naming_convention={

    "ix": 'ix_%(column_0_labels)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"

}


db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))                   #전역변수로 db, migrate 객체를 만든 다음 creat_app함수 안에서 init_app메서드를 이용해 초기화했다.
migrate = Migrate()

app = Flask(__name__)

app.config.from_object(config)      #config 파일에 작성한 항목을 app.config환경 변수로 부르기 위해 이 코드를 추가헀다


#ORM  flask db init하기전에 'export FLASK_APP=pybo/__init__.py' 해야 파일 잡음
#모델을 추가하거나 변경할떄는 flask db migrate(모델을 새로 생성하거나 변결할 때 사용) 명령이나 flask db upgrade(모델의 변경 내용을 실제 데이터베이스에 적용할 떄 사용) 명령만을 사용한다.

db.init_app(app)
migrate.init_app(app,db)

if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
    migrate.init_app(app,db,render_as_batch=True)
else:
    migrate.init_app(app,db)


from . import models

from .views import main_views, question_views, answer_views, auth_views, comment_views, vote_views
app.register_blueprint(main_views.bp)
app.register_blueprint(question_views.bp)
app.register_blueprint(answer_views.bp)
app.register_blueprint(auth_views.bp)
app.register_blueprint(comment_views.bp)
app.register_blueprint(vote_views.bp)

from .filter import format_datetime
app.jinja_env.filters['datetime'] = format_datetime

if __name__ == '__main__':
    app.run(debug=True)