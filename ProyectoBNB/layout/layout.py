from dash import dcc, html
import dash_bootstrap_components as dbc

PLOTLY_LOGO = "https://raw.githubusercontent.com/joelsilva11/Mapas/main/logo-blanco.png"

navbar = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(html.Img(src=PLOTLY_LOGO, height="60px"),width=1),
                dbc.Col(dbc.NavbarBrand("VISUALIZACIÓN DE MAPAS DE CALOR CON CONTORNOS DE DENSIDAD", className="ms-2",style={'font-size': '36px'}), width=8),
                dbc.Col(
                    dcc.Upload(
                        id='upload-data', #este es el id del objeto que actualiza el mapa
                        children=html.Div([
                            'Arrastra y suelta o ',
                            html.A('selecciona archivos')
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
                        multiple=False # Solo permite un archivo a la vez
                    ),
                    align="center"
                ),
            ],
            align="center",
            style={"margin": "0", "width": "100%"},
        ),
    ],
    color="dark",
    dark=True,
)

def create_dropdown(df,selected_column):
    unique_values = df[selected_column].dropna().unique()
    unique_values = sorted(unique_values, key=str)  # Ordenar los valores
    return html.Div(children=[
            html.Label('Tipo de Agencia'),
            dcc.Dropdown(options=[{'label': str(i), 'value': str(i)} for i in unique_values],multi=True,style={
        'backgroundColor': '#333',
        'color': '#fff','width': '100%'
    }),], style={'width': '100%','padding': 5,'backgroundColor': '#333'})


#Estructura principal de la pagina
layout = html.Div([
    navbar,
    html.Div([
        html.Div(id='output-data-upload', style={'padding': 5, 'flex': 8.5}),
        html.Div(id='Dropdown1', style={'padding': 5, 'flex': 1.5}),
    ], style={'display': 'flex', 'flex-direction': 'row'}),
])
