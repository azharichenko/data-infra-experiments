from flask import Flask, redirect, render_template, request

from integrations import HubIntegrations

app = Flask(__name__)

integrations = HubIntegrations(app)


@app.route("/")
def index():
    return render_template(
        "index.html", connection_statuses=integrations.get_connection_statuses()
    )


if __name__ == "__main__":
    app.run()
