from typing import Self

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from spendsmart.domainmodels import Transaction, TransactionType


class Base(DeclarativeBase):
    pass


class TxnRow(Base):
    __tablename__ = "transactions"

    datestamp: Mapped[str] = mapped_column(DateTime(), primary_key=True)
    description: Mapped[str] = mapped_column(String(128), primary_key=True)
    amount: Mapped[int] = mapped_column(primary_key=True)
    date_posted: Mapped[str] = mapped_column(DateTime())

    @classmethod
    def from_model(cls, txn: Transaction) -> Self:
        return cls(
            datestamp=txn.datestamp,
            description=txn.description,
            amount=txn.amount,
            date_posted=txn.date_posted,
        )

    def to_model(self) -> Transaction:
        return Transaction(
            datestamp=self.datestamp,
            description=self.description,
            amount=self.amount,
            date_posted=self.date_posted,
        )
