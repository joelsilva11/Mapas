import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Diccionario con los estilos de los mapas
mapbox_access_token = 'pk.eyJ1Ijoiam1zczExIiwiYSI6ImNsN3RsbHpldDEwNDIzdm1rMG1qZWx6cmUifQ.svDPURTTxi1aHuHpzPU8sQ'
mapbox_style_dict = {
    "Light": "light",
    "Dark": "dark",
    "Satellite": "satellite",
    "Satellite Streets": "satellite-streets",
    "Outdoors": "outdoors",
}

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in mapbox_style_dict.keys()],
        value='Light'
    ),
    dcc.Graph(id='map')
])

@app.callback(
    Output('map', 'figure'),
    [Input('dropdown', 'value')]
)
def update_map(style):
    return go.Figure(
        data=go.Scattermapbox(
            lat=['45.5017'],
            lon=['-73.5673'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=14
            ),
            text=['Montreal'],
        ),
        layout=go.Layout(
            autosize=True,
            hovermode='closest',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=dict(
                    lat=45,
                    lon=-73
                ),
                pitch=0,
                zoom=5,
                style=mapbox_style_dict[style],
                uirevision = 'constant',
            ),
        )
    )

if __name__ == '__main__':
    app.run_server(debug=True)