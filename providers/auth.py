from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AuthUser:
    id: str
    email: str
    role: str


class AuthProvider(ABC):
    @abstractmethod
    def get_current_user(self, token: str | None) -> AuthUser | None:
        raise NotImplementedError


class FakeAuthProvider(AuthProvider):
    def get_current_user(self, token: str | None) -> AuthUser | None:
        if token is None:
            return None

        if token == "admin-token":
            return AuthUser(id="user_admin", email="admin@example.com", role="admin")

        if token == "user-token":
            return AuthUser(id="user_123", email="user@example.com", role="user")

        return None
