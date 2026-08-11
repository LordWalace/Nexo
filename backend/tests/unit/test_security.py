import jwt

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password


def test_password_hashing():
    password = "secretpassword"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_create_access_token():
    subject = "user123"
    token = create_access_token(subject=subject)
    decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
    assert decoded["sub"] == subject
    assert decoded["type"] == "access"
    assert "exp" in decoded
