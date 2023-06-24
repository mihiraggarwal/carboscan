import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'

db = SQLAlchemy(app)

# Comment this during production
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def create_app(test_config=None):
    
    with app.app_context():
        db.create_all()

    from package import index
    app.register_blueprint(index.bp, url_prefix='/')
      
    return app

app = create_app()