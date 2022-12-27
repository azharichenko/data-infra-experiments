from re import S
from typing import List, Type

from peewee import Model, SqliteDatabase


sqlite_db = SqliteDatabase("data.db")


connection = sqlite_db.connect()


class BaseModel(Model):
    class Meta:
        database = sqlite_db


def create_database():
    pass


def register_models(models: List[Type[BaseModel]]) -> None:
    sqlite_db.create_tables(models)
