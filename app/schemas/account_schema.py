
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.transaction_schema import TransactionRead

class AccountBase(BaseModel):
    balance: Decimal = Field(ge=0)

class AccountCreate(AccountBase):
    user_id: int

class AccountRead(AccountBase):
    model_config = ConfigDict(from_attributes=True)
    user_id: int  
    sequence_number: int
    owner_username: str
    
class AccountReadWithTransactions(AccountRead):
    transactions: list[TransactionRead] = []