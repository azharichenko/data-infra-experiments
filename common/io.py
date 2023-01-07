"""
Common Access
"""


import pandas as pd
import pyarrow as pa
import pyarrow.dataset as ds

from pyarrow import fs

from deltalake import DeltaTable
from deltalake import DataCatalog


from common.catalog.metastore import get_database


def write_table(table: pa.Table, table_name: str, database_name: str) -> None:
    pass


def get_dataset(table_name: str, database_name: str) -> ds.Dataset:

    pass
