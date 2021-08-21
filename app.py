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

with open('dataset_public.json') as inputJSON:
    data = json.load(inputJSON)
    inputJSON.close


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
                    # id=str(num)+'button',
                    n_clicks=0,
                    color="link",
                    style={'textAlign': 'left'})
            ),


        ]
        # +
        # [dbc.Collapse(

        #     dbc.CardBody(cluster['news'][0]['body']),
        #     id=str(num),
        #     is_open=False
        # )]
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


# @app.callback(
#     [Output(str(i), 'is_open') for i in range(100)],
#     [Input(str(i)+'button', 'n_clicks')for i in range(100)],
#     [State(str(i), 'is_open')for i in range(100)]
# )
# def toogle_news(*args):
#     ctx = dash.callback_context

#     if not ctx.triggered:
#         return [False for i in range(100)]
#     else:
#         button_id = re.match(r'\d+',ctx.triggered[0]["prop_id"].split(".")[0])[0]

#     stateList = list(args[int(len(args)/2):])
#     stateList[int(button_id)]= not stateList[int(button_id)]
#     return stateList


adminPanel = html.Div([

    navbar,
    dbc.Container(children=[

        html.H1('Админка'),
        dcc.Dropdown(
            id='page-1-dropdown',
            options=[{'label': i, 'value': i} for i in [
                'TF-IDF', 'Bert', 'ruGPT-3', 'ARTM', 'Ручные правила']],
            placeholder="Выберите модель"
        ),
        html.Div(id='page-1-content'),
        html.Div(children=[
            "Возможно потребуется textarea для статьи и кнопка 'Предложить название'",
            html.Br(),
            "На этой странице должен быть выбор статьи или кластера",
            html.Br(),
            "После выбора будет предложено название темы?"]),
    ])

])


@app.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    if value:
        return ['Выбранная модель: "{}"'.format(value)]
    else:
        return 'модель не выбрана'


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
