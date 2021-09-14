import os
from flask import Flask
from flask_cors import CORS

from app.database import init_database

def create_app(appname: str = None, config: dict = {}) -> Flask:
    appname = appname if appname else __name__    
    app = Flask(appname)        
    app.config.from_object(f'app.config.{os.environ.get("FLASK_ENV").capitalize()}')

    init_database(app)
    
    from app.blueprint import bp
    app.register_blueprint(bp)

    # Cross-origin Resource Sharing (CORS)
    cors = CORS(
        app,
        resources={r"/*"},
        origins="*",
        headers=["Content-Type", "Authorization", "api_key"],
        allow_headers=["Content-Type", "Authorization", "api_key"],
        expose_headers=["Content-Type", "Authorization", "api_key"],
        support_credentials=True,
    )       

    return app