import dash_html_components as html
import dash_core_components as dcc


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
    
                    html.A(
                        html.Button(
                            "지도맵 확대",
                            id="learn-more-button",
                            style={"margin-left": "-10px"},
                        ),
                        href="http://byeongmin.pythonanywhere.com/",
                    ),
                    html.A(
                        html.Button("거래처 검색", id="learn-more-button"),
                        href="https://deglobalization.github.io/pyscript",
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("의원사업부 매출 현황")],
                        className="seven columns main-title",
                    ),
                    html.Div(

                        className="five columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "품목별 현황",
                href="/dash-financial-report/overview",
                className="tab first",
            ),
            dcc.Link(
                "담당자 현황",
                href="/dash-financial-report/price-performance",
                className="tab",
            ),
            dcc.Link(
                "거래처 현황",
                href="/dash-financial-report/portfolio-management",
                className="tab",
            ),
            dcc.Link(
                "지역별 현황", href="/dash-financial-report/fees", className="tab"
            ),
            dcc.Link(
                "포트폴리오 전략",
                href="/dash-financial-report/distributions",
                className="tab",
            ),
            dcc.Link(
                "품절 대응",
                href="/dash-financial-report/news-and-reviews",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table
