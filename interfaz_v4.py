import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output, State
import base64
import io
import plotly.express as px

#imagen logo Altitude
PLOTLY_LOGO = "https://raw.githubusercontent.com/joelsilva11/Mapas/main/logo-blanco.png"
#Token para usar mapox
token = 'pk.eyJ1Ijoiam1zczExIiwiYSI6ImNsN3RsbHpldDEwNDIzdm1rMG1qZWx6cmUifQ.svDPURTTxi1aHuHpzPU8sQ'

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


#################################################################################################################################################################
#Barra de titulo y carga de archivo csv
#################################################################################################################################################################
navbar = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(html.Img(src=PLOTLY_LOGO, height="60px"),width=1),
                dbc.Col(dbc.NavbarBrand("VISUALIZACIÓN DE MAPAS DE CALOR CON CONTORNOS DE DENSIDAD", className="ms-2",style={'font-size': '36px'}), width=8),
                dbc.Col(
                    dcc.Upload(
                        id='upload-data',
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
                    #width=3,
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
#################################################################################################################################################################
#Fin Barra de titulo y carga de archivo csv
#################################################################################################################################################################













# Diseño de la aplicación
app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
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
        multiple=False  # Permite solo un archivo a la vez
    ),
    dcc.Graph(id='map-graph')
])

# Callback para actualizar el mapa cuando se cargue un archivo
@app.callback(
    Output('map-graph', 'figure'),
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
)
def update_map(contents, filename):
    if contents is not None:
        # Cargar el archivo CSV
        df = pd.read_csv(filename)

        # Verificar si el archivo contiene las columnas de latitud y longitud
        if 'lat' in df.columns and 'lon' in df.columns:
            # Crear un mapa vacío
            fig = go.Figure(go.Scattermapbox())

            # Actualizar el mapa con los puntos del archivo CSV
            fig.add_trace(go.Scattermapbox(
                lat=df['lat'],
                lon=df['lon'],
                mode='markers',
                marker=dict(size=10, color='blue')
            ))

            # Configurar el diseño del mapa
            fig.update_layout(
                mapbox=dict(
                    style='open-street-map',
                    center=dict(lat=0, lon=0),
                    zoom=1
                ),
                margin=dict(l=0, r=0, t=0, b=0)
            )

            return fig

    # Si no se ha cargado un archivo o el archivo no contiene las columnas adecuadas, mostrar un mapa vacío
    return go.Figure(go.Scattermapbox())

if __name__ == '__main__':
    app.run_server(debug=True)
