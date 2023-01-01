# Local Data Catalog Interface. Copyright Alex Zharichenko

import click

from common.catalog.metastore import create_metastore
from common.catalog.filesystem import get_data_directory, data_catalog_exists
from common.logger import get_logger

logger = get_logger(__name__)


def initialize_data_catalog() -> None:
    if data_catalog_exists():
        raise RuntimeError("Data Catalog already exists.")
    logger.info("Initializing directory...")
    data_dir = get_data_directory()
    data_dir.mkdir()
    create_metastore()


@click.command()
@click.option(
    "--init",
    is_flag=True,
    show_default=True,
    help="Initializes directory and metastore for local data catalog.",
)
def main(init: bool) -> None:
    if init:
        initialize_data_catalog()
    else:
        raise RuntimeError("Something went wrong :O!")


if __name__ == "__main__":
    main()
