from functools import cache
from json import load
from pathlib import Path
from typing import Dict, NamedTuple


BASE_URL = "https://life.alexzharichenko.me"


class APIKey(NamedTuple):
    pass


class OAuth2Client(NamedTuple):
    id: str
    secret: str


@cache
def _get_keys() -> Dict[str, Dict]:
    keys_file = Path.cwd() / "keys.json"
    keys: Dict[str, Dict]
    with keys_file.open("r") as f:
        keys = load(f)
    return keys


def get_oauth_client_keys(*, service_name: str) -> OAuth2Client:
    keys = _get_keys()

    if service_name in keys:
        return OAuth2Client(
            id=keys[service_name]["client_id"],
            secret=keys[service_name]["client_secret"],
        )
    else:
        raise ValueError(f"Can't find keys for service: {service_name}")
