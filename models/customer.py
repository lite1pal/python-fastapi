from typing import Literal

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


CustomerStatus = Literal["lead", "active", "archived"]


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
