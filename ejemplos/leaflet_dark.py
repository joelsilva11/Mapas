import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import random
import pandas as pd

# Generar puntos aleatorios con valores en otra columna
random_points = []
for _ in range(100):
    lat = random.uniform(51.5, 51.6)
    lon = random.uniform(-0.15, -0.1)
    valor = random.randint(1, 10)
    random_points.append((lat, lon, valor))

# Crear el dataframe a partir de los puntos aleatorios
df = pd.DataFrame(random_points, columns=['Latitud', 'Longitud', 'Valor'])

# Create app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])  # Aplica el tema Darkly

app.layout = html.Div([
    html.H1('Mapa con Puntos y Tiles'),
    dcc.Slider(
        id='slider',
        min=1,
        max=10,
        step=1,
        value=5
    ),
    dl.Map([
        dl.LayersControl(
            [
                dl.BaseLayer(
                    dl.TileLayer(
                        url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                    ),
                    name='OpenStreetMaps',
                    checked=True
                ),
                dl.BaseLayer(
                    dl.TileLayer(
                        url='http://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png',
                        attribution='&copy; <a>Google Satellite</a>'
                    ),
                    name='GoogleSatellite',
                    
                )
            ],
            collapsed=True
        ),
        dl.LayerGroup(
            id='marker-group',
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
    ], style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"})
])

@app.callback(
    Output('marker-group', 'children'),
    Input('slider', 'value')
)
def update_markers( slider_value):
    markers = [
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
    return markers

if __name__ == '__main__':
    app.run_server(debug=True)
