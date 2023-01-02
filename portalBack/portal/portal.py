from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for, abort
)
from flask_jwt_extended import jwt_required, get_jwt_identity

from portal.db import get_db, User

bp = Blueprint('portal', __name__, url_prefix='/api')

@bp.route('/', methods = ['GET'])
def index(session=get_db()):
    
    return jsonify({ 'indexpage': "sample index page content" })

@bp.route('/users/<int:id>')
def get_user(id, session=get_db()):
    user = session.query(User).filter_by(id = id).first()
    if not user:
        abort(400)
    print(g.user)
    return jsonify({ 'username': user.username, 'user': 'g.user' })

@bp.route('/resource', methods=['GET'])
@jwt_required()
def get_resource(db_session=get_db()):
    user_id = get_jwt_identity()
    user = db_session.query(User).filter_by(id = user_id).first()
    db_session.close()
    return jsonify({ 'data': f'Hello, {user.username}!' })