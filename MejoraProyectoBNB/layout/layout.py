from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

PLOTLY_LOGO = "https://raw.githubusercontent.com/joelsilva11/Mapas/main/logo-blanco.png"


###################################################################crea la barra de titulo
navbar = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(html.Img(src=PLOTLY_LOGO, height="60px"),width=1),
                dbc.Col(dbc.NavbarBrand("VISUALIZACIÓN DE MAPAS DE CALOR CON CONTORNOS DE DENSIDAD", className="ms-2",style={'font-size': '36px'}), width=9),
                ############################################### Inicio Div que contiene al Boton que ejecuta el KDE
                dbc.Col(
                    html.Div(
                        dbc.Button('Run KDE Analysis', id='kde-button', n_clicks=0, style={'width': '100%','height': '50px'}, color="success"),
                        id='kde-button_container', 
                        style={'display': 'none'},
                    )
                ),
                ############################################### Fin Div que contiene al Boton que ejecuta el KDE
            ],
            align="center",
            style={
                "margin": "0", 
                "width": "100%"
            },
        ),
        
    ],
    color="dark",
    dark=True,
)
###################################################################funciones para crear los inputs
def generate_inputs (num_of_inputs):
    inputs = []
    texts = [
        'Banco BNB',
        'Otros Bancos',
        'ATMs',
        'SuperMercados',
        'Centros Médicos',
        'Hoteles',
        'Otros'
    ]
    for i in range(num_of_inputs):
        if i % 2 == 0:
            text_index = i // 2  # Índice para determinar el texto correspondiente
            input_item = dbc.Row(
                [
                    dbc.Col(html.H5(texts[text_index]), width=12),  # Texto en la parte superior
                    dbc.Col(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Peso",style={'width': '60px'}),
                                dcc.Input(
                                    id={'type': 'input', 'index': i},
                                    type='number',
                                    min=0,
                                    max=10,
                                    placeholder=f'Enter something here...',
                                ),
                            ]
                        ), width=12
                    )
                ]
            )
        else:
            input_item = dbc.Row(
                [
                    dbc.Col(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Radio",style={'width': '60px'}),
                                dcc.Input(
                                    id={'type': 'input', 'index': i},
                                    type='number',
                                    min=0,
                                    max=500,
                                    placeholder=f'Enter something here...',
                                ),
                            ]
                        ), width=12
                    )
                ]
            )
        inputs.append(input_item)
    return inputs

#funcion para crear el dropdown aun no existe solo hasta que el callback recibe el csv
def create_dropdown(df,selected_column,dropdown_id,titulo='Sin nombre'):
    unique_values = df[selected_column].dropna().unique()
    unique_values = sorted(unique_values, key=str)  # Ordenar los valores
    ############################################## Inicio del Div que contiene el Dropdown
    dropdown = html.Div(children=[
                    html.Label(titulo),
                    dcc.Dropdown(
                                id=dropdown_id,
                                options=[{'label': str(i), 'value': str(i)} for i in unique_values],
                                value=None,  # No se selecciona ninguna opción por defecto
                                multi=True,
                                style={
                                    'backgroundColor': '#333',
                                    'color': '#fff',
                                    'width': '100%'
                                }
                    ),
                ], 
                style={
                    'width': '100%',
                    #'padding': 5,
                    #'padding-top': 2,
                    'padding-right': 5,
                    'padding-bottom': 7,
                    'padding-left': 5,
                    'backgroundColor': '#333'
                }
                )
    ############################################## Fin del Div que contiene el Dropdown
    return dropdown






#############################################################################################################################################
#Estructura principal de la pagina
#############################################################################################################################################

