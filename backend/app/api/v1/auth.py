import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.dependencies import get_db
from app.core.security import create_access_token, verify_password
from app.infrastructure.database.models.user import User
from app.infrastructure.database.repositories.user_repository import UserRepository
from app.schemas.auth import GoogleLoginRequest, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
) -> "Any":
    repository = UserRepository(session)
    user = await repository.get_active_by_email(form_data.username)
    if not user or not user.password_hash or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/google", response_model=Token)
async def google_login(
    request: GoogleLoginRequest,
    session: AsyncSession = Depends(get_db),
) -> "Any":
    try:
        # Validate the token
        # If settings.GOOGLE_CLIENT_ID is None, it won't check audience
        idinfo = id_token.verify_oauth2_token(
            request.id_token, 
            google_requests.Request(), 
            settings.GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=10
        )

        email = idinfo.get("email")
        google_subject = idinfo.get("sub")
        name = idinfo.get("name", "Usuário do Google")

        if not email or not google_subject:
            raise ValueError("Token inválido: email ou sub ausentes")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token do Google inválido: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    repository = UserRepository(session)
    
    # Try to find existing user by google_subject or email
    user = await repository.get_by_email(email)
    
    if user:
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário inativo"
            )
        # Update google subject if it was empty
        if not user.google_subject:
            user.google_subject = google_subject
            await repository.update(user)
    else:
        # Create new user without password_hash
        user = User(
            id=uuid.uuid4(),
            name=name,
            email=email,
            password_hash=None,
            google_subject=google_subject,
            email_verified=True,
            is_active=True,
        )
        await repository.create(user)

    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}
