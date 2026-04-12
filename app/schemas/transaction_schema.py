from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from decimal import Decimal
from app.models.transaction import TransactionType

class TransactionBase(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)

class TransactionCreate(TransactionBase):
    user_id: int
    account_sequence_number: int
    type: TransactionType

class TransferCreate(TransactionBase):
    """Schema dedicated for transfers between accounts."""
    source_sequence_number: int
    destination_user_id: int
    destination_sequence_number: int

class TransactionRead(TransactionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    account_user_id: int
    account_sequence_number: int
    type: TransactionType
    timestamp: datetime