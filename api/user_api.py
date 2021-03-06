import flask
from flask import jsonify

import maps
from data import db_session
from data.users import User
from data.balance_changes import BalanceChanges
from random import choice
from flask import request
from .games import games_dict
import datetime
from maps import maps_dict

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/game/', methods=['GET', 'POST'])
def games_balance_update():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['game_name', 'bet', 'id', 'password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    current_user = db_sess.query(User).filter(User.id == request.json['id']).first()
    if current_user.hashed_password != request.json['password']:
        return jsonify({'error': 'Wrong password'})
    current_user.balance -= int(request.json['bet'])
    win, ch = games_dict[request.json['game_name']].get_win(request.json)
    current_user.balance += win
    new_note = BalanceChanges(game_name=request.json['game_name'],
                              content='ok',
                              change=win - int(request.json['bet']),
                              user=current_user)
    current_user.balance_changes_rel.append(new_note)
    db_sess.commit()
    return jsonify({'win': win,
                    'choice': ch,
                    'success': 'ok',
                    'bet': request.json['bet']})


@blueprint.route('/api/move/', methods=['GET', 'POST'])
def move():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['move']):
        return jsonify({'error': 'Bad request'})
    maps_dict['map'].move(request.json['move'])
    return jsonify({})


@blueprint.route('/api/move1/', methods=['GET', 'POST'])
def move1():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['move']):
        return jsonify({'error': 'Bad request'})
    maps_dict['map1'].move(request.json['move'])
    return jsonify({})


@blueprint.route('/api/cheat/', methods=['GET', 'POST'])
def cheat_balance_update():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'password', 'change']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    current_user = db_sess.query(User).filter(User.id == request.json['id']).first()
    if current_user.hashed_password != request.json['password']:
        return jsonify({'error': 'Wrong password'})
    current_user.balance += int(request.json['change'])
    new_note = BalanceChanges(game_name="cheating",
                              content='ok',
                              change=int(request.json['change']),
                              user=current_user)
    current_user.balance_changes_rel.append(new_note)
    db_sess.commit()
    return jsonify({'success': 'ok',
                    'date': str(datetime.datetime.now().strftime("%H:%M %d.%m.%y"))})


@blueprint.route('/api/emailsettings', methods=['POST', 'GET'])
def emailsettings():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'password', 'change']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    current_user = db_sess.query(User).filter(User.id == request.json['id']).first()
    if current_user.hashed_password != request.json['password']:
        return jsonify({'error': 'Wrong password'})
    if current_user.email_flag:
        current_user.email_flag = False
    else:
        current_user.email_flag = True
    print(current_user.email_flag)
    db_sess.commit()
    return jsonify({'success': 'ok', 'date': str(datetime.datetime.now().strftime("%H:%M %d.%m.%y"))})
