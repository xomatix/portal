from datetime import datetime, timedelta

from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for, abort
)
from flask_jwt_extended import create_access_token, get_jwt_identity, unset_jwt_cookies, set_access_cookies

from portal.db import get_db, User

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/login', methods = ['POST'])
def login(db_session=get_db()):
    username = request.json.get('username', '')
    password = request.json.get('password', '')
    if username is None or password is None:
        abort(400)
    user = db_session.query(User).filter_by(username = username).first()
    db_session.close()
    if user is None:
        abort(400) 
    if not user.verify_password(password):
        abort(400)
    access = create_access_token(identity=user.id, fresh=True, expires_delta=timedelta(minutes=10))
    response = jsonify({ 'access': access })
    set_access_cookies(response, access)
    return response

@bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@bp.after_request
def refresh(response):
    try:
        access_token = create_access_token(identity=get_jwt_identity())
        set_access_cookies(response, access_token)
        print("refreshed")
        return response
    except (RuntimeError, KeyError):
        return response


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