from typing import Self

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from spendsmart.domainmodels import Transaction, TransactionType


class Base(DeclarativeBase):
    pass


class TxnRow(Base):
    __tablename__ = "transactions"

    timestamp: Mapped[str] = mapped_column(DateTime(), primary_key=True)
    description: Mapped[str] = mapped_column(String(128), primary_key=True)
    amount: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(16))

    @classmethod
    def from_model(cls, txn: Transaction) -> Self:
        return cls(
            timestamp=txn.date_posted,
            description=txn.description,
            amount=txn.amount,
            type=txn.type.value,
        )

    def to_model(self) -> Transaction:
        return Transaction(
            date_posted=self.timestamp,
            description=self.description,
            amount=self.amount,
            type=TransactionType(self.type),
        )
