from flask import session, Flask, request, jsonify, make_response
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import jwt
from datetime import datetime, timedelta
from src.game import GameOfLife


app = Flask(__name__)  # Создание приложения Flask.
app.debug = True

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'lnkwfnwnldnv4s46s4dvs5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


db.create_all()


@app.route('/index', methods=['POST'])
def index():
    """
    Метод работы с главной страницей.
    :return: шаблон главной страницы
    """
    game = GameOfLife()
    states = game.game(request)
    return {"data": states}


@app.route('/auth/login', methods=['POST', 'GET'])
def login():
    """
    Метод с авторизацией пользователя.
    :return: ответ сервера, обёрнутый в статус-код
    """
    auth = request.form

    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response('Could not verify', 401)

    user = Users.query.filter_by(email=auth.get('email')).first()

    if not user or not check_password_hash(user.password, auth.get('password')):
        return make_response('Could not verify', 401)

    token = jwt.encode({
        'public_id': user.id,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }, app.config['SECRET_KEY'])

    session[auth.get('email')] = token

    return make_response(jsonify({'token': token}), 200)


@app.route('/auth/register', methods=['POST', 'GET'])
def register():
    """
    Метод с регистрацией пользователя.
    :return: ответ сервера, обёрнутый в статус-код
    """
    auth = request.form

    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response('Could not verify', 401)

    if not Users.query.filter_by(email=auth.get('email')).first():
        hashed_password = generate_password_hash(auth.get('password'), method='sha256')
        new_user = Users(username=auth.get('username'), email=auth.get('email'), password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        token = jwt.encode({
            'public_id': new_user.id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        session[auth.get('email')] = token

    return make_response(jsonify({'token': token}), 201)


if __name__ == "__main__":
    app.run()
