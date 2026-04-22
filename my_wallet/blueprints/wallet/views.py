from typing import Any

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from my_wallet.blueprints.user.fetchers import fetch_user_by
from my_wallet.blueprints.wallet.changers import delete, create, update
from my_wallet.blueprints.wallet.enums import WalletStatus
from my_wallet.blueprints.wallet.fetchers import (
    fetch_wallets_for,
    get_wallet_by,
    fetch_transactions_for,
    get_transaction_by,
)
from my_wallet.blueprints.wallet.forms import (
    TransactionAddForm,
    WalletAddForm,
    WalletAddMemberForm,
)
from my_wallet.blueprints.wallet.models import Transaction, Wallet


@login_required
def wallets_list() -> Any:
    """Show the list of wallets accessible to the current user."""
    wallets = fetch_wallets_for(current_user)
    return render_template("wallets_list.html", wallets=wallets)


@login_required
def wallet_detail(wallet_id: int) -> Any:
    """Show wallet details and its transactions."""
    wallet = get_wallet_by(wallet_id=wallet_id)
    transactions = fetch_transactions_for(wallet_id=wallet_id)
    return render_template(
        "wallet_detail.html", wallet=wallet, transactions=transactions
    )


@login_required
def wallet_delete(wallet_id: int) -> Any:
    """Soft-delete the wallet if the current user is its owner."""
    wallet = get_wallet_by(wallet_id=wallet_id)
    if wallet.owner != current_user:  # type: ignore[union-attr]
        flash("Cant delete the wallet since you're not owner of the wallet")
    else:
        wallet.status = WalletStatus.DELETED  # type: ignore[union-attr]
        update(wallet)
        flash("Wallet deleted")
    return redirect(url_for(".wallets_list"))


@login_required
def transaction_delete(transaction_id: int) -> Any:
    """Delete a transaction if the current user owns the wallet."""
    transaction = get_transaction_by(transaction_id)
    wallet_id = transaction.wallet_id  # type: ignore[union-attr]
    if transaction is None:
        flash("Transaction not found")
    elif transaction.wallet.owner == current_user:
        delete(transaction)
        flash("Transaction deleted")
    else:
        flash("Permission error")
    return redirect(url_for(".wallet_detail", wallet_id=wallet_id))


@login_required
def transaction_add(wallet_id: int) -> Any:
    """Show the transaction creation form and create a new transaction."""
    form = (
        TransactionAddForm(request.form)
        if request.method == "POST"
        else TransactionAddForm()
    )
    if request.method == "POST" and form.validate():
        create(
            Transaction(
                wallet_id=wallet_id,
                timestamp=form.timestamp.data,
                amount=form.amount.data,
                currency=form.currency.data,
                description=form.description.data,
            ),
        )
        flash("Transaction created")
        return redirect(url_for(".wallet_detail", wallet_id=wallet_id))
    return render_template("transaction_add.html", form=form)


@login_required
def wallet_add() -> Any:
    """Show the wallet creation form and create a new wallet."""
    form = WalletAddForm(request.form) if request.method == "POST" else WalletAddForm()
    if request.method == "POST" and form.validate():
        wallet = create(
            Wallet(
                title=form.title.data,
                status=WalletStatus.ACTIVE,
                owned_by_user_id=current_user.id,
            ),
        )
        flash("Wallet created")
        return redirect(url_for(".wallet_detail", wallet_id=wallet.id))
    return render_template("wallet_add.html", form=form)


@login_required
def wallet_access(wallet_id: int) -> Any:
    """Grant another user access to the wallet."""
    form = (
        WalletAddMemberForm(request.form)
        if request.method == "POST"
        else WalletAddMemberForm()
    )
    wallet = get_wallet_by(wallet_id=wallet_id)
    if request.method == "POST" and form.validate():
        user = fetch_user_by(email=form.email.data)
        if user is None:
            flash(f"User with email {form.email.data} not found")
        elif wallet and user.id in {u.id for u in wallet.users_with_access}:
            flash(f"User with email {form.email.data} already has access to the wallet")
        elif wallet and wallet.owned_by_user_id == user.id:
            flash("Cant add owner as user with access")
        else:
            wallet.users_with_access.append(user)  # type: ignore[union-attr]
            update(wallet)
            flash("Permission granted")
        return redirect(url_for(".wallet_access", wallet_id=wallet_id))
    return render_template("wallet_access.html", form=form, wallet=wallet)


@login_required
def wallet_access_remove(wallet_id: int, user_id: int) -> Any:
    """Revoke a user's access to the wallet."""
    wallet = get_wallet_by(wallet_id=wallet_id)
    user = fetch_user_by(user_id=user_id)  # type: ignore[arg-type]
    http_response = redirect(url_for(".wallet_access", wallet_id=wallet_id))
    if wallet is None:
        flash("Wallet not found")
    elif user is None:
        flash("User not found")
    elif user_id not in {u.id for u in wallet.users_with_access}:
        flash("User has no access to the wallet")
    else:
        wallet.users_with_access.remove(user)
        update(wallet)
        flash("Permission removed")
    return http_response
