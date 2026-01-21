from flask import Flask
from .models import db
from .routes.routes import api_blueprint

def create_app(app_env):

    app = Flask(__name__)
    app.config.from_object(app_env[1])
    app.register_blueprint(api_blueprint)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
