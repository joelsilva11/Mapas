import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import numpy as np

# Diccionario con los estilos de los mapas
token = 'pk.eyJ1Ijoiam1zczExIiwiYSI6ImNsN3RsbHpldDEwNDIzdm1rMG1qZWx6cmUifQ.svDPURTTxi1aHuHpzPU8sQ'


# Datos de ejemplo
np.random.seed(0)  # Para la reproducibilidad
lats_rojos = 45.5 + np.random.rand(10) * 0.01
lons_rojos = -73.6 + np.random.rand(10) * 0.01
lats_azules = 45.5 + np.random.rand(10) * 0.01
lons_azules = -73.6 + np.random.rand(10) * 0.01

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Capa roja', 'value': 'roja'},
            {'label': 'Capa azul', 'value': 'azul'}
        ],
        value=['roja', 'azul'],
        multi=True,
    ),
    dcc.Graph(id='map'),
])

@app.callback(
    Output('map', 'figure'),
    [Input('dropdown', 'value')]
)
def update_map(value):

    fig = go.Figure()

    # Añade un trazo invisible al mapa.
    fig.add_trace(go.Scattermapbox(
        lat=[45.5],  # Estas coordenadas pueden ser cualquier punto dentro del rango visible del mapa.
        lon=[-73.6],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=0,  # El tamaño 0 hace el marcador invisible.
        ),
        hoverinfo='none'  # Esto evita que aparezca un tooltip cuando el usuario pasa el cursor sobre el marcador.
    ))

    if value:  # Si hay alguna capa seleccionada
        if 'roja' in value:
            fig.add_trace(go.Scattermapbox(
                lat=lats_rojos,
                lon=lons_rojos,
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=14,
                    color='red'
                ),
                text=['Punto rojo'] * len(lats_rojos),
                name='Capa roja',
            ))

        if 'azul' in value:
            fig.add_trace(go.Scattermapbox(
                lat=lats_azules,
                lon=lons_azules,
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=14,
                    color='blue'
                ),
                text=['Punto azul'] * len(lats_azules),
                name='Capa azul',
            ))

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=token,
            bearing=0,
            center=dict(
                lat=45.5,
                lon=-73.6
            ),
            pitch=0,
            zoom=10,
            style='light',  # o cualquier otro estilo de Mapbox que prefieras
            uirevision='constant'
        ),
    )

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)

