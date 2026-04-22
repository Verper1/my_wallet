from typing import Any

from flask import abort
from flask.views import MethodView
from flask_login import current_user

from my_wallet.blueprints.api.blueprint import api_blueprint
from my_wallet.blueprints.api.schemas import WalletSchema, TransactionSchema
from my_wallet.blueprints.wallet.changers import create, update, delete
from my_wallet.blueprints.wallet.fetchers import (
    fetch_wallets_for,
    get_wallet_by,
    fetch_transactions_for,
    get_transaction_by,
)
from my_wallet.blueprints.wallet.models import Wallet, Transaction


class WalletsView(MethodView):
    @api_blueprint.response(200, WalletSchema(many=True))
    def get(self) -> Any:
        """List wallets of the current user."""
        return fetch_wallets_for(current_user)

    @api_blueprint.arguments(WalletSchema)
    @api_blueprint.response(201, WalletSchema)
    def post(self, wallet_data: dict) -> Any:
        """Create a new wallet."""
        wallet = create(
            Wallet(
                title=wallet_data["title"],
                status=wallet_data["status"],
                owned_by_user_id=current_user.id,
            ),
        )
        return wallet


class WalletView(MethodView):
    @api_blueprint.response(200, WalletSchema)
    def get(self, wallet_id: int) -> Any:
        """Get a wallet by id."""
        wallet = get_wallet_by(wallet_id)
        if wallet is None:
            abort(404)
        return wallet

    @api_blueprint.arguments(WalletSchema)
    @api_blueprint.response(201, WalletSchema)
    def put(self, wallet_data: dict, wallet_id: int) -> Any:
        """Update an existing wallet."""
        wallet = get_wallet_by(wallet_id)
        if wallet is None:
            abort(404)
        wallet.title = wallet_data["title"]  # type: ignore[union-attr]
        wallet.status = wallet_data["status"]  # type: ignore[union-attr]
        update(wallet)
        return wallet

    def delete(self, wallet_id: int) -> Any:
        """Delete a wallet by id."""
        wallet = get_wallet_by(wallet_id)
        if wallet is None:
            abort(404)
        delete(wallet)
        return {}


class TransactionsView(MethodView):
    @api_blueprint.response(200, TransactionSchema(many=True))
    def get(self, wallet_id: int) -> Any:
        """List transactions of the wallet."""
        return fetch_transactions_for(wallet_id)

    @api_blueprint.arguments(TransactionSchema)
    @api_blueprint.response(201, TransactionSchema)
    def post(self, wallet_id: int, transaction_data: dict) -> Any:
        """Create a new transaction in the wallet."""
        transaction = create(
            Transaction(
                wallet_id=wallet_id,
                timestamp=transaction_data["timestamp"],
                amount=transaction_data["amount"],
                currency=transaction_data["currency"],
                description=transaction_data["description"],
            )
        )
        return transaction


class TransactionView(MethodView):
    @api_blueprint.response(200, TransactionSchema)
    def get(self, wallet_id: int, transaction_id: int) -> Any:
        """Get a transaction by id."""
        transaction = get_transaction_by(transaction_id)
        if transaction is None or transaction.wallet_id != wallet_id:
            abort(404)
        return transaction

    @api_blueprint.arguments(TransactionSchema)
    @api_blueprint.response(201, TransactionSchema)
    def put(self, transaction_data: dict, wallet_id: int, transaction_id: int) -> Any:
        """Update an existing transaction."""
        transaction = get_transaction_by(transaction_id)
        if transaction is None or transaction.wallet_id != wallet_id:
            abort(404)
        transaction.timestamp = transaction_data["timestamp"]  # type: ignore[union-attr]
        transaction.amount = transaction_data["amount"]  # type: ignore[union-attr]
        transaction.currency = transaction_data["currency"]  # type: ignore[union-attr]
        transaction.description = transaction_data["description"]  # type: ignore[union-attr]
        update(transaction)
        return transaction

    def delete(self, wallet_id: int, transaction_id: int) -> Any:
        """Delete a transaction by id."""
        transaction = get_transaction_by(transaction_id)
        if transaction is None or transaction.wallet_id != wallet_id:
            abort(404)
        delete(transaction)
        return {}
