from flask import Flask
from .models.models import db, migrate
from .routes.routes import api_blueprint
from config import config_map

def create_app(app_env):

    app = Flask(__name__)
    config = config_map.get(app_env, config_map["production"])
    app.config.from_object(app_env[1])
    app.register_blueprint(api_blueprint)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    migrate.init_app(app, db)

    return app
