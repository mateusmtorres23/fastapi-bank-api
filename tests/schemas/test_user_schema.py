import pytest
from pydantic import ValidationError
from app.schemas.user_schema import UserCreate

def test_user_create_valid_password():
    schema = UserCreate(username="testuser", password="securepassword")
    assert schema.username == "testuser"
    assert schema.password == "securepassword"

def test_user_create_invalid_password_length():
    with pytest.raises(ValidationError):
        UserCreate(username="testuser", password="short")