import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from layout.layout import layout, navbar
from callbacks.callbacks import update_output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.layout = layout

app.callback(Output('map-container', 'style'),
             Output('upload-container', 'style'),
             Output('map-scatter', 'figure'),
             Output('Dropdown_1', 'children'),
             Input('upload-csv', 'contents'),
             State('upload-csv', 'filename'))(update_output)

if __name__ == '__main__':
    app.run_server(debug=True)
