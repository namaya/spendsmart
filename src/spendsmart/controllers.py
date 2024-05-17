from pathlib import Path
import logging

from spendsmart.statements.parsers import QfxParser
from spendsmart.utils import errctx
from spendsmart.datamodels.repos import TxnRepo
from spendsmart.domainmodels import Transaction
from spendsmart.datamodels.tables import TxnRow

logger = logging.getLogger(__name__)


class TxnController:
    """A class to mediate between views and the data model."""

    def __init__(self, txn_repo: TxnRepo):
        self._txn_repo = txn_repo

    def fetch_txns(self, limit: int = None, offset: int = 0) -> list[Transaction]:
        return self._txn_repo.fetch(limit, offset)

    @errctx("Couldn't index file '{file}'.")
    def index(self, file: Path):
        if not file.exists():
            raise FileNotFoundError(f"File not found.")

        if file.suffix not in (".qfx",):
            raise ValueError(f"File format is not supported.")

        logger.info(f"Indexing file '{file}'.")

        parser = QfxParser()

        statement = parser.parse(file)

        self._txn_repo.add(statement.transactions)
