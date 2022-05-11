from flask import Flask, render_template, redirect, request, url_for, session
from flask_bootstrap import Bootstrap
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, Email
import json


app = Flask(__name__)

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'lmkvs54ger5fv5$d72v1s3g'
users = {}
user_token = "ugvjvjh"


class LoginForm(FlaskForm):
    """
    Класс формы авторизации.
    """
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    """
    Класс формы регистрации.
    """
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=80)])


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Метод работы с главной страницей. Происходит рендеринг шаблона страницы и отправка данных на сервер.
    :return: шаблон страницы/ответ сервера/перенаправление на страницу авторизации
    """
    datas = []
    sessions_row = []
    request_data = ""

    if request.headers.get("Referer") == "http://127.0.0.1:4000/login":
        for row in session.items():
            sessions_row.append(row[1])
        request_data = request.args['data']
    elif request.headers.get("Referer"):
        sessions_row.append("")

    if request_data in sessions_row:
        if request.method == 'GET':
            return render_template('index.html')
        else:
            response = request.data.decode('utf-8')
            user_data = {}
            i = 0
            for row in json.loads(response)['data']:
                user_data[f"{i}"] = row
                i += 1
            # user_data["token"] = request.args['data']
            response_data = requests.post("http://127.0.0.1:5000/index", data=user_data, verify=False)
            datas = response_data.json()

            return datas
    else:
        return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
def get_login_data():
    """
    Метод авторизации пользователя. Происходит рендеринг шаблона страницы и отправка данных на сервер.
    :return: перенаправление на главную страницу/шаблон страницы
    """
    form = LoginForm()
    if request.method == 'POST':
        data = {}
        data["email"] = str(form.email.data)
        data["password"] = str(form.password.data)
        data["remember"] = bool(form.remember.data)
        response = requests.get("http://127.0.0.1:5000/auth/login", data=data)
        if response.status_code == 200:
            session[data['email']] = response.json()['token']
            user_token = response.json()['token']
            return redirect(url_for("index", data=user_token))

    return render_template('login.html', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    data = {}
    data['email'] = str(form.email.data)
    data['password'] = str(form.password.data)
    data['username'] = str(form.username.data)

    if form.validate_on_submit():
        user = requests.post("http://127.0.0.1:5000/auth/register", data=data)
        if user.status_code == 201:
            return redirect('/')

    return render_template('register.html', form=form)


# @app.route('/logout', methods=['GET'])
# def logout():
#     requests.get("http://127.0.0.1:5000/logout")
#     return redirect("/login")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4000, debug=True)
