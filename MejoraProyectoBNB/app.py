import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL
from layout.layout import layout, opciones_clases,opciones_bancos,opciones_agencias,opciones_atm,opciones_ceme,opciones_hoteles
from callbacks.callbacks import load_data_and_dropdowns, generate_map, generate_gson, filter_df,toggle_offcanvas,export_dataframe

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
#suppress_callback_exceptions=True
app.layout = layout


######################################################################Caso especial para los dropdowns personalizados
def create_callbacks(id_suffix, options):
    # Genera los IDs de los componentes con el sufijo proporcionado
    input_id = f'dp-input-{id_suffix}'
    checklist_id = f'checklist-{id_suffix}'
    all_checklist_id = f'all-checklist-{id_suffix}'

    @app.callback(
        Output(checklist_id, "value"),
        Output(all_checklist_id, "value"),
        Input(checklist_id, "value"),
        Input(all_checklist_id, "value"),
    )
    def sync_checklists(item_selected, all_selected):
        ctx = dash.callback_context
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if input_id == checklist_id:
            all_selected = ["All"] if set(item_selected) == set([option['value'] for option in options]) else []
        else:
            item_selected = [option['value'] for option in options] if all_selected else []

        return item_selected, all_selected

    @app.callback(
        Output(input_id, "value"),
        [Input(checklist_id, "value")],
    )
    def update_input(values):
        labels = [option["value"] for option in options if option["value"] in values]
        return ", ".join(labels)
######################################################################Caso especial para los dropdowns personalizados


#este callback se ejecuta las veces que sea necesario hasta que se cargue correctamente el csv
app.callback(
    Output('intermediate-value', 'data'),  # Actualiza el Store en lugar del mapa
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
        Input('checklist-1', 'value'),
        Input('checklist-2', 'value'),
        Input('checklist-3', 'value'),
        Input('checklist-4', 'value'),
        Input('checklist-5', 'value'),
        Input('checklist-6', 'value'),
        Input('store-transformed', 'data')
    ]
)(filter_df)

#este callback se ejecuta para desplegar el off-canvas
app.callback(
    [
        Output("offcanvas", "is_open"),
        Output({'type': 'input', 'index': ALL}, 'value'),
        Output('store-inputs', 'data')
    ],
    [
        Input("open-offcanvas", "n_clicks"),
        Input({'type': 'input', 'index': ALL}, 'n_blur'),
        Input('intermediate-value', 'data')
    ],
    [
        State("offcanvas", "is_open"),
        State({'type': 'input', 'index': ALL}, 'value'),
        State('store-inputs', 'data'),
    ]
)(toggle_offcanvas)

#este callback transforma df dataframe original
app.callback(
    Output('store-transformed', 'data'),
    Input('export-button', 'n_clicks'),
    State('store-inputs', 'data'),
    Input('intermediate-value', 'data')
)(export_dataframe)

# Estos callbacks son para los dropdowns personalizados
create_callbacks('1',opciones_clases)
create_callbacks('2',opciones_bancos)  
create_callbacks('3',opciones_agencias)
create_callbacks('4',opciones_atm)
create_callbacks('5',opciones_ceme)
create_callbacks('6',opciones_hoteles)

if __name__ == '__main__':
    app.run_server(debug=True)
