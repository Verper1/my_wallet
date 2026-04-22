from flask import Blueprint

from my_wallet.blueprints.wallet.routes import configure_routes

wallet_blueprint = Blueprint(
    "wallet", __name__, template_folder="templates", static_folder="static"
)
configure_routes(wallet_blueprint)
