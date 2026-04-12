import jwt
from datetime import datetime, timedelta, timezone
from app.security.jwt import create_access_token, JWT_SECRET_KEY, ALGORITHM

def test_create_access_token_payload_and_signature():
    data = {"sub": "1"}
    token = create_access_token(data)

    decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded_token["sub"] == data["sub"]
    assert "exp" in decoded_token

def test_create_access_token_custom_expiration():
    data = {"sub": "2"}
    custom_delta = timedelta(minutes=15)
    
    token = create_access_token(data=data, expires_delta=custom_delta)
    decoded_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    
    expiration_timestamp = decoded_payload["exp"]
    expiration_datetime = datetime.fromtimestamp(expiration_timestamp, tz=timezone.utc)
    
    expected_datetime = datetime.now(timezone.utc) + custom_delta
    time_difference = abs((expiration_datetime - expected_datetime).total_seconds())
    
    assert time_difference < 2