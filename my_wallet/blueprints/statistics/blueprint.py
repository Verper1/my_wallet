from flask import Blueprint

from my_wallet.blueprints.statistics.routes import configure_routes

statistics_blueprint = Blueprint(
    "statistics", __name__, template_folder="templates", static_folder="static"
)
configure_routes(statistics_blueprint)
