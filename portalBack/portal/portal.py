from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for, abort
)
from flask_jwt_extended import jwt_required, get_jwt_identity

from portal.db import get_db, User, Category, Post

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

#POST FUNCTIONS

@bp.route('/post/create', methods=['POST'])
@jwt_required()
def add_post(db_session=get_db()):
    title = request.json.get('title', '')
    description = request.json.get('description', '')
    category_id = request.json.get('category_id', '')
    if db_session.query(Post).filter_by(title=title).first() is not None:
        return jsonify({ 'data': 'Not created already exists!' })
    post = Post(title=title, description=description, category_id=category_id)
    db_session.add(post)
    db_session.commit()
    db_session.close()
    return jsonify({ 'data': f'Created {title} post!' })

@bp.route('/post/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def delete_post(id=id, db_session=get_db()):
    p = db_session.query(Post).filter_by(id=id).first()
    if p is not None:
        db_session.delete(p)
        db_session.commit()
        db_session.close()
        return jsonify({ 'data': f'Deleted {p.title} post!' })
    
    return jsonify({ 'data': 'Already not exists!' })

@bp.route('/post/<int:id>', methods=['PUT'])
@jwt_required()
def edit_post(id=id, db_session=get_db()):
    p = db_session.query(Post).filter(Post.id == id).first()
    title = request.json.get('title', '')
    description = request.json.get('description', '')
    category_id = request.json.get('category_id', '')
    if p is not None:
        p.title = title
        p.description = description
        p.category_id = category_id
        db_session.commit()
        return jsonify({ 'data': f'Updated {p.title} post!' })
    
    return jsonify({ 'data': 'Already not exists!' })

@bp.route('/post', methods=['GET'])
def get_posts(db_session=get_db()):
    posts = db_session.query(Post).all()
    db_session.close()
    posts = [i.__dict__ for i in posts]
    posts = [{'id': i['id'], 'title': i['title'], 'description': i['description'], 'category_id': i['category_id']} for i in posts]
    
    return jsonify({ 'data': posts})

#CATEGORY FUNCTIONS

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

@bp.route('/category/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def delete_category(id=id, db_session=get_db()):
    c = db_session.query(Category).filter_by(id=id).first()
    if c is not None:
        db_session.delete(c)
        db_session.commit()
        db_session.close()
        return jsonify({ 'data': f'Deleted {c.name} category!' })
    
    return jsonify({ 'data': 'Already not exists!' })

@bp.route('/category/<int:id>', methods=['PUT'])
@jwt_required()
def edit_category(id=id, db_session=get_db()):
    c = db_session.query(Category).filter(Category.id == id).first()
    name = request.json.get('name')
    description = request.json.get('description')
    if c is not None:
        c.name = name
        c.description = description
        db_session.commit()
        return jsonify({ 'data': f'Updated {c.name} category!' })
    
    return jsonify({ 'data': 'Already not exists!' })

@bp.route('/category', methods=['GET'])
def get_categories(db_session=get_db()):
    categories = db_session.query(Category).all()
    db_session.close()
    categories = [i.__dict__ for i in categories]
    categories = [{'id': i['id'], 'name': i['name'], 'description': i['description']} for i in categories]
    
    return jsonify({ 'data': categories})