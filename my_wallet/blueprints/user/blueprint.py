from flask import Blueprint

from my_wallet.blueprints.user.routes import configure_routes

user_blueprint = Blueprint(
    "user", __name__, template_folder="templates", static_folder="static"
)
configure_routes(user_blueprint)
