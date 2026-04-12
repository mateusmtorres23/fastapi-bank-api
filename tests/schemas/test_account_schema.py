import pytest
from decimal import Decimal
from pydantic import ValidationError
from app.schemas.account_schema import AccountCreate, AccountRead

def test_account_create_valid_balance():
    account = AccountCreate(user_id=1, balance=Decimal("100.00"))
    assert account.user_id == 1
    assert account.balance == Decimal("100.00")

def test_account_create_invalid_negative_balance():
    with pytest.raises(ValidationError):
        AccountCreate(user_id=1, balance=Decimal("-10.00"))

def test_account_read_schema():
    account_read = AccountRead(
        user_id=1,
        sequence_number=2,
        balance=Decimal("50.00"),
        owner_username="shannon"
    )
    assert account_read.sequence_number == 2