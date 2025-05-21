from flask import Flask
from config import Config
from extensions import db, migrate
from routes.home_route import home_bp  # Blueprint tvarkesnis kelio registravimas

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprint
    app.register_blueprint(home_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
