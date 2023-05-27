import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from layout.layout import layout, navbar
from callbacks.callbacks import update_output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.layout = layout

app.callback(Output('output-data-upload', 'children'),
              Output('Dropdown1', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))(update_output)

if __name__ == '__main__':
    app.run_server(debug=True)
