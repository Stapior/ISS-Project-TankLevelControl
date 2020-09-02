from flask import Flask
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap

from .frontend import frontend
from .nav import nav


def create_app(configfile=None):
    app = Flask(__name__)

    AppConfig(app)
    Bootstrap(app)

    app.register_blueprint(frontend)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

    nav.init_app(app)

    return app
