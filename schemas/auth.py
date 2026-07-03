from pydantic import BaseModel


class AuthUserResponse(BaseModel):
    id: str
    email: str
    role: str
