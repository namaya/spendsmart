from spendsmart.datamodels.repos import TxnRepo

from spendsmart.domainmodels import Transaction


class TxnController:
    def __init__(self, txn_repo: TxnRepo):
        self._txn_repo = txn_repo

    def list(self, limit: int = None, offset: int = 0) -> list[Transaction]:
        return self._txn_repo.list(limit, offset)
