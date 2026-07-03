from fastapi import APIRouter, Depends
from dependencies.auth import require_user
from providers.auth import AuthUser
from schemas.auth import AuthUserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me", response_model=AuthUserResponse)
def me(user: AuthUser = Depends(require_user)):
    return user
