import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from layout.layout import layout, navbar
from callbacks.callbacks import load_data_and_dropdowns, generate_map

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
#suppress_callback_exceptions=True
app.layout = layout

#este callback se ejecuta las veces que sea necesario hasta que se cargue correctamente el csv
app.callback(
    Output('intermediate-value', 'data'),  # Actualiza el Store en lugar del mapa
    Output('Dropdown_container_1', 'children'),
    Output('Dropdown_container_2', 'children'),
    Output('Dropdown_container_3', 'children'),
    Output('Dropdown_container_4', 'children'),
    Output('Dropdown_container_5', 'children'),
    Input('upload-csv', 'contents'),
    State('upload-csv', 'filename')
)(load_data_and_dropdowns)

#este callback se ejecuta una sola vez para crear el mapa y los filtros
app.callback(
    [Output('map-container', 'style'),
     Output('upload-container', 'style'),
     Output('map-scatter', 'figure'),
     Output('map-scatter', 'config')],
    [Input('Dropdown_1', 'value'),
     Input('intermediate-value', 'data'),
     State('map-scatter', 'figure')]
)(generate_map)

#este callback se ejecuta cuando se filtran datos por medio de los dropdowns


if __name__ == '__main__':
    app.run_server(debug=True)
