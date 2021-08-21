# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from typing import Container
import dash
from dash.dependencies import Output, State, Input
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_html_components.Tr import Tr
import pandas as pd
import json
import re
import base64

from infrastructure.db._base import DB
from handlers.get import get_service
# def get_service():
#     return 'ПУТИН'

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
            dbc.CardHeader(children=[
                html.H4(
                    news['headline'],
                    title=news['body'],
                    
                    
                    style={'textAlign': 'left'}),
                ]
            ),
            # dbc.Tooltip(children=news['body'], target='b'+str(news['id']), placement='bottom')
        ],
        id='b'+str(news['id']),
        className='mb-3'
    )


def make_cluster(cluster, num):
    return dbc.Card([
        dbc.CardHeader(html.H4(cluster['title'])),
        dbc.CardBody(
            [
                    make_news(cluster['news'][i], i) for i in range(len(cluster['news']))
                    ]
        )], className="mb-3")


index_page = html.Div([
    navbar,
    dbc.Container(children=[
        html.H1('Темы новостей'),
        # html.Div('Здесь расположены карточки со статьями'),
        # html.Div('Сортировка карточек от новой к старой'),
        # html.Div('в карточке открыта новейшая и закрыты старые статьи'),
        # html.Div('Заголовок карточки - тематика'),
        dbc.Button('обновить', id='reload-button', className="mb-3"),
        # dcc.Store(id='clusters'),
        html.Div(dbc.Spinner(color="primary"), id="cluster-cards")

    ])
])


@app.callback(

    Output('cluster-cards', 'children'),
    Input('reload-button', 'n_clicks')
    
)
def reload(n):

    data = db.get_many(0, db.get_size())
    return [make_cluster(data[i], i) for i in range(len(data))[::-1]]


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
                'tf_idf_header', 'ngram_header', 'dummy_header', ]],
            placeholder="Выберите модель"
        ),
        html.Div(id='page-1-content'),
        dcc.Store(id='news-json'),
        dcc.Store(id='article-title'),
        html.Div(id="is_saved")


    ])

])


@app.callback(
    Output('output-data-upload', 'children'),
    Output('news-json', 'data'),
    Input('upload_file', 'contents'),
    State('upload_file', 'filename'),
)
def upload_file(content, filename):
    if filename:
        if 'json' in filename:
            content_type, content_string = content.split(',')

            decoded = base64.b64decode(content_string)
            text = decoded.decode('utf-8')
            article = json.loads(text)

            # return [news['body']+'\n' for news in article]
            return [make_news(article[i], i) for i in range(len(article))], article
        else:
            return "Загрузите файл формата json", None
    else:
        return "загрузите тестовый файл с кластером новостей", None


@app.callback(Output('page-1-content', 'children'),
              Output('article-title', 'data'),
              Input('page-1-dropdown', 'value'),
              State('news-json', 'data'))
def dropdown(value, article):
    if not article:
        return "Сначала загрузите данные", None

    if value:
        header_generator_service = get_service(value)
        title = header_generator_service.create_cluster_header(
            article
        ).header
        return ['Выбранная модель: "{}"'.format(value),
                html.H2(title),
                dbc.Button('сохранить результат в базу',
                           id='save-button', n_clicks=0)
                ], title
    else:
        header_generator_service = get_service('random_header')
        title = header_generator_service.create_cluster_header(
            article
        ).header
        return ['модель не выбрана',
                html.H2(title),
                dbc.Button('сохранить результат в базу',
                           id='save-button', n_clicks=0)
                ], title


@app.callback(
    Output('is_saved', 'children'),
    [Input('save-button', 'n_clicks')],
    State('news-json', 'data'),
    State('article-title', 'data'),
)
def save_to_db(click, cluster, title):
    # print(click, cluster, title)
    if click:
        db.insert_one({'title': title, 'news': cluster})
        # print(click, cluster, title)
        return "Сохранено!"
    else:
        return None


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/admin':
        return adminPanel
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)
