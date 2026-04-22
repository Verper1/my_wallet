from flask_smorest import Blueprint


def configure_routes(blueprint: Blueprint) -> None:
    from my_wallet.blueprints.api.views import WalletsView, WalletView
    from my_wallet.blueprints.api.views import TransactionsView, TransactionView

    blueprint.add_url_rule(
        "/api/wallets", view_func=WalletsView, methods=["GET", "POST"]
    )
    blueprint.add_url_rule(
        "/api/wallet/<int:wallet_id>",
        view_func=WalletView,
        methods=["GET", "PUT", "DELETE"],
    )
    blueprint.add_url_rule(
        "/api/wallet/<int:wallet_id>/transactions",
        view_func=TransactionsView,
        methods=["GET", "POST"],
    )
    blueprint.add_url_rule(
        "/api/wallet/<int:wallet_id>/transaction/<int:transaction_id>",
        view_func=TransactionView,
        methods=["GET", "PUT", "DELETE"],
    )
