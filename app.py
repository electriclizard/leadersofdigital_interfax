# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from typing import Container
import dash
from dash.dependencies import Output, State, Input
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import json
from datetime import datetime
import base64

from infrastructure.db._base import DB
from handlers.get import get_service

print("Ipmports complete")

db = DB.factory('json', config={})

data = db.get_many(0, db.get_size())


app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP], title='Interfax')

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
], style={'backgroundColor': 'white'})


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Admin", href="/admin")),

    ],
    brand="Newsfeed",
    brand_href="/",
    color="#008080",
    dark=True,)


def make_news(news, num):
    if 'published_at' in news:

        date = datetime.strptime(
            news['published_at'][:-6], '%Y-%m-%d %H:%M:%S.%f')
    return dbc.Card(
        [
            html.P([
                html.Time("• " + date.strftime("%Y-%m-%d %H:%M") + " " if 'published_at' in news else None,
                          style={'color': 'grey', 'font-size': 'smaller'}),
                (news['headline'] or '')
            ], id='d'+str(news['id'])
            ),
            dbc.Tooltip(news['body'], target='d' +
                        str(news['id']), style={"width": "50vw", "maxWidth": "50vw"})
        ], style={'border': '0px'}

    )


def make_cluster(cluster, num):
    return dbc.Card([
        dbc.CardHeader(
            children=[html.H4(cluster['title']+" - Ground Truth") if 'title' in cluster else None,
                      html.H4(cluster['generated_title']+" - Сгенерированный заголовок") if 'generated_title' in cluster else None, ]

        ),
        dbc.CardBody(
            [
                make_news(cluster['news'][i], i) for i in range(len(cluster['news']))
            ]
        )], style={'margin': '20px', 'border-radius': '20px'})


index_page = html.Div([
    navbar,
    dbc.Container(children=[
        dbc.Row([
            html.H1('Темы новостей', style={'margin': '10px'}),
            # html.Div('Здесь расположены карточки со статьями'),
            # html.Div('Сортировка карточек от новой к старой'),
            # html.Div('в карточке открыта новейшая и закрыты старые статьи'),
            # html.Div('Заголовок карточки - тематика'),
            dbc.Button('обновить', id='reload-button',
                       className="mb-3", style={'margin': '10px'}),
        ]),
        # dcc.Store(id='clusters'),
        html.Div(dbc.Spinner(color="primary"),
                 id="cluster-cards", style={'align': 'center'})

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
            # options=[{'label': i, 'value': i} for i in [
            #     'bert_header', 'ngram_header', 'dummy_header', ]],
            options=[{'label': 'Нейросетевой генератор bert', 'value': 'bert_header'}, {
                'label': 'Статистический генератор', 'value': 'ngram_header'}],
            placeholder="Выберите модель"
        ),
        html.Div(),
        dbc.Spinner(color="primary", id='page-1-content',),
        dcc.Store(id='news-json'),
        dcc.Store(id='article-title'),
        html.Div(id="is_saved")
    ])
])


def validateJSON(jsondata):
    if 'title' in jsondata[0]:
        return 'multiple'
    if 'body' in jsondata[0]:
        return 'single'
    return None


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

            JSONtype = validateJSON(article)
            print(JSONtype)

            if JSONtype == None:
                return ['Формат JSON не соответствует требуемому. Если хотите загрузить одну тему, обязательно наличие "body" в элементах списка. Если необходимо обработать несколько тем, необходимо наличие "title" в элементах'], None

            if JSONtype == 'single':
                return [make_news(article[i], i) for i in range(len(article))], article

            if JSONtype == 'multiple':
                return [html.H3('Вы загрузили '+str(len(article))+' тем, обработка займет больше времени')]+[make_cluster(article[i], i) for i in range(len(article))], article
        else:
            return "Загрузите файл формата json", None
    else:
        return "загрузите тестовый файл с кластером новостей", None


def create_choice(title):
    return dbc.RadioItems(
        options=[{'label': i, 'value': i} for i in title],
        value='choose',
        id='choice'
    )
    # return [html.H2(i) for i in title]


@app.callback(Output('article-title', 'data'), Input('choice', 'value'))
def changeTitle(value):
    return value


@app.callback(Output('page-1-content', 'children'),

              Input('page-1-dropdown', 'value'),
              State('news-json', 'data'))
def dropdown(value, article):
    if not article:
        return "Сначала загрузите данные", None

    JSONType = validateJSON(article)

    if value:

        if JSONType == 'single':
            header_generator_service = get_service(value)
            title = header_generator_service.create_cluster_header(
                article
            ).header

            return ['Выбранная модель: "{}"'.format(value), create_choice(title),
                    dbc.Button('сохранить результат в базу',
                               id='save-button', n_clicks=0)]

        if JSONType == 'multiple':
            title = []
            for i in range(len(article)):
                finaldict = {}
                news = article[i]['news']
                header_generator_service = get_service(value)
                result = header_generator_service.create_cluster_header(
                    news
                ).header
                finaldict[article[i]['title']] = result
                title.append(finaldict)

            return['Выбранная модель: "{}"'.format(value), html.Br(), generate_table(title)]
    else:
        return ['модель не выбрана']


def gen_row(dct):
    print(dct)
    return [html.Td(list(dct.keys())[0]), html.Td(list(dct.values())[0][0])]


def generate_table(data):

    return dbc.Table([
        html.Thead([html.Th('Ground Truth'), html.Th(
            'Сгенерированный заголовок')]),
        html.Tbody(
            [html.Tr(gen_row(dct)) for dct in data]
        )
    ]
    )


@app.callback(
    Output('is_saved', 'children'),
    [Input('save-button', 'n_clicks')],
    State('news-json', 'data'),
    State('article-title', 'data'),
)
def save_to_db(click, cluster, title):
    if (click) & (validateJSON(cluster) == 'single'):
        db.insert_one({'generated_title': title, 'news': cluster})
        return "Сохранено!"

    # if click & len(title) > 1:
    #     result = []
    #     for k in range(len(cluster)):
    #         news = cluster[k]
    #         news['generated_title'] = title[k][news['title']][0]
    #         result.append(news)
    #     db.insert_many(result)
    #     return "Сохранено все!"
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
    app.run_server(host='0.0.0.0')
