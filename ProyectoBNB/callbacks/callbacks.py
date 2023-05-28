import os
os.environ['USE_PYGEOS'] = '0'
import dash
import base64
import io
import pandas as pd
import geopandas as gpd
#import plotly.express as px
import plotly.graph_objects as go
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
    '''Si no se carga el csv el callback retorna:
    Un contenedor del mapa escondido para css no existe
    Un contenedor del upload bloqueado y se muestra hasta que se cargue con existo el csv
    No actualiza el mapa porque no hay puntos evitando errores
    tampoco actualiza el contenedor del dropdown 
    '''
    if contents is None:
        return {'display': 'none'}, {'display': 'block'}, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    df = parse_contents(contents, filename)

    if isinstance(df, pd.DataFrame):
        gdf = toGeojson(df, 'Latitud', 'Longitud')
        fig = go.Figure(go.Scattermapbox(
            #gdf,
            lat=gdf.geometry.y,
            lon=gdf.geometry.x,
            mode='markers',
            marker=go.scattermapbox.Marker(size=9),
            #zoom=11,
            #center={'lat': gdf.geometry.y.mean(), 'lon': gdf.geometry.x.mean()},
            #mapbox_style='carto-positron',
            #height=850,
            #hover_data=['Nombre', 'Direccion', 'Clase']
        ))

        fig.update_layout(
            autosize=True,
            hovermode='closest',
            margin=dict(l=0, r=0, t=0, b=0),
            mapbox=dict(
                accesstoken = token,
                style='dark',
                center={'lat': gdf.geometry.y.mean(), 'lon': gdf.geometry.x.mean()},
                zoom = 12
            ),
            
        )
        dp1 = create_dropdown(df,'TipoAgencia','Tipo Agencia')
        dp2 = create_dropdown(df,'Banco','Bancos')
        dp3 = create_dropdown(df,'Clase','Tipo Punto')
        dp4 = create_dropdown(df,'TipoCentroMedico','Tipo Centro Médico')
        dp5 = create_dropdown(df,'TipoHotel','Tipo Hospedaje')
        return {'display': 'block'}, {'display': 'none'}, fig, dp1, dp2, dp3, dp4, dp5
    else:
        return  {'display': 'none'}, {'display': 'block'}, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
