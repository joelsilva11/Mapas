import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import numpy as np

# Diccionario con los estilos de los mapas
token = 'pk.eyJ1Ijoiam1zczExIiwiYSI6ImNsN3RsbHpldDEwNDIzdm1rMG1qZWx6cmUifQ.svDPURTTxi1aHuHpzPU8sQ'



# Puntos (latitud y longitud) 
lats = [37.7749 + i*0.01 for i in range(10)]
lons = [-122.4194 + i*0.01 for i in range(10)]
ids = list(range(1, 11))

# Inicializando la aplicación
app = dash.Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    dcc.Graph(id='map'),
    dcc.Slider(
        id='slider',
        min=1,
        max=10,
        step=1,
        value=1,  # Ajusta el valor por defecto a un solo número
        marks={i: f'{i}' for i in range(1, 11)},
        included=True,
        updatemode='drag',
    )
])

@app.callback(
    Output('map', 'figure'),
    [Input('slider', 'value')]
)
def update_map(slider_value):

    # Filtrar los puntos basados en el valor del slider
    filtered_lats = [lat for lat, id in zip(lats, ids) if id <= slider_value]
    filtered_lons = [lon for lon, id in zip(lons, ids) if id <= slider_value]

    # Crea el objeto figura
    fig = go.Figure()

    # le agrega un trace
    fig.add_trace(
        go.Scattermapbox(
            lat=filtered_lats,
            lon=filtered_lons,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=14,
                color='red'
            ),
            text=[f'Punto {id}' for id in ids if id == slider_value],
            name='Puntos',
        )
    )

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=token,
            bearing=0,
            center=dict(
                lat=37.7749,
                lon=-122.4194
            ),
            pitch=0,
            zoom=10,
            style='light',  
            uirevision='constant'  # Mantener el estado del zoom/paneo entre actualizaciones
        ),
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)



