"""Secrets management"""

import os
from typing import Any, Dict

import click
import pyarrow as pa

__all__ = ["get_secret", "store_secret"]


def _create_secrets_store():
    pass


def get_secret(namespace: str, key: str) -> Dict[str, Any]:
    pass


def store_secret(namespace: str, key: str, data: Dict[str, Any]) -> None:
    pass


@click.command()
def main():
    pass


if __name__ == "__main__":
    main()