layout = html.Div([
    ################################################### Inicio Barra de título
    navbar,
    ################################################### Fin Barra de título
    ################################################### Inicio Div pantalla principal
    html.Div([
        ############################################### Inicio Div que contiene upload y mapa a la vez
        html.Div([
            ############################################### Inicio Div que contiene upload
            html.Div([
                ############################################### Inicio objeto Upload
                dcc.Upload(
                    id='upload-csv', #Id Upload
                    children=html.Div([
                        'Arrastre y suelte o ',
                        html.A('Seleccione Archivos')
                    ]),
                    style={
                        'width': '99%',
                        'height': '88vh',
                        'display': 'flex',  # Esto permite utilizar las propiedades flexbox para centrar el contenido
                        'justify-content': 'center',  # Centra el contenido horizontalmente
                        'align-items': 'center',  # Centra el contenido verticalmente
                        'lineHeight': '60px',
                        'borderWidth': '2px',
                        'borderStyle': 'dashed',
                        'borderRadius': '20px',
                        'textAlign': 'center',
                        'margin': '10px'
                    }
                ),
                ############################################### Fin objeto Upload
            ], 
            id='upload-container' #Id contenedor del Upload
            ),
            ############################################### Fin Div que contiene upload
            ############################################### Inicio Div que contiene Grafico mapa
            html.Div(
                dcc.Graph(
                    id='map-scatter',
                    style={'height': '90vh'}
                ),
                id='map-container',
                style={
                    'display': 'none'
                }
            ),
            ############################################### Fin Div que contiene Grafico mapa
        ],
        style={
            'padding': 5, 
            'flex': 8.5
        }
        ),
        ############################################### Fin Div que contiene upload y mapa a la vez
        ############################################### Inicio Div que contiene los Dropdown
        html.Div([
            ############################################### Inicio Div que contiene al Boton que oculta el canvas
            html.Div(
                        dbc.Button('Editar parámetros', id='open-offcanvas', n_clicks=0, style={'width': '100%','height': '50px'}, color='primary'),
                        id='offcanvas-button-container', 
                        style={'display': 'none'},
                    ),
            ############################################### Fin Div que contiene al Boton que oculta el canvas
            ############################################### Inicio Div que contiene al Dropdown1 que filtra Clase
            html.Div(
                [
                dcc.Dropdown(
                    id='Dropdown_1', #debe existir un dropdown antes de mostrarse para evitar errores
                    options=[],
                    value=None,
                    style={
                    'display': 'none'
                    }
                )],
                id='Dropdown_container_1', 
                style={
                'padding-bottom': 5, 
                }
            ),
            ############################################### Fin Div que contiene al Dropdown1
            ############################################### Inicio Div que contiene al Dropdown2 que filtra bancos
            html.Div(
                [
                dcc.Dropdown(
                    id='Dropdown_2', #debe existir un dropdown antes de mostrarse para evitar errores
                    options=[],
                    value=None,
                    style={
                    'display': 'none'
                    }
                )],
                id='Dropdown_container_2', 
                style={
                'padding-bottom': 5, 
                }
            ),
            ############################################### Fin Div que contiene al Dropdown2
            ############################################### Inicio Div que contiene al Dropdown3 que filtra tipo de agencia
            html.Div(
                [
                dcc.Dropdown(
                    id='Dropdown_3', #debe existir un dropdown antes de mostrarse para evitar errores
                    options=[],
                    value=None,
                    style={
                    'display': 'none'
                    }
                )],
                id='Dropdown_container_3', 
                style={
                'padding-bottom': 5, 
                }
            ),
            ############################################### Fin Div que contiene al Dropdown3
            ############################################### Inicio Div que contiene al Dropdown6 que filtra tipo de ATM
            html.Div(
                [
                dcc.Dropdown(
                    id='Dropdown_6', #debe existir un dropdown antes de mostrarse para evitar errores
                    options=[],
                    value=None,
                    style={
                    'display': 'none'
                    }
                )],
                id='Dropdown_container_6', 
                style={
                'padding-bottom': 5, 
                }
            ),
            ############################################### Fin Div que contiene al Dropdown6
            ############################################### Inicio Div que contiene al Dropdown4 que filtra tipo Centro médico
            html.Div(
                [
                dcc.Dropdown(
                    id='Dropdown_4', #debe existir un dropdown antes de mostrarse para evitar errores
                    options=[],
                    value=None,
                    style={
                    'display': 'none'
                    }
                )],
                id='Dropdown_container_4', 
                style={
                'padding-bottom': 5, 
                }
            ),
            ############################################### Fin Div que contiene al Dropdown4
            ############################################### Inicio Div que contiene al Dropdown5 que filtra tipo hospedaje
            html.Div(
                [
                dcc.Dropdown(
                    id='Dropdown_5', #debe existir un dropdown antes de mostrarse para evitar errores
                    options=[],
                    value=None,
                    style={
                    'display': 'none'
                    }
                )],
                id='Dropdown_container_5', 
                style={
                'padding-bottom': 5, 
                }
            ),
            ############################################### Fin Div que contiene al Dropdown5
        ],
        style={
                'flex-direction': 'column',
                #'padding': 5,
                'padding-top': 5,
                'padding-right': 5,
                'padding-bottom': 5, 
                'flex': 1.5
        }
        ),
        ############################################### Fin Div que contiene los Dropdown
    ], 
    style={
        'display': 'flex', 
        'flex-direction': 'row'
    }
    ),
    ############################################### Inicio de la ventana desplegable
    dbc.Offcanvas(
        dbc.Container([
            dbc.Row(
                dbc.Col(
                    generate_inputs(14),
                    width=12
                ),
                justify="center"
            ),
            dbc.Row(  # Agregamos una nueva fila para el botón
                dbc.Col(
                    dbc.Button("Cargar Datos", id="export-button", color="success",
                               style={"marginTop": "50px", "width": "100%"}
                               ),
                    width=12,
                ),
                justify="center",
            )
        ]),
        id="offcanvas",
        title="Editar Peso y Radios",
        is_open=False,
        scrollable=True,
    ),
    ############################################### Fin de la ventana desplegable
    dcc.Store(id='store-inputs'),
    ################################################### Fin Div pantalla principal
    ################################################### Inicio para almacenar el df para que pueda ser usado en otros callbacks
    dcc.Store(id='intermediate-value'),
    ################################################### Fin para almacenar el df para que pueda ser usado en otros callbacks
    ################################################### Inicio para almacenar el KDE en un geojson
    dcc.Store(id='kde-output'),
    ################################################### Fin para almacenar el KDE en un geojson
    ################################################### Inicio para almacenar el df que sera filtado por los dropdowns
    dcc.Store(id='filter-value'),
    ################################################### Fin para almacenar el df que sera filtado por los dropdowns
    ################################################### Inicio para almacenar el df tranformado por los inputs
    dcc.Store(id='store-transformed')
    ################################################### Fin para almacenar el df tranformado por los inputs
])

#############################################################################################################################################
#Estructura principal de la pagina
#############################################################################################################################################
