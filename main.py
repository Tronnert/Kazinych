from flask import Flask
from data import db_session
from data.users import User
from forms.user import RegisterForm
from flask import render_template, redirect, make_response, jsonify, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.user import LoginForm, UploadForm
import requests
from api import user_api
from werkzeug.utils import secure_filename
import os
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'static/img'
login_manager = LoginManager()
app.register_blueprint(user_api.blueprint)
login_manager.init_app(app)


def check_filename(filename):
    return all(map(lambda x: x in string.ascii_letters + string.digits + ".", filename))


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main_page():
    return render_template("main.html", title="Прибежище афериста")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def make_map_image():
    toponym_to_find = "Кипр"
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    delta = "1.5"
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": "map"
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    map_file = "static/img/map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


@app.route('/about')
def about():
    return render_template('about.html', title='О нас')


# @app.route('/game')
# @login_required
# def first_game():
#     return post('http://localhost:8080/api/user', json={'bet': 100, 'game_name': 'first', 'id': current_user.id, 'password': current_user.hashed_password}).json()


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = UploadForm()
    mes = ""
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext in app.config['UPLOAD_EXTENSIONS']:
                if check_filename(filename):
                    filename = str(current_user.id) + "." + file_ext
                    uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                    db_sess = db_session.create_session()
                    user = db_sess.query(User).filter(User.id == current_user.id).first()
                    user.image = filename
                    db_sess.commit()
                    return redirect("/profile")
                else:
                    mes = "В имени файла есть некоректные символы"
    return render_template('profile.html', title='Профиль', form=form, message=mes)


@app.route('/roulette')
def roulette():
    return render_template('roulette.html', title='Рулетка', current_user=current_user)


@app.route('/cyber_roulette')
def roulette2():
    return render_template('roulette2.html', title='Рулетка', current_user=current_user)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/cyber_roulette')
def cyber_roulette():
    return render_template('roulette2.html', title='Кибер рулетка', current_user=current_user)


def main():
    make_map_image()
    if not os.path.exists("db"):
        os.mkdir("db")
    db_session.global_init("db/casino.db")
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
