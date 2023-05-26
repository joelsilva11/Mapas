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

def toGeojson(df, latitud, longitud):
    return gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[longitud], df[latitud], crs="EPSG:4326"))

# Cargar los datos geoespaciales
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
    html.Div([
        html.Label('Mapa de calor'),
        html.Iframe(id='folium-map', width='100%', height=500)
    ])
])


# Definir el callback para generar el mapa de calor con contornos de densidad
@app.callback(
    dash.dependencies.Output('folium-map', 'srcDoc'),
    [dash.dependencies.Input('density-slider', 'value')]
)
def update_density_map(weight):
    # Filtrar los datos según el peso seleccionado
    filtered_data = data[data['Peso'] >= weight]

    # Crear el mapa de folium
    m = folium.Map(location=[filtered_data['Latitud'].mean(), filtered_data['Longitud'].mean()], zoom_start=12)

    # Obtener los valores únicos de la columna "Radio"
    unique_radios = filtered_data['Peso'].unique()

    # Crear un colormap para asignar colores a los diferentes radios
    colormap = linear.YlOrRd_09.scale(0, len(unique_radios) - 1)

    # Iterar sobre los valores únicos de la columna "Radio"
    for radio in unique_radios:
        # Filtrar los datos por el radio actual
        filtered_by_radio = filtered_data[filtered_data['Peso'] == radio]

        # Crear el objeto HeatMap para el radio actual
        heatmap = HeatMap(
            data=filtered_by_radio[['Latitud', 'Longitud', 'Peso']].values,
            radius=int(radio),
            min_opacity=0.7,
            max_val=filtered_by_radio['Peso'].max(),
            gradient=colormap.to_step(6).to_dict(),
            blur=15,
            overlay=True,
            control=True
        )

        # Añadir el HeatMap al mapa de folium
        heatmap.add_to(m)

    # Guardar el mapa de folium en un archivo HTML temporal
    temp_file = 'temp_map.html'
    m.save(temp_file)

    # Leer el archivo HTML temporal y retornarlo como fuente para el IFrame
    with open(temp_file, 'r') as f:
        src_doc = f.read()

    # Eliminar el archivo HTML temporal
    os.remove(temp_file)

    return src_doc


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
