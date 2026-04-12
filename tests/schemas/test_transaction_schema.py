import pytest
from decimal import Decimal
from pydantic import ValidationError
from app.models.transaction import TransactionType
from app.schemas.transaction_schema import TransactionCreate

def test_transaction_create_valid_deposit():
    schema = TransactionCreate(account_id=1, amount=Decimal("100.00"), type=TransactionType.DEPOSIT)
    assert schema.amount == Decimal("100.00")
    assert schema.type == TransactionType.DEPOSIT

def test_transaction_create_invalid_zero_amount():
    with pytest.raises(ValidationError):
        TransactionCreate(account_id=1, amount=Decimal("0.00"), type=TransactionType.DEPOSIT)