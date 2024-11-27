import pytest
from src.auth import decode_access_token, create_access_token
from datetime import timedelta

def test_decode_valid_token():
    # Create a valid token
    token_data = {"sub": "testuser"}
    token = create_access_token(data=token_data, expires_delta=timedelta(minutes=30))
    
    # Decode it
    decoded_data = decode_access_token(token)
    assert decoded_data["sub"] == "testuser"

def test_decode_invalid_token():
    with pytest.raises(Exception):
        decode_access_token("invalid.token.value")

def test_decode_expired_token():
    # Create an expired token
    token_data = {"sub": "testuser"}
    expired_token = create_access_token(data=token_data, expires_delta=timedelta(seconds=-10))
    
    # Decode it (should raise an error)
    with pytest.raises(Exception):
        decode_access_token(expired_token)
