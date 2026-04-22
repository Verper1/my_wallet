from flask_smorest import Blueprint

from my_wallet.blueprints.api.routes import configure_routes


api_blueprint = Blueprint("api", "api", url_prefix="/api")
configure_routes(api_blueprint)
