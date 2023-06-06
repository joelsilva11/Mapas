from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_daq as daq

PLOTLY_LOGO = "https://raw.githubusercontent.com/joelsilva11/Mapas/main/logo-blanco.png"


################################################################ Creamos las opciones de los filtros para no hacerlos muy complicado
################################################Opciones clase
opciones_cl = [
    "Agencia",
    "ATM",
    "Centro Comercial",
    "Centro Médico",
    "Hotel",
    "Mercado",
    "Restaurante",
    "Supermercado",
    "Universidad"
]
opciones_clases = [{'label': opcion, 'value': opcion} for opcion in opciones_cl]

################################################Opciones bancos
opciones_bancos = [
    {'label':"Banco Bisa",'value':"Banco Bisa S.A."},
    {'label':"Banco de Crédito de Bolivia",'value':"Banco de Crédito de Bolivia S.A."},
    {'label':"Banco Económico Bolivia",'value':"Banco Económico Bolivia"},
    {'label':"Banco Fie",'value':"Banco Fie S.A."},
    {'label':"Banco Ganadero",'value':"Banco Ganadero S.A."},
    {'label':"Banco Mercantil Santa Cruz",'value':"Banco Mercantil Santa Cruz S.A."},
    {'label':"Banco Unión",'value':"Banco Unión S.A."}
]

################################################Opciones agencias
opciones_ag = [
    "Agencia",
    "Express",
    "Externa",
    "Indefinido",
    "Punto Promocional Fijo",
    "Sucursal",
    "Ventanilla"
]
opciones_agencias = [{'label': opcion, 'value': opcion} for opcion in opciones_ag]

################################################Opciones atm
opciones_atm = [
    {'label': 'Permite depósitos', 'value': 'Si'},
    {'label': 'No Permite depósitos', 'value': 'No'}, 
    ]

################################################Opciones centros médicos
opciones_cm = [
    "Centro de salud",
    "Clínica",
    "Hospital"
]
opciones_ceme = [{'label': opcion, 'value': opcion} for opcion in opciones_cm]

################################################Opciones hoteles
opciones_ht = [
    "ApartHotel",
    "Apartment",
    "Bed and breakfast",
    "Guest house",
    "Holiday home",
    "Homestay",
    "Hostel",
    "Hotel",
    "Inn",
    "Resort"
]
opciones_hoteles = [{'label': opcion, 'value': opcion} for opcion in opciones_ht]
################################################################ fin de las opciones de los filtros para no hacerlos muy complicado


