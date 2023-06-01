import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from layout.layout import layout
from callbacks.callbacks import load_data_and_dropdowns, generate_map, generate_gson, filter_df

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
    Output('Dropdown_container_6', 'children'),
    Output('kde-button_container', 'style'),
    Input('upload-csv', 'contents'),
    State('upload-csv', 'filename')
)(load_data_and_dropdowns)

#este callback se ejecuta una sola vez para crear el mapa
app.callback(
    [
        Output('map-container', 'style'),
        Output('upload-container', 'style'),
        Output('map-scatter', 'figure'),
        Output('map-scatter', 'config')
    ],
    [
        Input('filter-value', 'data'),
        State('map-scatter', 'figure'),
        State('map-scatter', 'config'),
        Input('kde-output', 'data')
    ]
)(generate_map)

#este callback se ejecuta cuando se el usuario quiere generar un KDE
app.callback(
    Output('kde-output', 'data'),
    [Input('kde-button', 'n_clicks')],
    State('filter-value', 'data')
)(generate_gson)

#este callback se ejecuta para modificar el dataframe
app.callback(
        Output('filter-value', 'data'),
    [
        Input('Dropdown_1', 'value'),
        Input('Dropdown_2', 'value'),
        Input('Dropdown_3', 'value'),
        Input('Dropdown_4', 'value'),
        Input('Dropdown_5', 'value'),
        Input('Dropdown_6', 'value'),
        State('intermediate-value', 'data')
    ]
)(filter_df)




if __name__ == '__main__':
    app.run_server(debug=True)
