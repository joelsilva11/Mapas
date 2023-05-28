import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output, State
import base64
import io

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
mapbox_access_token = 'pk.eyJ1Ijoiam1zczExIiwiYSI6ImNsN3RsbHpldDEwNDIzdm1rMG1qZWx6cmUifQ.svDPURTTxi1aHuHpzPU8sQ'

app.layout = html.Div([
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Arrastre y suelte o ',
                html.A('Seleccione Archivos')
            ]),
            style={
                'width': '99%',
                'height': '97vh',
                'display': 'flex',  # Esto permite utilizar las propiedades flexbox para centrar el contenido
                'justify-content': 'center',  # Centra el contenido horizontalmente
                'align-items': 'center',  # Centra el contenido verticalmente
                'lineHeight': '60px',
                'borderWidth': '2px',
                'borderStyle': 'dashed',
                'borderRadius': '20px',
                'textAlign': 'center',
                'margin': '10px'
            }
        ),
    ], id='upload-container'),
    html.Div([
        dbc.Spinner(dcc.Graph(id='output-data-upload', style={'height': '98vh'})),
    ], id='map-container', style={'display': 'none'}),
])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    return df


@app.callback(Output('map-container', 'style'),
              Output('upload-container', 'style'),
              Output('output-data-upload', 'figure'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(contents, filename):
    if contents is None:
        return {'display': 'none'}, {'display': 'block'}, dash.no_update

    df = parse_contents(contents, filename)
    fig = go.Figure(go.Scattermapbox(
        lat=df["Latitud"],  # Ajustar según tus datos
        lon=df["Longitud"],  # Ajustar según tus datos
        mode='markers',
        marker=go.scattermapbox.Marker(size=9)
    ))

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            #bearing=90, #angulo de rotacion del mapa
            center=dict(
                lat=df['Latitud'].mean(),
                lon=df['Longitud'].mean()
            ),
            pitch=0,
            zoom=3,
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
    )

    return {'display': 'block'}, {'display': 'none'}, fig

if __name__ == '__main__':
    app.run_server(debug=True)
