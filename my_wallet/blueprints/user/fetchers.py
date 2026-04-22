from flask import current_app
from sqlalchemy import select, not_

from my_wallet.blueprints.user.models.user import User


def fetch_user_by(user_id: int | None = None, email: str | None = None) -> User | None:
    """Return a user looked up by id (if given) or by email."""
    where_clause = User.id == user_id if user_id else User.email == email
    row = current_app.session.execute(  # type: ignore[attr-defined]
        select(User).where(where_clause)
    ).fetchone()
    return row[0] if row else None


def fetch_all_users_with_configured_telegram() -> list[User]:
    """Return all users that have a telegram chat id configured."""
    users = current_app.session.execute(  # type: ignore[attr-defined]
        select(User).where(not_(User.telegram_chat_id.is_(None)))
    ).fetchall()
    return [r[0] for r in users]
