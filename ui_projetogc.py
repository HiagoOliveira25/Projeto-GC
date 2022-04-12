from curses import color_content
from operator import invert
from turtle import width
from dash import html, Dash, Input, Output,callback, callback_context, exceptions
import dash_bootstrap_components as dbc
from rotinas_aux import card_color

import pandas as pd

dados = pd.read_excel('./grade_curricular.xlsx')
dados.fillna('',inplace=True)
print(dados)

mt_facil = 'light'
facil = 'info'
normal = 'primary'
dificil = 'warning'
mt_dificil = 'danger'
na = 'secondary'
btn = 'success'

tema_claro = dbc.themes.FLATLY
tema_escuro = dbc.themes.DARKLY

app = Dash(__name__, external_stylesheets=[tema_claro])
children_page = []
inputs = []
outputs = []
saida = []
j = 0
for i in range(11):
    children_p = []
    for index, dado in dados.iterrows():
        if dado['Periodo'] == i:
            color_df, inverte = card_color(dado['Dificuldade'],na,mt_facil, facil, normal, dificil, mt_dificil)

            children_p.append([dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.Div(f"{dado['Disciplina']}"),
                        html.Strong(f"{dado['Referencia']}")
                        ], style={'text-align':'center'}),
                    dbc.CardBody([
                        html.Strong(f"{dado['Codigo']}"),
                        html.Div(f"[{dado['Tipo']} - {dado['Creditos']}]"),
                        ], style={'text-align':'center'}),
                    dbc.CardFooter([
                        dbc.Row([
                            dbc.Col([html.Div(f'Pré-requisistos: '), html.Div(f'{dado["Pre-requisitos"]}')]),
                            dbc.Col([html.Div(f'Co-requisitos: '),html.Div(f'{dado["Co-requisitos"]}')]),
                            ]),
                        # dbc.Button(
                        #     'click para mais informações',
                        #     color = 'dark', 
                        #     id = f'btn_{dado["Referencia"]}',
                        #     n_clicks = 0
                        #     )
                    ], className="d-grid gap-2")
                ], color = color_df, inverse=inverte),width = 4, class_name='mb-4'),
                # dbc.Toast('funcionou',header='detalhes:', id = f'toast_{dado["Referencia"]}')
                ])

            # inputs.append(Input(f'btn_{dado["Referencia"]}', 'n_clicks'))
            # outputs.append(dict(saida = Output(f'toast_{dado["Referencia"]}', 'children')))
    
    children_page.append(dbc.Row(dbc.Card([
        dbc.CardHeader(html.H2(html.Strong(f'{i}º PERÍODO'))),
        dbc.CardBody(dbc.Row(children_p), id=f'p{i}')
    ])))

ap_v = html.Div(children_page)

children_overview = []
a = [b for b in range(1,11)]
a.append(0)
for i in a:
    col_overview = []
    for index, dado in dados.iterrows():
        if dado['Periodo'] == i and dado['Tipo'] != 'OP':
            color_df, inverte = card_color(dado['Dificuldade'],na,mt_facil,facil,normal, dificil, mt_dificil)
            card = dbc.Card(
                [html.Div(dado['Referencia']),html.Div(dado['Disciplina']), html.Div(dado['Creditos'])], 
                color=color_df, 
                inverse=inverte,
                style={'font-size':'0.75rem', 'text-align':'center'},
                className='mb-1')
            col_overview.append(card)

        elif dado['Periodo'] == 0 and i == 0:
            color_df, inverte = card_color(dado['Dificuldade'], na, mt_facil, facil, normal, dificil, mt_dificil)
            card = dbc.Card(
                [html.Div(dado['Referencia']),html.Div(dado['Disciplina']), html.Div(dado['Creditos'])], 
                color=color_df, 
                inverse=inverte,
                style={'font-size':'0.75rem', 'text-align':'center'},
                className='mb-1')
            col_overview.append(card)
        
    children_overview.append(dbc.Col(dbc.Card([
        dbc.CardHeader(f'P-{i}'),
        dbc.CardBody(col_overview, className='mb-1')], className='mb-1'), width = 3, className='mb-1'))
