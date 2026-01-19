from flask import Flask
from .models import db
from .routes import init_routes
from config import app_env

def create_app():

    app = Flask(__name__)
    app.config.from_object(app_env[1])
    db.init_app(app)
    init_routes(app)

    print('-----------------------------------------')
    print(f'Environment configured for {app_env[0]}')
    print('_________________________________________')

    with app.app_context():
        db.create_all()

    return app
