import logging
from pathlib import Path
import sys

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from spendsmart.transactions.datamodels import TxnRow
from spendsmart.statements.parsers import QfxParser
from spendsmart.utils import errctx


logger = logging.getLogger(__name__)

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)


def main():
    if len(sys.argv) >= 2:
        index(Path(sys.argv[1]))

    # TODO: view transactions
    # * GOAL: categorize transactions
    # * allot budget for each category
    # * track spending


@errctx("Couldn't index file '{file}'.")
def index(file: Path):
    if not file.exists():
        raise FileNotFoundError(f"File not found.")

    if file.suffix not in (".qfx",):
        raise ValueError(f"File format is not supported.")

    logger.info(f"Indexing file '{file}'.")

    parser = QfxParser()

    statement = parser.parse(file)

    # TODO: Automatically categorize transactions (using LLM)

    inspector = inspect(engine)

    if not inspector.has_table(TxnRow.__tablename__):
        TxnRow.metadata.create_all(engine)

    with Session(engine) as session:
        for txn in statement.transactions:
            row = TxnRow.from_model(txn)

            session.add(row)

        session.commit()


if __name__ == "__main__":
    main()
