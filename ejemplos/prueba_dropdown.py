import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
from dash import Dash, html, dcc
import pandas as pd
import dash
import plotly.graph_objects as go
from sklearn.neighbors import KernelDensity
import plotly.express as px
import numpy as np
from ipywidgets import HTML

def toGeojson(df, latitud, longitud):
    return gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[longitud], df[latitud], crs="EPSG:4326"))

# Cargar los datos geoespaciales
# datos = gpd.read_file('ruta_al_archivo.geojson')

path = 'C:/Users/joels/altitudesolutions.org/AS - Clientes/57 BNB/2. Datos/POI/PuntosDeInteresCBB2.csv'
df = pd.read_csv(path)

data = toGeojson(df, 'Latitud', 'Longitud')

# Obtener los límites del mapa
lat_min, lat_max = data['Latitud'].min(), data['Latitud'].max()
lon_min, lon_max = data['Longitud'].min(), data['Longitud'].max()

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Definir el layout de la aplicación
app.layout = html.Div([
    html.H1('Visualización de Mapa de Calor con Contornos de Densidad'),
    html.Div([
        html.Label('Peso mínimo'),
        dcc.Slider(
            id='density-slider',
            min=data['Peso'].min(),
            max=data['Peso'].max(),
            step=1,
            value=data['Peso'].min(),
            marks={str(peso): str(peso) for peso in range(data['Peso'].min(), data['Peso'].max() + 1, 10)}
        )
    ], style={'margin': '20px'}),
    html.Div(id='density-map')
])


# Definir el callback para generar el mapa de calor con contornos de densidad
@app.callback(
    dash.dependencies.Output('density-map', 'children'),
    [dash.dependencies.Input('density-slider', 'value')]
)
def update_density_map(weight):
    # Filtrar los datos según el peso seleccionado
    filtered_data = data[data['Peso'] >= weight]

    # Generar el mapa de calor con contornos de densidad
    fig = go.Figure(data=go.Densitymapbox(
        lat=filtered_data['Latitud'],
        lon=filtered_data['Longitud'],
        z=filtered_data['Peso'],
        radius=10,
        colorscale='Viridis',
        colorbar=dict(title='Peso')
    ))

    fig.update_layout(
        mapbox=dict(
            center=dict(lat=data['Latitud'].mean(), lon=data['Longitud'].mean()),
            zoom=12,
            style='carto-positron'
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        height=600,
        width=800
    )

    return dcc.Graph(figure=fig)


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)

