import pandas as pd
from dash import Dash, Input, Output, dcc, html
import numpy as np

def datelist_functions(x):
    return list(dict.fromkeys(x))



data = pd.read_csv('sales-rawdata.csv', thousands = ',').query("사업부코드 == 10.0")
data = data[data['RX 총Net매출(VAT제외)']!=0].sort_values(by='년월')

date_list = data['년월'].dropna().to_list()
#date_list = list(dict.fromkeys(date_list))
date_options = datelist_functions(date_list)
date_options.sort()
date_length = len(date_options)

last_date = date_options[date_length - 1]

#data = data[data['년월']==last_date]
data['Rx'] = data['RX 총Net매출(VAT제외)']

data['년월'] = pd.to_datetime(data['년월'], format="%Y%m")
regions = data["담당자명"].sort_values().unique()
avocado_types = data["품목명"].sort_values().unique()

data['region'] = data['담당자명']
data['type'] =data['품목명']
data['Date'] = data['년월']

#data = (
#    pd.read_csv("avocado.csv")
#    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
#    .sort_values(by="Date")
#)
#regions = data["region"].sort_values().unique()
#avocado_types = data["type"].sort_values().unique()

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Avocado Analytics: Understand Your Avocados!"

def create_layout(app):
    return html.Div(
        children=[
            html.Div(
                children=[
                    html.P(children="🥑", className="header-emoji"),
                    html.H1(
                        children="Avocado Analytics", className="header-title"
                    ),
                    html.P(
                        children=(
                            "Analyze the behavior of avocado prices and the number"
                            " of avocados sold in the US between 2015 and 2018"
                        ),
                        className="header-description",
                    ),
                ],
                className="header",
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(children="Region", className="menu-title"),
                            dcc.Dropdown(
                                id="region-filter",
                                options=[
                                    {"label": region, "value": region}
                                    for region in regions
                                ],
                                value="Albany",
                                clearable=False,
                                className="dropdown",
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Div(children="Type", className="menu-title"),
                            dcc.Dropdown(
                                id="type-filter",
                                options=[
                                    {
                                        "label": avocado_type.title(),
                                        "value": avocado_type,
                                    }
                                    for avocado_type in avocado_types
                                ],
                                value="organic",
                                clearable=False,
                                searchable=False,
                                className="dropdown",
                            ),
                        ],
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children="Date Range", className="menu-title"
                            ),
                            dcc.DatePickerRange(
                                id="date-range",
                                min_date_allowed=data["년월"].min().date(),
                                max_date_allowed=data["년월"].max().date(),
                                start_date=data["년월"].min().date(),
                                end_date=data["년월"].max().date(),
                            ),
                        ]
                    ),
                ],
                className="menu",
            ),
            html.Div(
                children=[
                    html.Div(
                        children=dcc.Graph(
                            id="price-chart",
                            config={"displayModeBar": False},
                        ),
                        className="card",
                    ),
                    html.Div(
                        children=dcc.Graph(
                            id="volume-chart",
                            config={"displayModeBar": False},
                        ),
                        className="card",
                    ),
                ],
                className="wrapper",
            ),
        ]
    )


@app.callback(
    Output("price-chart", "figure"),
    Output("volume-chart", "figure"),
    Input("region-filter", "value"),
    Input("type-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_charts(region, avocado_type, start_date, end_date):
    filtered_data = data.query(
        "region == @region and type == @avocado_type"
        " and Date >= @start_date and Date <= @end_date"
    )
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["년월"],
                "y": filtered_data["RX 총Net매출(VAT제외)"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["년월"],
                "y": filtered_data["RX 총Net매출(VAT제외)"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return price_chart_figure, volume_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
