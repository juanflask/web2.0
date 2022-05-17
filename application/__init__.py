from flask import Flask
from flask_login import LoginManager
from .models import User
from application.bd import get_db_connection, close_db

import os


def init_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'database.db')
    )

    login_manager = LoginManager()
    login_manager.login_view = "auth_bp.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        conn = get_db_connection()
        curs = conn.cursor()
        curs.execute("SELECT * from login_usuario where id = (?)",[user_id])
        lu = curs.fetchone()
        close_db()
        if lu is None:
            return None
        else:
            return User(lu[0], lu[1], lu[2], lu[3])

    with app.app_context():
        from . import route
        app.register_blueprint(route.mainpages_bp)
        app.register_blueprint(route.auth_bp)

    return app