###################################################################crea la barra de titulo
navbar = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(html.Img(src=PLOTLY_LOGO, height="60px"),width=2,style={'padding-left': '75px'}),
                dbc.Col(dbc.NavbarBrand("VISUALIZACIÓN DE MAPAS DE CALOR CON CONTORNOS DE DENSIDAD",style={'font-size': '36px'}), width=7),
                ############################################### Inicio Div que contiene al Boton que ejecuta el KDE
                dbc.Col(
                    html.Div(
                        dbc.Button('Run KDE Analisys', id='kde-button', n_clicks=0, style={'width': '100%','height': '50px'}, color="success"),
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
    color="#333",
    dark=True,
)


###################################################################crea los slicers
def create_slider(Titulo,id_suffix):
    id_peso = f'sl-peso-{id_suffix}'
    id_radio = f'sl-radio-{id_suffix}'
    return html.Div([
                    html.Div([
                        html.H6(Titulo,
                            style={
                                'padding-top':'7px',
                                'flex': '1',
                                'text-align': 'left'
                            }
                        ),
                        ], style={'display': 'flex'}
                    ),
                    
                    dbc.InputGroup(
                        [
                            dbc.Button(
                                "P", 
                                color="primary",
                                style={
                                    'flex': '0.04'
                                    }
                            ),
                            html.Div([
                                html.Div(
                                daq.Slider(
                                    id=id_peso,
                                    min=0,
                                    max=10,
                                    step=1,
                                    marks={i: str(i) for i in range(11)},
                                    value=5,
                                    color='#2A9FD6',
                                    className='my-slider' # parametro para personlizar la longitud maxima del slider con css
                                ),
                                style={
                                    'margin-left': 25,
                                    'margin-right': 25,
                                    }
                                )
                                ],
                                style={
                                    'padding-top': '8px',
                                    'padding-bottom': '25px',
                                    #'backgroundColor': '#092533',
                                    'backgroundColor': 'rgba(42, 159, 214, 0.15)',
                                    'borderRadius': '5px',
                                    'flex': '1',
                                },
                            ),
                        ],
                        style={
                            'display': 'flex',
                        }
                    ),
                    dbc.InputGroup(
                        [
                            dbc.Button(
                                "R", 
                                #color="#6A72AC",
                                style={
                                    'flex': '0.04',
                                    'backgroundColor':"#2DB89E",
                                    'borderColor':"#2DB89E"
                                    }
                            ),
                            html.Div([
                                dcc.Slider(
                                    id=id_radio,
                                    min=0,
                                    max=500,
                                    step=50,
                                    value=200, # Valor inicial del slider
                                    marks=None,
                                    #marks={i: str(i) for i in range(0, 501, 50)}, # Marca los puntos en el slider en incrementos de 50
                                    tooltip={"placement": "bottom","always_visible": True},
                                    className="dcc-slider-custom"
                                )
                                ],
                                style={
                                    'padding-top': '8px',
                                    #'backgroundColor': '#273B00',
                                    'backgroundColor': 'rgba(45, 184, 158, 0.2)',
                                    'flex': '1',
                                    'borderRadius': '5px',
                                },
                            ),
                        ],
                        style={
                            'display': 'flex',    
                        }
                    )
                ],
            style={
                'margin-bottom': 7,
                'backgroundColor': '#333',
                'borderRadius': '5px',
                'padding-bottom': '10px',
                'padding-left': '10px',
                'padding-right': '10px',
            },
            )


###################################################################crea los dropdowns personalizados
def create_dropdown_p(id_suffix, dp_options,title_dp = 'Title'): 
    # Genera los IDs de los componentes con el sufijo proporcionado
    input_id = f'dp-input-{id_suffix}'
    button_id = f'dp-button-{id_suffix}'
    checklist_id = f'checklist-{id_suffix}'
    all_checklist_id = f'all-checklist-{id_suffix}'
    container_id = f'checklist_container-{id_suffix}'


    # Crea y devuelve el componente
    return html.Div(
        [
            html.H6(
                title_dp, 
                style={
                    'padding-left': '10px',
                    'padding-top':'7px',
                    'margin-bottom': '5px'
                }
            ),
            dbc.InputGroup(
                [
                    dbc.Input(id=input_id, value="", readonly=True,),
                    dbc.Button("▼", id=button_id, color="primary")
                ],
                style={
                    'padding-left': '10px',
                    'padding-right': '10px'
                }
            ),
            html.Div(
                [
                html.Div(
                    [   
                        dbc.Checklist(options=["All"], value=[], id=all_checklist_id, style={'padding-left': 8}),
                        dbc.Checklist(options=dp_options, value=[], id=checklist_id, style={'padding-left': 16}),
                    ],
                    id=container_id,
                    style={
                        'display':'none',
                        'backgroundColor': 'rgba(0, 0, 0, 0.92)', 
                        'borderRadius': '5px',
                        'overflow': 'auto',
                        'maxHeight': '180px', 
                        'position': 'absolute', 
                        'z-index': '9999',
                        'width': '100%',
                    }
                ),
                ],
                style={
                    'position': 'relative',
                    'padding-left': '10px',
                    'margin-right': '20px'
                }
            ),
        ],
        style={
            
            'backgroundColor': '#333',
            'borderRadius': '5px',
            'height': '8.5vh',
        }
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

#funcion para crear los switches para seleccion del banco bnb
radioitems = html.Div(
    [
        html.H6(
                'Puntos BNB', 
                style={
                    'padding-left': '10px',
                    'padding-top':'7px',
                    'margin-bottom': '20px'
                }
            ),
        dbc.Checklist(
            options=[
                {"label": "Agencias", "value": 'Agencia'},
                {"label": "ATMs", "value": 'ATM'}
            ],
            value=['Agencia', 'ATM'],# inicia los valores en ON
            id="switches-input",
            switch=True,
        style={
                'padding-left': '10px',
                'margin-bottom': '5px'
        }
        ),
    ]
)




#############################################################################################################################################
#Estructura principal de la pagina
#############################################################################################################################################

layout = html.Div([
    ################################################### Inicio Barra de título
    navbar,
    ################################################### Fin Barra de título


    ################################################################################ Inicio Div pantalla principal
    html.Div([
        ############################################### Inicio Div que contiene los dropdowns personalizados
        html.Div([
            ################################################### Dropdown1
            html.Div(create_dropdown_p('1',opciones_clases,'Tipos de Puntos'),style={'padding-bottom': 7}),

            ################################################### Dropdown2
            html.Div(create_dropdown_p('2',opciones_bancos,'Bancos'),style={'padding-bottom': 7}),

            ################################################### Dropdown3
            html.Div(create_dropdown_p('3',opciones_agencias,'Tipos de Agencias'),style={'padding-bottom': 7}),

            ################################################### Dropdown4
            html.Div(create_dropdown_p('4',opciones_atm,'ATM con depósito'),style={'padding-bottom': 7}),

            ################################################### Dropdown5
            html.Div(create_dropdown_p('5',opciones_ceme,'Tipos de Centros Médicos'),style={'padding-bottom': 7}),

            ################################################### Dropdown6
            html.Div(create_dropdown_p('6',opciones_hoteles,'Tipos de Hospedaje'),style={'padding-bottom': 7}),

            ################################################### Selector Agencias y ATMs BNB
            html.Div(radioitems,
            style={
                'margin-bottom': '7px',
                'backgroundColor': '#333',
                'borderRadius': '5px',
                'height': '12vh',
            }
            ),

            ################################################### Indicador de numero de puntos
            html.Div(dbc.Card(
            [
                dbc.CardHeader(html.H6("Número de puntos")),
                dbc.CardBody(
                    [
                        html.H1("",id="num_puntos_id", className="card-title text-center", style={'font-size': '110px'}),
                    ]
                ),
                #dbc.CardFooter("This is the footer"),
            ],
            style={"width": "18rem",'backgroundColor': '#333'},
            ),
            style={
                #'margin-bottom': '7px',
                'backgroundColor': '#333',
                'borderRadius': '5px',
                #'height': '22vh',
            }
            )
        ],
        style={
            'padding-top': 7, 
            'flex': 1.5,
            'height': '91vh',
            #'backgroundColor': '#335'
        },
        ),
        ############################################### Fin Div que contiene los dropdowns personalizados

        ############################################### Inicio Div que contiene el upload y el mapa a la vez
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
                        'width': '98.6%',
                        'height': '89vh',
                        'display': 'flex',  # Esto permite utilizar las propiedades flexbox para centrar el contenido
                        'justify-content': 'center',  # Centra el contenido horizontalmente
                        'align-items': 'center',  # Centra el contenido verticalmente
                        'lineHeight': '60px',
                        'borderWidth': '2px',
                        'borderStyle': 'dashed',
                        'borderRadius': '20px',
                        'textAlign': 'center',
                        'margin': '8px',
                    }
                ),
                ############################################### Fin objeto Upload
            ], 
            id='upload-container', #Id contenedor del Upload
            style={'height': '100vh'}
            ),
            ############################################### Fin Div que contiene upload

            ############################################### Inicio Div que contiene Grafico mapa
            html.Div(
                dcc.Graph(
                    id='map-scatter',
                    style={'height': '91vh'}
                ),
                id='map-container',
                style={
                    'display': 'none'
                }
            ),
            ############################################### Fin Div que contiene Grafico mapa
        ],
        style={
            #'padding': 7, 
            'flex': 7,
            'margin': 7,
            'backgroundColor': '#333',
            'borderRadius': '5px',
            #'height': '91vh'
        }
        ),
        ############################################### Fin Div que contiene upload y mapa a la vez

        ############################################### Inicio Div que contiene los sliders
        html.Div([
            ############################################### Slider 1
            create_slider('Banco BNB','1'),
            ############################################### Slider 2
            create_slider('Otros Bancos','2'),
            ############################################### Slider 3
            create_slider('ATMs','3'),
            ############################################### Slider 4
            create_slider('Supermercados','4'),
            ############################################### Slider 5
            create_slider('Centros Médicos','5'),
            ############################################### Slider 6
            create_slider('Hotels','6'),

            ############################################### Inicio Div que contiene al Boton que oculta el canvas
            html.Div([
                dbc.Button(
                    'Editar parámetros', 
                    id='open-offcanvas', 
                    n_clicks=0, 
                    style={
                        'width': '100%',
                        #'height': '7vh',
                    }, 
                    color='primary'
                ),
            ],
            style={
                'margin-bottom': 7
            },
            ),
            ############################################### Fin Div que contiene al Boton que oculta el canvas
        ],
        id='sliders_contain',
        style={
                'flex-direction': 'column',
                'display': 'block',
                'padding-top': 7,
                #'padding-right': 5,
                'padding-bottom': 5, 
                'flex': 2
        }
        ),
        ############################################### Fin Div que contiene los sliders
    ], 
    style={
        'display': 'flex', 
        'flex-direction': 'row'
    }
    ),
    ################################################################################ Inicio Div pantalla principal


    ################################################################################ Inicio de la ventana desplegable
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
    ################################################################################ Fin de la ventana desplegable


    ################################################### Inicio Stores inputs
    dcc.Store(id='store-inputs'),
    ################################################### Fin Stores inputs

    
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
