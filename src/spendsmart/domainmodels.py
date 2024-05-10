from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TransactionType(Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


@dataclass
class Transaction:
    type: TransactionType
    date_posted: datetime
    description: str
    amount: float


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
