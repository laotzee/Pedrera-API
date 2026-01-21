from flask import Flask
from .models.models import db, migrate
from .routes.routes import api_blueprint

def create_app(app_env):

    app = Flask(__name__)
    app.config.from_object(app_env[1])
    app.register_blueprint(api_blueprint)
    db.init_app(app)
    migrate.init_app(app, db)

    return app
