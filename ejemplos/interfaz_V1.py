import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
import base64
import io

mapbox_access_token = 'pk.eyJ1Ijoiam1zczExIiwiYSI6ImNsN3RsbHpldDEwNDIzdm1rMG1qZWx6cmUifQ.svDPURTTxi1aHuHpzPU8sQ' # Asegúrate de usar tu propio token de Mapbox aquí.

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Arrastra y Suelta o ',
            html.A('Selecciona un archivo CSV')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    html.Div(id='content-container')
])

def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        return df
    except Exception as e:
        print(e)
        return None

@app.callback(Output('content-container', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')]
)
def update_content(contents, filename):
    if contents is None:
        return html.Div([
            'No se ha cargado ningún archivo.'
        ])
    else:
        df = parse_contents(contents)
        if df is None:
            return html.Div([
                'No se pudo leer el archivo CSV.'
            ])
        
        fig = go.Figure(go.Scattermapbox(
            lat=df['Latitud'],
            lon=df['Longitud'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=9,
                color='rgb(0,0,255)',
                opacity=0.7
            ),
            hovertext=df[['Nombre', 'Direccion', 'Clase']].astype(str),
        ))

        fig.update_layout(
            mapbox=dict(
                accesstoken=mapbox_access_token,
                style='dark',
                center=dict(
                    lat=df['Latitud'].mean(),
                    lon=df['Longitud'].mean()
                ),
                zoom=11,
            ),
            margin={"r":0,"t":0,"l":0,"b":0},
            height=200
        )
        
        return dcc.Graph(
            id='map-with-csv',
            figure=fig,
            style={'width': '100%'}
        )

if __name__ == '__main__':
    app.run_server(debug=True)





