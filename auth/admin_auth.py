"""Admin-only authentication for the public FastAPI application."""

import hmac

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth.models import UserLogin
from auth.security import create_access_token, decode_access_token
from config import ADMIN_PASSWORD, ADMIN_USERNAME


router = APIRouter(prefix="/auth", tags=["Authentication"])
bearer_scheme = HTTPBearer()


@router.post("/login")
def login(credentials: UserLogin):
    if not ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin authentication is not configured.",
        )

    valid_username = hmac.compare_digest(credentials.username, ADMIN_USERNAME)
    valid_password = hmac.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (valid_username and valid_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

    return {
        "access_token": create_access_token({"sub": ADMIN_USERNAME, "role": "admin"}),
        "token_type": "bearer",
    }


def require_admin(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
    payload = decode_access_token(credentials.credentials)
    if not payload or payload.get("sub") != ADMIN_USERNAME or payload.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin authentication is required.")

    return ADMIN_USERNAME
