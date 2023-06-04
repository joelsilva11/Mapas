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

def toGeojson(df, latitud, longitud):
    return gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[longitud], df[latitud], crs="EPSG:4326"))

# Cargar los datos geoespaciales
# datos = gpd.read_file('ruta_al_archivo.geojson')

path = 'C:/Users/joels/altitudesolutions.org/AS - Clientes/57 BNB/2. Datos/POI/PuntosDeInteresCBB2.csv'
df = pd.read_csv(path)

data = toGeojson(df, 'Latitud', 'Longitud')


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
    dcc.Graph(id='density-map')
])


# Definir el callback para generar el mapa de calor con contornos de densidad
@app.callback(
    dash.dependencies.Output('density-map', 'figure'),
    [dash.dependencies.Input('density-slider', 'value')]
)
def update_density_map(weight):
    # Filtrar los datos según el peso seleccionado
    filtered_data = data[data['Peso'] >= weight]

    # Obtener los límites del mapa
    lat_min, lat_max = filtered_data['Latitud'].min(), filtered_data['Latitud'].max()
    lon_min, lon_max = filtered_data['Longitud'].min(), filtered_data['Longitud'].max()

    # Calcular el tamaño del radio en función del nivel de zoom
    zoom = 12  # Nivel de zoom inicial
    radius_scale = 100 / (2 ** zoom)  # Escala del radio

    # Generar el mapa de calor con contornos de densidad
    fig = px.density_mapbox(
        filtered_data,
        lat='Latitud',
        lon='Longitud',
        z='Peso',
        radius=data['Peso']+10,
        zoom=zoom,
        center={'lat': filtered_data['Latitud'].mean(), 'lon': filtered_data['Longitud'].mean()},
        mapbox_style='carto-positron',
        opacity=0.7,
        height=700,
        hover_data=['Nombre', 'Direccion', 'Clase']
    )

    # Actualizar la configuración del layout
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        coloraxis_colorbar=dict(title='Peso'),
    )

    return fig


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
