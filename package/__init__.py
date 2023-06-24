from flask import Flask

app = Flask(__name__, instance_relative_config=True)

def create_app(test_config=None):
    @app.route('/', methods=['GET'])
    def index():
        return "Hello world"
    
    return app

app = create_app()