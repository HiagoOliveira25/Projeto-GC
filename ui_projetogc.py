from curses import color_content
from operator import invert
from turtle import width
from dash import html, Dash, Input, Output,callback, callback_context, exceptions
import dash_bootstrap_components as dbc

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

app = Dash(__name__, external_stylesheets=[tema_escuro])
children_page = []
inputs = []
outputs = []
for i in range(11):
    children_p = []
    for index, dado in dados.iterrows():
        if dado['Periodo'] == i:
            inverte = True
            if dado['Dificuldade'] == 0:
                color_df = na 
                inverte = False
            elif dado['Dificuldade'] == 1:
                color_df = mt_facil
                inverte = False
            elif dado['Dificuldade'] == 2:
                color_df = facil
            elif dado['Dificuldade'] == 3:
                color_df = normal
            elif dado['Dificuldade'] == 4:
                color_df = dificil
            elif dado['Dificuldade'] == 5:
                color_df = mt_dificil

            children_p.append(dbc.Col(
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
#                        dbc.Button(
#                            'click para mais informações',
#                            color = 'dark', 
#                            id = f'btn_{dado["Referencia"]}',
#                            n_clicks = 0
#                            )
                    ], className="d-grid gap-2")
                ], color = color_df, inverse=inverte),width = 4, class_name='mb-4'))

#            inputs.append(Input(f'btn_{dado["Referencia"]}', 'n_clicks'))
#            outputs.append(Output(f'toast_{dado["Referencia"]}', 'children'))
    
    children_page.append(dbc.Row(dbc.Card([
        dbc.CardHeader(html.H2(html.Strong(f'{i}º PERÍODO'))),
        dbc.CardBody(dbc.Row(children_p), id=f'p{i}')
    ])))


legend_2 = html.Div([
    dbc.Card([
        dbc.CardHeader(html.H3('LEGENDA')),
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
    ],style={'position':'fixed'}), ])
            
layout = html.Div([
    dbc.Row([

    ], id = 'Titulo'),
    dbc.Row([
        dbc.Col(children_page, width = 10),
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

app.layout = html.Div(layout, id = 'core_page')



if __name__ == "__main__":
    app.run_server(debug=True)