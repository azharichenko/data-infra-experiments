from abc import ABC, abstractmethod
from typing import List, NamedTuple, Type

from flask import Flask

from common.models import BaseModel


class ConnectionStatus(NamedTuple):
    service_name: str
    is_connected: bool
    action_link: str


class BaseDataProvider(ABC):
    @abstractmethod
    def get_database_models(self) -> List[Type[BaseModel]]:
        pass

    @abstractmethod
    def update(self) -> bool:
        pass


class BaseIntegration(ABC):
    @abstractmethod
    def get_connection_status(self) -> ConnectionStatus:
        pass

    # TODO(@azharichenko): Consider correcting this function signiature to make it generic for other types besides oauth
    @abstractmethod
    def connect(self, code: str) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def get_data_provider(self) -> BaseDataProvider:
        pass

    @abstractmethod
    def add_views_to_flask(self, app: Flask) -> None:
        pass
