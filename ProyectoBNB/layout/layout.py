from dash import dcc, html
import dash_bootstrap_components as dbc

PLOTLY_LOGO = "https://raw.githubusercontent.com/joelsilva11/Mapas/main/logo-blanco.png"

navbar = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(html.Img(src=PLOTLY_LOGO, height="60px"),width=1),
                dbc.Col(dbc.NavbarBrand("VISUALIZACIÓN DE MAPAS DE CALOR CON CONTORNOS DE DENSIDAD", className="ms-2",style={'font-size': '36px'}), width=9),
                dbc.Col(
                    html.Div(
                        dbc.Button('Run KDE Analysis', id='kde-button', n_clicks=0, style={'width': '100%','height': '50px'}, color='primary'),
                        id='kde-button_container', 
                        style={'display': 'none'},
                    )
                ),
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
            ############################################### Inicio Div que contiene al Boton que ejecuta el KDE
            
            ############################################### Fin Div que contiene al Boton que ejecuta el KDE
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
    ################################################### Fin Div pantalla principal
    ################################################### Inicio para almacenar el df para que pueda ser usado en otros callbacks
    dcc.Store(id='intermediate-value'),
    ################################################### Fin para almacenar el df para que pueda ser usado en otros callbacks
    ################################################### Inicio para almacenar el KDE en un geojson
    dcc.Store(id='kde-output'),
    ################################################### Fin para almacenar el KDE en un geojson
    ################################################### Inicio Boton que genera el KDE
    
    ################################################### Fin Boton que genera el KDE
    ################################################### Inicio para almacenar el df que sera filtado por los dropdowns
    dcc.Store(id='filter-value'),
    ################################################### Fin para almacenar el df que sera filtado por los dropdowns
])

#############################################################################################################################################
#Estructura principal de la pagina
#############################################################################################################################################
