# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from typing import Container
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

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

index_page = html.Div([
    navbar,
    dbc.Container(children=[
        html.H1('Страница с новостями - карточки новостей, объединенныe по темам'),
        html.Div('Здесь расположены карточки со статьями'),
        html.Div('Сортировка карточек от новой к старой'),
        html.Div('в карточке открыта новейшая и закрыты старые статьи'),
        html.Div('Заголовок карточки - тематика')
    ])

])

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
