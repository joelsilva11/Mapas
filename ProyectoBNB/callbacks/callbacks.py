import os
os.environ['USE_PYGEOS'] = '0'
import dash
import base64
import io
import pandas as pd
import geopandas as gpd
import plotly.express as px
from dash import dcc, html
from layout.layout import create_dropdown

token = 'pk.eyJ1Ijoiam1zczExIiwiYSI6ImNsN3RsbHpldDEwNDIzdm1rMG1qZWx6cmUifQ.svDPURTTxi1aHuHpzPU8sQ'

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
                    'width': '100%'
                }
            ),create_dropdown(df,'TipoAgencia')
        else:
            return df,dash.no_update
    else:
        return dash.no_update, dash.no_update
