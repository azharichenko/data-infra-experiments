# Flask extension to hook into custom data providers

from collections.abc import Sequence
from typing import Dict, List, Type, Optional, Generic

from flask import Flask

from common.base import BaseIntegration
from common.models import register_models
from common.types import Integration
from integrations.bills import BillsIntegration
from integrations.debt import DebtIntegration
from integrations.withings import WithingsIntegration


def _connect_integrations_apis(app: Flask, integrations: Sequence[Integration]):
    for integration in integrations:
        integration.add_views_to_flask(app)


class HubIntegrations:
    def __init__(self, app: Optional[Flask] = None) -> None:
        self.integrations: List[BaseIntegration] = [
            BillsIntegration(),
            # DebtIntegration(),
            # WithingsIntegration(),
        ]

        if app:
            _connect_integrations_apis(app, self.integrations)

    def get_connection_statuses(self) -> List[Dict]:
        return [
            integration.get_connection_status()._asdict()
            for integration in self.integrations
        ]

    def establish_database_models(self) -> None:
        for integration in self.integrations:
            provider = integration.get_data_provider()
            models = provider.get_database_models()
            register_models(models)
