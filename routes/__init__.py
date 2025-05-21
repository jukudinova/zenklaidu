from flask import Flask
from config import Config
from extensions import db, migrate
from routes.home_route import home_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_bp)

    return app
