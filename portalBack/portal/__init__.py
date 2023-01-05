import os
from flask import Flask
from flask_jwt_extended import JWTManager

def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///instance/portal.sqlite',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER='/images'
    )

    JWTManager(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    app.register_blueprint(db.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import portal
    app.register_blueprint(portal.bp)

    return app