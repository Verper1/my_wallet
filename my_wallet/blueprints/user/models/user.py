from sqlalchemy import Column, Integer, String

from my_wallet.db.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), info={"label": "First name"})
    last_name = Column(String(30), info={"label": "Last name"})
    email = Column(String(30))
    mobile = Column(String(30))

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def is_authenticated(self) -> bool:
        """Return True if the user is authenticated."""
        return True

    @property
    def is_active(self) -> bool:
        """Return True if the user account is active."""
        return True

    @property
    def is_anonymous(self) -> bool:
        """Return True if this is an anonymous user."""
        return False

    def get_id(self) -> str:
        """Return the user id as a string for flask-login."""
        return str(self.id)
