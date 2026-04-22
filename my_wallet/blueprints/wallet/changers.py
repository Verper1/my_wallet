from typing import TypeVar

from flask import current_app

from my_wallet.blueprints.wallet.models import Wallet

ModelT = TypeVar("ModelT")


def create_wallet(wallet: Wallet) -> Wallet:
    """Persist a new wallet."""
    return create(wallet)


def update(model_obj: ModelT) -> ModelT:
    """Persist changes to an existing model instance."""
    assert model_obj.id  # type: ignore[attr-defined]
    current_app.session.add(model_obj)  # type: ignore[attr-defined]
    current_app.session.commit()  # type: ignore[attr-defined]
    return model_obj


def create(model_obj: ModelT) -> ModelT:
    """Persist a new model instance."""
    current_app.session.add(model_obj)  # type: ignore[attr-defined]
    current_app.session.commit()  # type: ignore[attr-defined]
    return model_obj


def delete(model_obj: object) -> None:
    """Delete a model instance."""
    current_app.session.delete(model_obj)  # type: ignore[attr-defined]
    current_app.session.commit()  # type: ignore[attr-defined]
