# backend/app/models/journal.py
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class JournalEntry(SQLModel, table=True):
    __tablename__ = "journal_entry"

    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    description: Optional[str] = None

    lines: List["JournalLine"] = Relationship(back_populates="entry")


class JournalLine(SQLModel, table=True):
    __tablename__ = "journal_line"

    id: Optional[int] = Field(default=None, primary_key=True)
    entry_id: int = Field(foreign_key="journal_entry.id")
    account_id: int = Field(foreign_key="chart_of_account.id")

    debit: float = Field(default=0.0)
    credit: float = Field(default=0.0)

    entry: "JournalEntry" = Relationship(back_populates="lines")
    account: "ChartOfAccount" = Relationship(back_populates="journal_lines")