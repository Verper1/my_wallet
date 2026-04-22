from flask import current_app
from sqlalchemy import select, or_

from my_wallet.blueprints.user.models import User
from my_wallet.blueprints.wallet.enums import WalletStatus
from my_wallet.blueprints.wallet.models import Wallet, Transaction


def fetch_wallets_for(user: User) -> list[Wallet]:
    """Return all active wallets the user owns or has access to."""
    wallets = current_app.session.execute(  # type: ignore[attr-defined]
        select(Wallet).where(
            Wallet.status == WalletStatus.ACTIVE,
            or_(
                Wallet.owned_by_user_id == user.id,
                Wallet.users_with_access.any(User.id == user.id),
            ),
        )
    ).fetchall()
    return [w[0] for w in wallets]


def get_wallet_by(wallet_id: int) -> Wallet | None:
    """Return the wallet with the given id or None."""
    wallet_row = current_app.session.execute(  # type: ignore[attr-defined]
        select(Wallet).where(Wallet.id == wallet_id)
    ).fetchone()
    return wallet_row[0] if wallet_row else None


def fetch_transactions_for(wallet_id: int) -> list[Transaction]:
    """Return all transactions belonging to the wallet."""
    transactions = current_app.session.execute(  # type: ignore[attr-defined]
        select(Transaction).where(Transaction.wallet_id == wallet_id)
    ).fetchall()
    return [w[0] for w in transactions]


def get_transaction_by(transaction_id: int) -> Transaction | None:
    """Return the transaction with the given id or None."""
    transaction_row = current_app.session.execute(  # type: ignore[attr-defined]
        select(Transaction).where(Transaction.id == transaction_id)
    ).fetchone()
    return transaction_row[0] if transaction_row else None
