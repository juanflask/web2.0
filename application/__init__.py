from flask import Flask
import os


def init_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'database.db')
    )

    with app.app_context():
        from . import route
        app.register_blueprint(route.mainpages_bp)
        app.register_blueprint(route.auth_bp)

    return app
