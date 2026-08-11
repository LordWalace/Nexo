from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from app.core.config import settings
from app.core.exceptions import AppException

password_hash = PasswordHash((Argon2Hasher(),))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def create_access_token(
    subject: str | Any, expires_delta: timedelta | None = None
) -> str:
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def create_refresh_token(
    subject: str | Any, expires_delta: timedelta | None = None
) -> str:
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        )

    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_access_token(token: str) -> str:
    if not token:
        raise AppException(
            code="TOKEN_MISSING", message="Token ausente.", status_code=401
        )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])

        token_type = payload.get("type")
        if token_type != "access":
            raise AppException(
                code="TOKEN_INVALID_TYPE",
                message="Tipo de token inválido.",
                status_code=401,
            )

        subject = payload.get("sub")
        if not subject:
            raise AppException(
                code="TOKEN_INVALID_PAYLOAD",
                message="Payload sem identificador de usuário.",
                status_code=401,
            )

        return str(subject)
    except ExpiredSignatureError:
        raise AppException(
            code="TOKEN_EXPIRED", message="Token expirado.", status_code=401
        )
    except InvalidTokenError:
        raise AppException(
            code="TOKEN_INVALID_SIGNATURE",
            message="Token malformado ou assinatura inválida.",
            status_code=401,
        )
