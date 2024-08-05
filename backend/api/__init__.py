import os
import dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DB_NAME = 'worter.db'
ENV_NAME = '.env'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

env_path = os.path.join(BASE_DIR, ENV_NAME)
db_path = os.path.join(BASE_DIR, DB_NAME)

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # App configuration
    app.config['SECRET_KEY'] = dotenv.get_key(env_path, "SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    
    db.init_app(app)
    
    # Blueprints
    from .api import api
    app.register_blueprint(api, url_prefix='/api')
    
    from .models import TelegramUser, GermanWords, WordSeen
    
    create_database(app)
    
    return app

def create_database(app):
    with app.app_context():
        db.create_all()