import logging

from flask import Flask
from flask_login import LoginManager
from flask_smorest import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_mailgun import Mailgun
from twilio.rest import Client

from my_wallet.blueprints.api.blueprint import api_blueprint
from my_wallet.blueprints.statistics.blueprint import statistics_blueprint
from my_wallet.blueprints.user.blueprint import user_blueprint
from my_wallet.blueprints.user.fetchers import fetch_user_by
from my_wallet.blueprints.wallet.blueprint import wallet_blueprint
from my_wallet.config import get_config
from my_wallet.utils.config import get_connection_dsn


logging.basicConfig(level=logging.INFO)


def compose_app() -> Flask:
    """Build and return the configured Flask application."""
    app = Flask(__name__)
    app.config.update(get_config())
    app.register_blueprint(user_blueprint, url_prefix="/user")
    app.register_blueprint(wallet_blueprint, url_prefix="/wallet")
    app.register_blueprint(statistics_blueprint, url_prefix="/statistics")

    app.engine = create_engine(  # type: ignore[attr-defined]
        get_connection_dsn(app.config), echo=True, query_cache_size=0
    )  # type: ignore[attr-defined]
    app.session = scoped_session(sessionmaker(app.engine))  # type: ignore[attr-defined]

    app.login_manager = LoginManager()  # type: ignore[attr-defined]
    app.login_manager.init_app(app)  # type: ignore[attr-defined]
    app.login_manager.user_loader(fetch_user_by)  # type: ignore[attr-defined]

    app.mailgun = Mailgun()  # type: ignore[attr-defined]
    app.mailgun.init_app(app)  # type: ignore[attr-defined]

    app.api = Api(app)  # type: ignore[attr-defined]
    app.api.register_blueprint(api_blueprint)  # type: ignore[attr-defined]

    app.twillio_client = Client(  # type: ignore[attr-defined]
        app.config["TWILLIO_SID"], app.config["TWILLIO_AUTH_TOKEN"]
    )  # type: ignore[attr-defined]
    return app
