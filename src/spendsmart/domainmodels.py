from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TransactionType(Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


@dataclass(eq=True, frozen=True)
class Transaction:
    datestamp: datetime
    date_posted: datetime
    description: str
    amount: int
    merchant: str = ""
    category: str = ""


@dataclass
class Statement:
    account_number: str
    start_date: str
    end_date: str
    transactions: list[Transaction]


@dataclass
class Account:
    account_number: str
    balance: float
    available_balance: float
    currency: str
    transactions: list[Transaction]
