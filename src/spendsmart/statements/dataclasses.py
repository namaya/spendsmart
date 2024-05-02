from dataclasses import dataclass
from enum import Enum


class TransactionType(Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


@dataclass
class Transaction:
    type: TransactionType
    date_posted: str
    description: str
    amount: float
    balance: float


@dataclass
class Statement:
    account_number: str
    start_date: str
    end_date: str
    transactions: list[Transaction]
