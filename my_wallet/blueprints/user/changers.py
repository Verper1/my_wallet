from typing import Any

from flask import current_app
from sqlalchemy import update

from my_wallet.blueprints.user.models.user import User


def create_user(email: str, mobile: str, first_name: str, last_name: str) -> User:
    """Create and persist a new user."""
    user = User(
        email=email,
        mobile=mobile,
        first_name=first_name,
        last_name=last_name,
    )
    current_app.session.add(user)  # type: ignore[attr-defined]
    current_app.session.commit()  # type: ignore[attr-defined]
    return user


def update_user(user_id: int, **kwargs_to_update: Any) -> None:
    """Update fields of the given user."""
    current_app.session.execute(  # type: ignore[attr-defined]
        update(User).where(User.id == user_id).values(**kwargs_to_update)
    )
    current_app.session.commit()  # type: ignore[attr-defined]
