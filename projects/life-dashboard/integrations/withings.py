# Withings Data Integrations

from typing import List, Type

from flask import Flask, redirect, request
from flask.views import MethodView

from common.base import BaseIntegration, BaseDataProvider, ConnectionStatus
from common.config import BASE_URL
from common.config import get_oauth_client_keys
from common.models import BaseModel

from withings_api import WithingsAuth, WithingsApi, AuthScope

BASE_ENDPOINT = "/api/withings"


class SleepSummary(BaseModel):
    pass


class DailyMeasures(BaseModel):
    pass


class WithingsDataProvider(BaseDataProvider):
    def __init__(self, api: WithingsApi) -> None:
        self.api = api
        self.models: List[Type[BaseModel]] = [
            SleepSummary,
            DailyMeasures,
        ]


class WithingsCallbackAPI(MethodView):
    def __init__(self, **kwargs) -> None:
        self.callback_func = kwargs["callback_func"]

    def get(self):
        code = request.args.get("code", default=None)
        state = request.args.get("state", default=None)
        if code:
            self.callback_func(code)
        else:
            # TODO(@azharichenko): Need to do a better error maybe with an error pop up message
            raise RuntimeError("Needdddd codeee")
        return redirect("/")


class WithingsIntegration(BaseIntegration):
    def __init__(self) -> None:
        oauth2_client = get_oauth_client_keys(service_name="withings")
        self.auth = WithingsAuth(
            client_id=oauth2_client.id,
            consumer_secret=oauth2_client.secret,
            callback_uri=f"{BASE_URL}{BASE_ENDPOINT}/callback",
            scope=(
                AuthScope.USER_ACTIVITY,
                AuthScope.USER_METRICS,
                AuthScope.USER_INFO,
                AuthScope.USER_SLEEP_EVENTS,
            ),
        )
        self.api: WithingsApi = None

    def get_connection_status(self) -> ConnectionStatus:
        global api
        return ConnectionStatus(
            service_name="Withings",
            is_connected=self.api is not None,
            action_link=self.auth.get_authorize_url(),
        )

    def connect(self, code: str) -> None:
        print(code)
        credentials = self.auth.get_credentials(code)
        self.api = WithingsApi(credentials)

    def disconnect(self) -> None:
        self.api = None

    def get_data_provider(self) -> Type[BaseDataProvider]:
        return WithingsDataProvider(self.api)

    def add_views_to_flask(self, app: Flask) -> None:
        # Callback API
        callback_view = WithingsCallbackAPI.as_view(
            "withings_callback_api", callback_func=self.connect
        )
        app.add_url_rule(
            f"{BASE_ENDPOINT}/callback",
            view_func=callback_view,
            methods=[
                "GET",
            ],
        )
