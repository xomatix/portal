import functools

from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for, abort
)
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity

from portal.db import get_db, User

bp = Blueprint('auth', __name__, url_prefix='/api/auth')



@bp.route('/login', methods = ['POST'])
def login(db_session=get_db()):
    username = request.json.get('username', '')
    password = request.json.get('password', '')
    if username is None or password is None:
        abort(400)
    user = db_session.query(User).filter_by(username = username).first()

    if user is None:
        abort(400) 
    if not user.verify_password(password):
        abort(400)
    access = create_access_token(identity=user.id)

    return jsonify({ 'access': access })

@bp.route('/register', methods = ['POST'])
def new_user(db_session=get_db()):
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if db_session.query(User).filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)

    db_session.add(user)
    db_session.commit()
    return jsonify({ 'username': user.username }), 201, {'Location': url_for('portal.get_user', id = user.id, _external = True)}

@bp.route('/delete', methods = ['POST'])
def del_user(db_session=get_db()):
    username = request.json.get('username')
    if username is None:
        abort(400) # missing arguments
    if db_session.query(User).filter_by(username = username).first() is not None:
        user = db_session.query(User).filter_by(username = username).first()
        db_session.delete(user)
        db_session.commit()
    return "deleted"