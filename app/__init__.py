from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, jwt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from .routes.auth import auth_bp
    from .routes.transactions import transactions_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(
        transactions_bp,
        url_prefix="/api/transactions"
    )

    @app.get("/")
    def home():
        return {
            "message": "Personal Finance REST API",
            "status": "running"
        }

    @app.get("/api/health")
    def health_check():
        return {
            "status": "healthy"
        }

    with app.app_context():
        db.create_all()

    return app