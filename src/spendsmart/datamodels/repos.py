from sqlalchemy import Engine
from sqlalchemy.orm import Session

from spendsmart.datamodels.tables import TxnRow
from spendsmart.domainmodels import Transaction


class TxnRepo:
    def __init__(self, db_engine: Engine):
        self._db_engine = db_engine

    def list(self, limit: int = None, offset: int = 0) -> list[Transaction]:
        with Session(self._db_engine) as session:
            cursor = (
                session.query(TxnRow)
                .order_by(TxnRow.timestamp)
                .limit(limit)
                .offset(offset)
                .all()
            )

        return [txn.to_model() for txn in cursor]
