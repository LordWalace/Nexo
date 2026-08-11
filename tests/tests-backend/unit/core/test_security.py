import time
from datetime import timedelta

import jwt
import pytest
from app.core.config import settings
from app.core.exceptions import AppException
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)


def test_password_hashing():
    password = "secret_password"
    hashed = get_password_hash(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_create_access_token():
    subject = "user123"
    token = create_access_token(subject=subject)
    assert isinstance(token, str)

    # Verify contents
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
    assert payload["sub"] == subject
    assert payload["type"] == "access"
    assert "exp" in payload


def test_create_access_token_custom_expiry():
    subject = "user123"
    token = create_access_token(subject=subject, expires_delta=timedelta(minutes=5))
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
    assert payload["sub"] == subject
    assert "exp" in payload


def test_create_refresh_token():
    subject = "user123"
    token = create_refresh_token(subject=subject)
    assert isinstance(token, str)

    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
    assert payload["sub"] == subject
    assert payload["type"] == "refresh"
    assert "exp" in payload


def test_decode_access_token_valid():
    subject = "user123"
    token = create_access_token(subject=subject)
    decoded_sub = decode_access_token(token)
    assert decoded_sub == subject


def test_decode_access_token_missing():
    with pytest.raises(AppException) as excinfo:
        decode_access_token("")
    assert excinfo.value.code == "TOKEN_MISSING"


def test_decode_access_token_invalid_type():
    subject = "user123"
    token = create_refresh_token(subject=subject)  # Creates a refresh token
    with pytest.raises(AppException) as excinfo:
        decode_access_token(token)
    assert excinfo.value.code == "TOKEN_INVALID_TYPE"


def test_decode_access_token_no_sub():
    # Create a raw token missing 'sub'
    to_encode = {"exp": time.time() + 3600, "type": "access"}
    token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")

    with pytest.raises(AppException) as excinfo:
        decode_access_token(token)
    assert excinfo.value.code == "TOKEN_INVALID_PAYLOAD"


def test_decode_access_token_expired():
    # Expired token
    to_encode = {"exp": time.time() - 100, "type": "access", "sub": "123"}
    token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")

    with pytest.raises(AppException) as excinfo:
        decode_access_token(token)
    assert excinfo.value.code == "TOKEN_EXPIRED"


def test_decode_access_token_invalid_signature():
    # Tampered token
    subject = "user123"
    token = create_access_token(subject=subject)
    tampered_token = token[:-5] + "aaaaa"

    with pytest.raises(AppException) as excinfo:
        decode_access_token(tampered_token)
    assert excinfo.value.code == "TOKEN_INVALID_SIGNATURE"
