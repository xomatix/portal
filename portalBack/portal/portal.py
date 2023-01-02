from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for, abort
)
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

from portal.db import get_db, User, Category

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

@bp.route('/category/create', methods=['POST'])
@jwt_required()
def add_category(db_session=get_db()):
    name = request.json.get('name')
    description = request.json.get('description')
    if db_session.query(Category).filter_by(name=name).first() is not None:
        return jsonify({ 'data': 'Not created already exists!' })
    category = Category(name=name, description=description)
    db_session.add(category)
    db_session.commit()
    db_session.close()
    return jsonify({ 'data': f'Created {name} category!' })

@bp.route('/category', methods=['GET'])
@jwt_required()
def get_categories(db_session=get_db()):
    categories = db_session.query(Category).all()
    db_session.close()
    categories = [i.__dict__ for i in categories]
    categories = [{'name': i['name'], 'description': i['description']} for i in categories]
    #c = json.dumps(categories[0]) 
    print(categories )
    
    return jsonify({ 'data': categories})