from flask import Flask
from flask import url_for
from flask import request
from flask import render_template
from flask import redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def main():
    return "Start"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
