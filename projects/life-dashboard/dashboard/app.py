"""
Life Dashboard
"""
from typing import List, Dict

import requests
from dash import Dash, html, dcc, dash_table

from common.config import BASE_URL

app = Dash(__name__)


def get_bills_table_data() -> Dict[str, List[Dict]]:
    resp = requests.get("http://127.0.0.1:6000/api/bills")
    return resp.json()


app.layout = html.Div(
    children=[
        dash_table.DataTable(**get_bills_table_data()),
    ]
)
