# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

cities = pd.read_csv("data/cities.csv")
twinning = pd.read_csv("data/twinning.csv")


def calculate_relation(cities, twinning):
    merged_df = pd.merge(twinning, cities, how="cross")
    merged_df = merged_df[merged_df["cid"] == merged_df["cid1"]]
    merged_df = merged_df[["fid", "cid1", "cid2", "name", "lat", "lon", "country"]]
    merged_df = pd.merge(merged_df, cities, how="cross")
    merged_df = merged_df[merged_df["cid"] == merged_df["cid2"]]
    return merged_df.reset_index(drop=True)


relations = calculate_relation(cities, twinning)
print(relations)
fig = go.Figure()

fig.add_trace(
    go.Scattergeo(
        mode="markers", lon=cities["lon"], lat=cities["lat"], text=cities["name"]
    )
)

for i in range(len(relations)):
    fig.add_trace(
        go.Scattergeo(
            lon=[relations["lon_x"][i], relations["lon_y"][i]],
            lat=[relations["lat_x"][i], relations["lat_y"][i]],
            mode="lines",
            line=dict(width=0.1, color="red"),
        )
    )


# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
fig.layout.autosize = True
app.layout = html.Div(
    children=[
        html.H1(children="Sister Cities"),
        dcc.Graph(
            id="example-graph",
            figure=fig,
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
