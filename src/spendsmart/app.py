import csv
import logging
from pathlib import Path
import sys

from spendsmart.utils import errctx


logger = logging.getLogger(__name__)


def main():
    if len(sys.argv) >= 2:
        index(Path(sys.argv[1]))


@errctx("Couldn't index file '{file}'.")
def index(file: Path):
    if not file.exists():
        raise FileNotFoundError(f"File not found.")

    if not file.suffix == ".csv":
        raise ValueError(f"File format is not supported.")

    logger.info(f"Indexing file '{file}'.")


if __name__ == "__main__":
    main()
