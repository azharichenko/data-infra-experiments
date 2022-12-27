"""
Life Dashboard CLI
"""

from argparse import ArgumentParser

from common.models import create_database
from integrations import HubIntegrations


parser = ArgumentParser(
    description="CLI tool for establishing the services for the life dashboard"
)
parser.add_argument("--init", action="store_true")
parser.add_argument("--hub", action="store_true")
parser.add_argument("--dash", action="store_true")


def init():
    create_database()

    hub = HubIntegrations()
    hub.establish_database_models()


def run_hub_app():
    from hub.app import app as hub_app

    # hub_app.run(ssl_context="adhoc", host="0.0.0.0", debug=True)
    hub_app.run(debug=True, port=6000)


def run_dashboard_app():
    from dashboard.app import app as dash_app

    dash_app.run_server(debug=True, port=7000)


if __name__ == "__main__":
    args = parser.parse_args()

    if args.init:
        init()
    elif args.hub:
        run_hub_app()
    elif args.dash:
        run_dashboard_app()
