import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
from dash import Dash, html, dcc
import pandas as pd
import dash
import folium
from folium.plugins import HeatMap
import numpy as np
from branca.colormap import linear

import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import folium
import pandas as pd
import dash_leaflet as dl
import random


# Generar puntos aleatorios con valores en otra columna
random_points = []
for _ in range(100):
    lat = random.uniform(51.5, 51.6)
    lon = random.uniform(-0.15, -0.1)
    valor = random.randint(1, 10)
    random_points.append((lat, lon, valor))

# Crear el dataframe a partir de los puntos aleatorios
df = pd.DataFrame(random_points, columns=['Latitud', 'Longitud', 'Valor'])

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Mapa con Puntos y Filtro'),
    dcc.Slider(
        id='slider',
        min=1,
        max=10,
        step=1,
        value=5
    ),
    dl.Map(
        [
            dl.TileLayer(
                'https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png',
            attribution='Map data &copy; Google Maps'),
            dl.MarkerClusterGroup(
                id='marker-cluster',
                children=[
                    dl.Marker(
                        position=(row['Latitud'], row['Longitud']),
                        children=[
                            dl.Tooltip(row['Valor']),
                            dl.Popup(f'Latitud: {row["Latitud"]}, Longitud: {row["Longitud"]}, Valor: {row["Valor"]}')
                        ]
                    )
                    for _, row in df.iterrows()
                ]
            )
        ],
        id='map',
        center=(51.5074, -0.1278),
        zoom=12,
        style={'width': '1000px', 'height': '500px'},

    )
])

@app.callback(
    Output('marker-cluster', 'children'),
    [Input('slider', 'value')]
)
def update_map_markers(slider_value):
    filtered_markers = [
        dl.Marker(
            position=(row['Latitud'], row['Longitud']),
            children=[
                dl.Tooltip(row['Valor']),
                dl.Popup(f'Latitud: {row["Latitud"]}, Longitud: {row["Longitud"]}, Valor: {row["Valor"]}')
            ]
        )
        for _, row in df.iterrows()
        if row['Valor'] <= slider_value
    ]
    return filtered_markers

if __name__ == '__main__':
    app.run_server(debug=True)




