import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

#token necesario para cargar los tiles de los mapas
mapbox_access_token = 'pk.eyJ1Ijoiam1zczExIiwiYSI6ImNsN3RsbHpldDEwNDIzdm1rMG1qZWx6cmUifQ.svDPURTTxi1aHuHpzPU8sQ'

#opciones para el boton tile layers
mapbox_style_dict = {
    "Light": "light",
    "Dark": "dark",
    "Satellite": "satellite",
    "Satellite Streets": "satellite-streets",
    "Outdoors": "outdoors",
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Graph(id='map', style={'width': '100%', 'height': '800px'}),
    html.Div(
        dbc.DropdownMenu(
            label=html.Img(src='https://raw.githubusercontent.com/joelsilva11/GIS/main/tile_icon.png', style={'height':'25px', 'width':'25px'}),
            children=[
                dbc.DropdownMenuItem(i, id=i) for i in mapbox_style_dict.keys()
            ],
            id="dropdown",
            direction="end",
        ),
        style={'position': 'absolute', 'top': '10px', 'left': '10px', 'z-index': '1'}
    ),
    
])

@app.callback(
    Output('map', 'figure'),
    [Input(i, 'n_clicks') for i in mapbox_style_dict.keys()],
    [State(i, 'children') for i in mapbox_style_dict.keys()]
)
def update_map(*args):
    ctx = dash.callback_context

    if not ctx.triggered:
        style = 'Light'
    else:
        style = ctx.triggered[0]['prop_id'].split('.')[0]
    
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
            margin=dict(l=0, r=0, t=0, b=0),
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
                uirevision='constant',
            ),
        )
    )

if __name__ == '__main__':
    app.run_server(debug=True)
