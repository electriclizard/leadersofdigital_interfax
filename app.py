# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from typing import Container
import dash
from dash.dependencies import Output, State, Input
from dash_bootstrap_components._components.Collapse import Collapse
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_html_components.Tr import Tr
import pandas as pd
import json
import re
import base64

from infrastructure.db._base import DB
from handlers.header_generation import get_service


db = DB.factory('json', config={})

data = db.get_many(0, db.get_size())


app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP], title='Interfax')

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Admin", href="/admin")),

    ],
    brand="Home",
    brand_href="/",
    color="primary",
    dark=True,)


def make_news(news, num):
    return dbc.Card(
        [
            dbc.CardHeader(
                dbc.Button(
                    news['headline'],
                    n_clicks=0,
                    color="link",
                    style={'textAlign': 'left'})
            ),
        ]
    )
    pass


def make_cluster(cluster, num):
    return dbc.Card([
        dbc.CardHeader(html.H4(cluster['title'])),
        dbc.CardBody(
            [
                    make_news(cluster['news'][i], i) for i in range(len(cluster['news']))
                    ]
        )])


index_page = html.Div([
    navbar,
    dbc.Container(children=[
        html.H1('Страница с новостями - карточки новостей, объединенныe по темам'),
        html.Div('Здесь расположены карточки со статьями'),
        html.Div('Сортировка карточек от новой к старой'),
        html.Div('в карточке открыта новейшая и закрыты старые статьи'),
        html.Div('Заголовок карточки - тематика'),


    ]+[make_cluster(data[i], i) for i in range(100)])
])


adminPanel = html.Div([

    navbar,
    dbc.Container(children=[

        html.H1('Админка'),
        dcc.Upload(
            id="upload_file",
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),
        html.Div(id='output-data-upload'),
        dcc.Dropdown(
            id='page-1-dropdown',
            options=[{'label': i, 'value': i} for i in [
                'TF-IDF', 'Bert', 'ruGPT-3', 'ARTM', 'Ручные правила']],
            placeholder="Выберите модель"
        ),
        html.Div(id='page-1-content'),

    ])

])


@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload_file', 'contents'),
    State('upload_file', 'filename')
)
def upload_file(content, filename):
    if filename:
        if 'json' in filename:
            content_type, content_string = content.split(',')

            decoded = base64.b64decode(content_string)
            text = decoded.decode('utf-8')
            article = json.loads(text)

            # return [news['body']+'\n' for news in article]
            return [make_news(article[i], i) for i in range(len(article))]
        else:
            return "Загрузите файл формата json"
    else:
        return "загрузите тестовый файл с кластером новостей"


@app.callback(Output('page-1-content', 'children'),
              Input('page-1-dropdown', 'value'),
              State('upload_file', 'contents'))
def page_1_dropdown(value, content):
    if not content:
        return "Сначала загрузите данные"

    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    text = decoded.decode('utf-8')
    article = json.loads(text)

    if value:
        header_generator_service = get_service(value)
        return ['Выбранная модель: "{}"'.format(value),
                html.H2(header_generator_service.create_cluster_header(
                    article
                ).header),
                dbc.Button('сохранить в базу?')
                ]
    else:
        header_generator_service = get_service('random_header')
        return ['модель не выбрана',
                html.H2(header_generator_service.create_cluster_header(
                    article
                ).header),
                ]


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/admin':
        return adminPanel
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)
