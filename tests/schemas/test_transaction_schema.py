import pytest
from decimal import Decimal
from pydantic import ValidationError
from app.schemas.transaction_schema import TransactionCreate
from app.models.transaction import TransactionType

def test_transaction_create_valid_deposit():
    transaction = TransactionCreate(
        user_id=1,
        account_sequence_number=1,
        amount=Decimal("150.00"),
        type=TransactionType.DEPOSIT
    )
    assert transaction.user_id == 1
    assert transaction.account_sequence_number == 1
    assert transaction.amount == Decimal("150.00")

def test_transaction_create_invalid_zero_amount():
    with pytest.raises(ValidationError):
        TransactionCreate(
            user_id=1,
            account_sequence_number=1,
            amount=Decimal("0.00"), 
            type=TransactionType.DEPOSIT
        )