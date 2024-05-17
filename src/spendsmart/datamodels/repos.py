from sqlalchemy import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy import inspect

from spendsmart.datamodels.tables import TxnRow
from spendsmart.domainmodels import Transaction


class TxnRepo:
    def __init__(self, db_engine: Engine):
        self._db_engine = db_engine

        inspector = inspect(self._db_engine)
        if not inspector.has_table(TxnRow.__tablename__):
            TxnRow.metadata.create_all(self._db_engine)

    def fetch(self, limit: int = None, offset: int = 0) -> list[Transaction]:
        if limit is None:
            limit = 100

        with Session(self._db_engine) as session:
            cursor = (
                session.query(TxnRow)
                .order_by(TxnRow.datestamp.desc())
                .limit(limit)
                .offset(offset)
                .all()
            )

        return [txn.to_model() for txn in cursor]

    def add(self, txns: list[Transaction]):
        with Session(self._db_engine) as session:
            for txn in txns:
                session.merge(TxnRow.from_model(txn))

            session.commit()
