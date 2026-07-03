from fastapi import APIRouter, Depends
from dependencies.auth import require_user
from providers.auth import AuthUser

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
def me(user: AuthUser = Depends(require_user)):
    return user
