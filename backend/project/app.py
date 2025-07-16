import os
from flask import Flask
from auth import auth_bp
from routes import main_bp
from database import db
from extensions import bcrypt

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    db_path = os.path.join(app.instance_path, "users.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SECRET_KEY"] = "changeme"

    os.makedirs(app.instance_path, exist_ok=True)  # crea la cartella se non esiste

    bcrypt.init_app(app)
    db.init_app(app)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
