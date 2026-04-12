import pytest
from app.schemas.account_schema import AccountCreate
from pydantic import ValidationError
from decimal import Decimal

def test_account_create_valid_balance():
    schema = AccountCreate(user_id=1, balance=Decimal("500.00"))
    assert schema.balance == Decimal("500.00")
    assert schema.user_id == 1

def test_account_create_invalid_negative_balance():
    with pytest.raises(ValidationError):
        AccountCreate(user_id=1, balance=Decimal("-0.01"))