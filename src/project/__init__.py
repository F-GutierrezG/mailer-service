import os
from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt

from project.views.health import health_blueprint
from project.views.mail import mail_blueprint


bcrypt = Bcrypt()


def register_blueprints(app):
    app.register_blueprint(health_blueprint)
    app.register_blueprint(mail_blueprint)


def create_app(script_info=None):
    app = Flask(__name__)

    CORS(app)

    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    bcrypt.init_app(app)

    register_blueprints(app)

    @app.shell_context_processor
    def ctx():
        return {'app': app}

    return app
