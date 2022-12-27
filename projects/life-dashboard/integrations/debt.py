from typing import List, Type

from flask import Flask

from common.base import BaseIntegration, BaseDataProvider, ConnectionStatus
from common.types import Integration, DataProvider, Model


class DebtDataProvider(BaseDataProvider):
    def __init__(self) -> None:
        pass

    def get_database_models(self) -> List[Type[Model]]:
        return super().get_database_models()

    def update(self) -> bool:
        return super().update()


class DebtIntegration(BaseIntegration):
    def __init__(self) -> None:
        pass

    def get_connection_status(self) -> ConnectionStatus:
        return ConnectionStatus(
            service_name="Debt Data Provider", is_connected=True, action_link=""
        )

    def connect(self, code: str = "") -> None:
        pass

    def disconnect(self) -> None:
        pass

    def get_data_provider(self) -> Type[DataProvider]:
        return DebtDataProvider()

    def add_views_to_flask(self, app: Flask) -> None:
        pass
