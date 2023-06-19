import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, callback_context

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
tile_icon = 'https://raw.githubusercontent.com/joelsilva11/GIS/main/tile_icon_2.png'
options = [{'label': f'Opción {i+1}', 'value': f'Valor {i+1}'} for i in range(10)]
options2 = [{'label': f'Opc {i+1}', 'value': f'Numero {i+1}'} for i in range(10)]
options3 = [{'label': f'Opt {i+1}', 'value': f'Num {i+1}'} for i in range(10)]

def create_dp_tile(id_suffix,tl_icon,tl_title,tl_options):
    button_id = f'tl-button-{id_suffix}'
    list_id = f'tl-list-{id_suffix}'
    container_id = f'tl-container-list-{id_suffix}'
    icon_id = f'tl-icon-{id_suffix}'

    return html.Div(
        [
            html.Div(
            [
                html.Img(src= tl_icon,id=icon_id, style={'width':'25px', 'height':'25px'})
            ], 
            id= button_id,
            style={
                'borderRadius': '5px',
                'backgroundColor': '#492',
                'padding':'7px',
                'display': 'inline-block', # Agregado
            }
            ),
            html.Div(
            [
                html.H6(tl_title, style={'padding': '4px 8px 0px 8px'}),
                dbc.RadioItems(
                    options=tl_options, 
                    value=[], 
                    id=list_id, 
                style={
                    'padding': '0px 4px 4px 8px',
                    #'backgroundColor': '#222',
                    'border-bottom-left-radius': '5px',
                    'border-bottom-right-radius': '5px',
                }
                ),
            ],
            id= container_id,
            style={
                    'backgroundColor': '#333',
                    'borderRadius': '5px',
                    'position': 'absolute', 
                    'z-index': '100',
                    #'display': 'inline-block', # Agregado
                    'display':'none',
            },
            ),

        ],
        style={
            'position': 'relative', 
            'borderRadius': '4px',
            'top': '10px', 
            'left': '10px', 
            #'z-index': '10',
            #'height': '88px',
        }
    )

def create_dp_layer(id_suffix,tl_icon,tl_title,tl_options):
    button_id = f'ly-button-{id_suffix}'
    list_id = f'ly-list-{id_suffix}'
    container_id = f'ly-container-list-{id_suffix}'
    icon_id = f'ly-icon-{id_suffix}'

    return html.Div(
        [
            html.Div(
            [
                html.Img(src= tl_icon,id=icon_id, style={'width':'25px', 'height':'25px'})
            ], 
            id= button_id,
            style={
                'borderRadius': '5px',
                'backgroundColor': '#492',
                'padding':'7px',
                'display': 'inline-block', # Agregado
            }
            ),
            html.Div(
            [
                html.H6(tl_title, style={'padding': '4px 8px 0px 8px'}),
                dbc.Checklist(
                    options=tl_options, 
                    value=[], 
                    id=list_id, 
                style={
                    'padding': '0px 4px 4px 8px',
                    #'backgroundColor': '#222',
                    'border-bottom-left-radius': '5px',
                    'border-bottom-right-radius': '5px',
                }
                ),
            ],
            id= container_id,
            style={
                    'backgroundColor': '#333',
                    'borderRadius': '5px',
                    'position': 'absolute', 
                    'z-index': '100',
                    #'display': 'inline-block', # Agregado
                    'display':'none',
            },
            ),

        ],
        style={
            'position': 'relative', 
            'borderRadius': '4px',
            'top': '10px', 
            'left': '10px', 
            #'z-index': '10',
            #'height': '88px',
        }
    )

# Usar la función para crear componentes
dropdown1 = create_dp_tile('1',tile_icon,'Mapa base',options)
dropdown2 = create_dp_layer('1',tile_icon,'Mapa base',options)
app.layout = html.Div(
    [
       dropdown1,
       dropdown2 
    ],
    style={
            'position': 'absolute', }
                    
)


if __name__ == '__main__':
    app.run_server(debug=True)