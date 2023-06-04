import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output, State
import base64
import io

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([
    html.Div("Cargar Archivo CSV", 
             style={
                 'textAlign': 'center', 
                 'margin': '20px', 
                 'fontSize': 30
                 }
        ),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Arrastra y suelta o ',
            html.A('selecciona archivos')
        ]),
        style={
            'width': '100%',
            'height': '100px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False # Solo permite un archivo a la vez
    ),
    html.Div(id='output-data-upload'),
])

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        else:
            return html.Div([
                'Archivo no soportado: {}'.format(filename)
            ])
    except Exception as e:
        print(e)
        return html.Div([
            'Hubo un error al procesar este archivo.'
        ])

    if 'Latitud' not in df.columns or 'Longitud' not in df.columns:
        return html.Div([
            'El archivo no contiene las columnas necesarias: Latitud y Longitud.'
        ])

    return df

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
        
def update_output(contents, filename):
    if contents:
        df = parse_contents(contents, filename)
        if isinstance(df, pd.DataFrame):
            return html.Div([
                html.Div(
                    dbc.Table.from_dataframe(
                        df.head(5), 
                        striped=True, 
                        bordered=True,
                        dark=True, 
                        hover=True
                    ),
                    style={
                        'overflowX': 'auto'
                    }
                )
            ], 
            style={
                'width': '100%', 
                'margin': 'auto'
            })
        else:
            return df

if __name__ == '__main__':
    app.run_server(debug=True)
