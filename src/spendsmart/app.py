import logging
from pathlib import Path
import sys

from sqlalchemy import create_engine

from spendsmart.datamodels.repos import TxnRepo
from spendsmart.controllers import TxnController
from spendsmart.views import SpendSmartApp


logger = logging.getLogger(__name__)


def main():
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    txn_repo = TxnRepo(engine)
    txn_controller = TxnController(txn_repo)

    # TODO: only index file if transactions are not already indexed
    if len(sys.argv) >= 2:
        txn_controller.index(Path(sys.argv[1]))

    app = SpendSmartApp(txn_controller)

    app.run()
    # TODO: view transactions
    # * GOAL: categorize transactions
    # * allot budget for each category
    # * track spending


if __name__ == "__main__":
    main()
