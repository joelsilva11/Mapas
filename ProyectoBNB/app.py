import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from layout.layout import layout
from callbacks.callbacks import load_data_and_dropdowns, generate_map, generate_gson, filter_df,show_inputs

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
    Output('offcanvas-button-container', 'style'),
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

inputs = [Input(f"input-{x}-{y}", "value") for x in ['peso', 'radio'] for y in ['bnb', 'ob', 'at', 'sm', 'cm', 'ht', 'ot']]
states = [State(f"input-{x}-{y}", "value") for x in ['peso', 'radio'] for y in ['bnb', 'ob', 'at', 'sm', 'cm', 'ht', 'ot']]
inputs.append(Input("open-offcanvas", "n_clicks"))
states.append(State('intermediate-value', 'data'))

#este callback se ejecuta para desplegar el off-canvas
app.callback(
    [
        Output("offcanvas", "is_open"),
        Output('input-peso-bnb', 'value'),
        Output('input-radio-bnb', 'value'),
        Output('input-peso-ob', 'value'),
        Output('input-radio-ob', 'value'),
        Output('input-peso-at', 'value'),
        Output('input-radio-at', 'value'),
        Output('input-peso-sm', 'value'),
        Output('input-radio-sm', 'value'),
        Output('input-peso-cm', 'value'),
        Output('input-radio-cm', 'value'),
        Output('input-peso-ht', 'value'),
        Output('input-radio-ht', 'value'),
        Output('input-peso-ot', 'value'),
        Output('input-radio-ot', 'value')
    ],
    [ 
        Input("open-offcanvas", "n_clicks"),
        State('input-peso-bnb', 'value'),
        State('input-radio-bnb', 'value'),
        State('input-peso-ob', 'value'),
        State('input-radio-ob', 'value'),
        State('input-peso-at', 'value'),
        State('input-radio-at', 'value'),
        State('input-peso-sm', 'value'),
        State('input-radio-sm', 'value'),
        State('input-peso-cm', 'value'),
        State('input-radio-cm', 'value'),
        State('input-peso-ht', 'value'),
        State('input-radio-ht', 'value'),
        State('input-peso-ot', 'value'),
        State('input-radio-ot', 'value'),
        State('intermediate-value', 'data')
    ]
)(show_inputs)


if __name__ == '__main__':
    app.run_server(debug=True)
