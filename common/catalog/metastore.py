from functools import cache
from typing import Any, Dict

from peewee import CharField, ForeignKeyField, Model, SqliteDatabase

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
    name = CharField(unique=True)


class CatalogTable(BaseModel):
    name = CharField(unique=True)
    location = CharField()
    data_format = CharField()
    database = ForeignKeyField(Namespace, backref="tables")


def create_metastore() -> None:
    logger.info("attempting to initialize db...")
    database = get_database()
    with database:
        database.create_tables([Namespace, CatalogTable])


def create_database(database_name: str) -> None:
    database = get_database()
    with database.atomic():
        namespace = Namespace.create(name=database_name)


def does_database_exist(database_name: str) -> bool:
    return True


def create_table(
    database_name: str, table_name: str, data_format: str = "PARQUET"
) -> None:
    database = get_database()
    data_path = f"{database_name}/{table_name}"
    with database.atomic():
        namespace = Namespace.get(name=database_name)
        table = CatalogTable.create(
            name=table_name,
            database=namespace,
            data_format=data_format,
            location=data_path,
        )


def get_table_properties(database_name: str, table_name: str) -> Dict[str, Any]:
    table = CatalogTable.get(name=table_name)
    print(table)


def does_table_exist(database_name: str, table_name: str) -> bool:
    return True


if __name__ == "__main__":
    create_metastore()
    create_database(database_name="sister_cities")
    create_table(database_name="sister_cities", table_name="test_table")
    get_table_properties(database_name="sister_cities", table_name="test_table")
