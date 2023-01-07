"""Secrets management"""

import json
import os
from typing import Any, Dict, Optional

import click
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import polars as pl


from common.catalog.filesystem import get_data_directory
from common.logger import get_logger

__all__ = ["get_secret", "store_secret"]


secrets_dir = get_data_directory() / "secrets"
secrets_file = secrets_dir / "secrets.parquet"


logger = get_logger(__name__)


def _create_secrets_store():
    pass


def get_secret(namespace: str, key: str) -> Optional[Dict[str, Any]]:
    dataset = ds.dataset(secrets_dir, format="parquet")
    df = (
        pl.scan_ds(dataset)
        .filter((pl.col("namespace") == namespace) & (pl.col("key") == key))
        .select("data")
        .collect()
    )
    if df.shape[0] == 0:
        raise ValueError(f"Can't find secret {namespace}:{key} in secret store.")
    secret = df[0, 0]
    return json.loads(secret)


def store_secret(namespace: str, key: str, data: Dict[str, Any]) -> None:
    df = None
    if not secrets_file.exists():
        df = pd.DataFrame(
            data={"namespace": [namespace], "key": [key], "data": [json.dumps(data)]}
        )
    else:
        df = pd.read_parquet(secrets_file)

        lookup_df = df.copy().reset_index()
        lookup_df = lookup_df[lookup_df["namespace"] == namespace]
        lookup_df = lookup_df[lookup_df["key"] == key]

        if not lookup_df.empty:
            print(f"updated secret")
            print(lookup_df, lookup_df.index, df.loc[lookup_df.index[0], "data"])
            df.loc[lookup_df.index[0], "data"] = json.dumps(data)
        else:
            print("added additional entry")
            df = pd.concat(
                [
                    df,
                    pd.DataFrame(
                        data={
                            "namespace": [namespace],
                            "key": [key],
                            "data": [json.dumps(data)],
                        }
                    ),
                ]
            )
    df.to_parquet(secrets_file, index=False)


@click.command()
def main():
    pass


if __name__ == "__main__":
    main()
