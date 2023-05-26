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

PLOTLY_LOGO = "https://raw.githubusercontent.com/joelsilva11/Mapas/main/logo-blanco.png"
token = 'pk.eyJ1Ijoiam1zczExIiwiYSI6ImNsN3RsbHpldDEwNDIzdm1rMG1qZWx6cmUifQ.svDPURTTxi1aHuHpzPU8sQ'

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

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


app.layout = html.Div([
    navbar,
    html.Div(id='output-data-upload'),
])

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        else:
            return html.Div([
                'Archivo no soportado: {}'.format(filename)
            ])
    except Exception as e:
        print(e)
        return html.Div([
            'Hubo un error al procesar este archivo.'
        ])

    if 'Latitud' not in df.columns or 'Longitud' not in df.columns:
        return html.Div([
            'El archivo no contiene las columnas necesarias: Latitud y Longitud.'
        ])

    return df

def toGeojson(df,latitud,longitud):
    return gpd.GeoDataFrame(df,geometry=gpd.points_from_xy(df[longitud],df[latitud],crs="EPSG:4326"))



@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(contents, filename):
    if contents:
        df = parse_contents(contents, filename)
        if isinstance(df, pd.DataFrame):
            gdf = toGeojson(df, 'Latitud', 'Longitud')
            fig = px.scatter_mapbox(
                gdf,
                lat=gdf.geometry.y,
                lon=gdf.geometry.x,
                #zoom=11,
                center={'lat': gdf.geometry.y.mean(), 'lon': gdf.geometry.x.mean()},
                #mapbox_style='carto-positron',
                height=850,
                hover_data=['Nombre', 'Direccion', 'Clase']
            )
            fig.update_layout(
                autosize=True,
                margin=dict(l=0, r=0, t=0, b=0),
                mapbox=dict(
                    accesstoken = token,
                    style='dark',
                    zoom = 11
                )
            )
            return dcc.Graph(
                figure=fig,
                style={
                    'width': '85%'
                }
            )
        else:
            return df


if __name__ == '__main__':
    app.run_server(debug=True)





