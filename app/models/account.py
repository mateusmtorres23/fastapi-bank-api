from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.transaction import Transaction

class Account(Base):
    __tablename__ = "accounts"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    sequence_number: Mapped[int] = mapped_column(primary_key=True)

    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))

    owner: Mapped["User"] = relationship("User", back_populates="accounts")
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", 
        back_populates="account"
    )

    @property
    def owner_username(self) -> str:
        return self.owner.username if self.owner else ""