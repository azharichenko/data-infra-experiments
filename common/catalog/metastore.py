from functools import cache

from peewee import Model, SqliteDatabase

from common.catalog.filesystem import get_data_directory
from common.logger import get_logger

logger = get_logger(__name__)


@cache
def get_database() -> SqliteDatabase:
    db_path = get_data_directory() / "metastore.db"
    return SqliteDatabase(db_path)


class BaseModel(Model):
    class Meta:
        database = get_database()


class Namespace(BaseModel):
    pass


class CatalogTable(BaseModel):
    pass


def create_metastore() -> None:
    logger.info("attempting to initialize db...")
    database = get_database()
    with database:
        database.create_tables([Namespace, CatalogTable])


if __name__ == "__main__":
    create_metastore
