from decimal import Decimal
import enum
from typing import TYPE_CHECKING
# Import ForeignKeyConstraint
from sqlalchemy import ForeignKeyConstraint, Numeric, Enum 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.account import Account
    
class TransactionType(str, enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    user_id: Mapped[int] = mapped_column()
    account_sequence_number: Mapped[int] = mapped_column()
    
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType))
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id", "account_sequence_number"],
            ["accounts.user_id", "accounts.sequence_number"],
        ),
    )

    account: Mapped["Account"] = relationship("Account", back_populates="transactions")