overview = dbc.Row(children_overview)

col_overview = []
for index, dado in dados.iterrows():
    if dado['Periodo'] != 0 and dado['Tipo'] == 'OP':
        color_df, inverte = card_color(dado['Dificuldade'],na,mt_facil, facil, normal, dificil, mt_dificil)
        card = dbc.Card(
            [html.Div(dado['Referencia']),html.Div(dado['Disciplina']), html.Div(dado['Creditos'])], 
            color=color_df, 
            inverse=inverte,
            style={'font-size':'0.75rem', 'text-align':'center'}, 
            className='mb-2')
        col_overview.append(card)

children_overview.append(dbc.Col(dbc.Card([
        dbc.CardHeader(f'P-OP'),
        dbc.CardBody(col_overview, className='mb-2')], className='mb-2'), width = 3, className='mb-2'))
overview = dbc.Row(children_overview)
ap_ov = html.Div(overview)

legend_2 = html.Div([
    dbc.Card([
        dbc.CardHeader(html.H3('UFPB MECFLUX', style={'text-align':'center'})),
        dbc.CardBody([
            dbc.Card([
                dbc.CardHeader("VISUALIZAÇÃO"),
                dbc.CardBody(
                    dbc.RadioItems(
                        options=[
                            {"label": "Detalhada", "value": 1},
                            {"label": "Overview", "value": 2},
                        ],
                        value=1,
                        id="mv_1",
                    ),
                    style={'text-align':'center'}
                )]),
            dbc.Card([
                dbc.CardHeader(html.H5('LEGENDA')),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col('Fácil'),
                        dbc.Col('Difícil', style={'text-align':'right'})
                    ]),
                    dbc.CardGroup([
                        dbc.Card(' ', color = mt_facil, style={'height':'1.5em'}),
                        dbc.Card(' ', color = facil),
                        dbc.Card(' ', color = normal),
                        dbc.Card(' ', color = dificil),
                        dbc.Card(' ', color = mt_dificil),
                    ]),
                    html.Hr(),
                    dbc.Row([
                        html.Div('Não avaliados:'),
                        html.Div(dbc.Card(' ', color = na, style={'height':'1.5em'}))
                    ], style={'text-align':'center'}),
                ], class_name='mb-4')
            ]),
        ], class_name='mb-2'),
        dbc.CardFooter([html.H6('PROJETO'), html.P('CAMEC - UFPB')],style={'text-align':'center'})
    ],style={'height':'100%'})],style={'position':'fixed'}, className='mb-4')
            



layout = html.Div([
    
    dbc.Row([
        dbc.Col('', width = 10, id='ver'),
        dbc.Col(legend_2,width = 2)
    ]),
    ])

#@callback(outputs, inputs)
#def detalhes(*args):
#    if args is None:
#        raise exceptions.PreventUpdate
#    ctx = callback_context

#    if not ctx.triggered:
#        button_id = 'No clicks yet'
#    else:
#        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

#    table_headers = [html.Th(f'Button {i+1}') for i in range(len(args))]
#    table_headers.append('Click mais recente')

#    table_itens = [html.Td(args[i] or 0) for i in range(len(args))]
#    table_itens.append(html.Td(button_id))
#    return html.Div([
#        html.Table([
#            html.Tr(table_headers),
#            html.Tr(table_itens)
#        ]),
#    ])
@app.callback(
    Output('ver', 'children'),
    Input('mv_1', 'value'))
def modo_de_visualizacao(mv):
    if ap_ov == None or mv == None or ap_v == None:
        raise exceptions.PreventUpdate

    if mv == 1:
        return ap_v
    else:
        return ap_ov


# @callback(
#     Output(outputs),
#     Input(inputs)
# )
# def btn_details(*args):
#     if args is None:
#         raise exceptions.PreventUpdate
#     ctx = callback_context

#     if not ctx.triggered:
#         button_id = 'No clicks yet'
#     else:
#         button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    

app.layout = html.Div(layout)

if __name__ == "__main__":
    app.run_server(debug=True)

