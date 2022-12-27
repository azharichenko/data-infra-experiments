"""
Bills Data Provider

This provides information on all the baseline monthly costs,
debts, etc. that need to be accounted for
"""

from functools import cache
from typing import Dict, List, Type

from flask import Flask
from flask.views import MethodView
from peewee import CharField, FloatField

from common.base import BaseIntegration, BaseDataProvider, ConnectionStatus
from common.models import BaseModel
from common.types import Model, DataProvider


class MonthlyBill(BaseModel):
    name = CharField()
    cost = FloatField()


def get_total_monthly_bills() -> float:
    pass


@cache
def get_monthly_bill_columns() -> List[Dict[str, str]]:
    return [
        {"name": column, "id": column}
        for column in MonthlyBill._meta.fields.keys()
        if column != "id"
    ]


class BillsAPI(MethodView):
    def get(self) -> Dict:
        # TODO: Account for errors and both sides
        return {
            "data": [
                {"name": monthly_bill.name, "cost": monthly_bill.cost}
                for monthly_bill in MonthlyBill.select()
            ],
            "columns": get_monthly_bill_columns(),
        }

    def post(self):
        pass

    def delete(self):
        pass


class BillsDataProvider(BaseDataProvider):
    def __init__(self) -> None:
        pass

    def get_database_models(self) -> List[Type[Model]]:
        return [MonthlyBill]

    def update(self) -> bool:
        return True


class BillsIntegration(BaseIntegration):
    BASE_ENDPOINT = "/api/bills"

    def __init__(self) -> None:
        self.data_provider = BillsDataProvider()

    def get_connection_status(self) -> ConnectionStatus:
        return ConnectionStatus(
            service_name="Bills Data Provider",
            is_connected=True,
            action_link="",
        )

    def connect(self, code: str = "") -> None:
        pass

    def disconnect(self) -> None:
        pass

    def get_data_provider(self) -> BillsDataProvider:
        return self.data_provider

    def add_views_to_flask(self, app: Flask) -> None:
        bill_view = BillsAPI.as_view("bills_api")
        app.add_url_rule(f"{self.BASE_ENDPOINT}", view_func=bill_view, methods=["GET"])
