from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship

from my_wallet.blueprints.wallet.enums import WalletStatus
from my_wallet.db.base import Base


wallet_access_table = Table(
    "wallet_access",
    Base.metadata,
    Column("wallet_id", ForeignKey("wallet.id"), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=True),
)


class Wallet(Base):
    __tablename__ = "wallet"

    id = Column(Integer, primary_key=True)
    title = Column(String(30))
    status = Column(Enum(WalletStatus))
    owned_by_user_id = Column(Integer, ForeignKey("user.id"), nullable=True)

    owner = relationship("User")
    users_with_access = relationship("User", secondary=wallet_access_table)

    def __str__(self) -> str:
        return f"{self.title}"

    @property
    def users_ids_with_access(self) -> list[int]:
        """Return ids of users who have access to this wallet."""
        return [u.id for u in self.users_with_access]
