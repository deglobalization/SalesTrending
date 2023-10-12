import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
from dash import Dash, dash_table

from utils import Header, make_dash_table

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

def datelist_functions(x):
    return list(dict.fromkeys(x))

df_fund_facts = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))
df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))

df = pd.read_csv('products.csv', encoding='euc-kr')
data = pd.read_csv('sales-rawdata.csv', thousands = ',').query("사업부코드 == 10.0 and 년월 == 202301")
data = data[data['RX 총Net매출(VAT제외)']!=0].sort_values(by='년월')

date_list = data['년월'].dropna().to_list()
#date_list = list(dict.fromkeys(date_list))
date_options = datelist_functions(date_list)
date_options.sort()
date_length = len(date_options)

last_date = date_options[date_length - 1]

data = data[data['년월']==last_date]
data['Rx'] = data['RX 총Net매출(VAT제외)']

fig = px.treemap(data, path=[px.Constant("품목군별 볼륨 기준"), '품목군명', '품목명'], values='Rx',
                  color='Rx', hover_data=['품목명'],
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(data['품목단가']))
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))


def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("경기도"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                       구리시(이인철, 이지형), 남양주시(홍승현, 김두훈, 김승현, 박종우), 하남시(김병민, 이지형), 광주시(김서연, 김관태), 용인시(이희영, 박경현, 김인용, 이창준, 최유진), 평택시(이호진, 김승찬, 신민혜, 김태규)",
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                                                        html.H6(
                                        "수도6 품목별 현황",
                                        className="subtitle padded",
                                    ),
                        
                            dcc.Graph(
            id="graph",
            figure=fig
        ),
          
                    # Row 5
                    html.Div(
                        [
                            
                            html.Div(
                                [
                                    html.H6(
                                        "수도6 주요품목별 현황 (단위: 원)",
                                        className="subtitle padded",
                                    ),
                                    dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]),
                                ],
                                className="six columns",
                            ),
                           
                        ],
                        className="row ",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
