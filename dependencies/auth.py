from fastapi import Header, HTTPException
from providers.auth import AuthProvider, AuthUser, FakeAuthProvider

auth_provider: AuthProvider = FakeAuthProvider()


def require_user(authorization: str | None = Header(default=None)) -> AuthUser:
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = auth_provider.get_current_user(token)

    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return user
