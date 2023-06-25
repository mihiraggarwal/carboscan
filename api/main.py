import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24)

db = SQLAlchemy(app)

# Comment this during production
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

from api.models.product import Product

def create_app(test_config=None):
    
    with app.app_context():
        db.create_all()

    from api import index
    app.register_blueprint(index.bp, url_prefix='/')

    from api import search
    app.register_blueprint(search.bp, url_prefix='/search')

    from api import result
    app.register_blueprint(result.bp, url_prefix='/result')
      
    return app

app = create_app()