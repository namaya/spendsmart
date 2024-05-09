from typing import Self

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, MappedAsDataclass

from spendsmart.statements.dataclasses import Transaction


class Base(DeclarativeBase):
    pass


class TxnRow(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(16))
    timestamp: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(128))
    amount: Mapped[int] = mapped_column()

    @classmethod
    def from_model(cls, txn: Transaction) -> Self:
        return cls(
            type=txn.type.value,
            timestamp=txn.date_posted,
            description=txn.description,
            amount=txn.amount,
        )
