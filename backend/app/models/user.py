from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="company.id")
    email: str
    full_name: str
    role: str = "admin"
    created_at: datetime = Field(default_factory=datetime.utcnow)