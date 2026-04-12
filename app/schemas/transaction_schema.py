from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from decimal import Decimal
from app.models.transaction import TransactionType

class TransactionBase(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    type: TransactionType

class TransactionCreate(TransactionBase):
    user_id: int
    account_sequence_number: int

class TransactionRead(TransactionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    account_sequence_number: int
    timestamp: datetime