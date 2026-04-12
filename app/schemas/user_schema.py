from pydantic import BaseModel, Field, ConfigDict
from app.schemas.account_schema import AccountRead

class UserBase(BaseModel):
    username: str = Field(max_length=50)

class UserCreate(UserBase):
    password: str = Field(min_length=6)

class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class UserReadWithAccounts(UserRead):
    accounts: list[AccountRead] = []