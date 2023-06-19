import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, callback_context

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

options = [{'label': f'Opción {i+1}', 'value': f'Valor {i+1}'} for i in range(10)]
options2 = [{'label': f'Opc {i+1}', 'value': f'Numero {i+1}'} for i in range(10)]
options3 = [{'label': f'Opt {i+1}', 'value': f'Num {i+1}'} for i in range(10)]

def create_dropdown(id_suffix, dp_options,title_dp = 'Title'):
    # Genera los IDs de los componentes con el sufijo proporcionado
    input_id = f'dp-input-{id_suffix}'
    button_id = f'dp-button-{id_suffix}'
    checklist_id = f'checklist-{id_suffix}'
    all_checklist_id = f'all-checklist-{id_suffix}'
    container_id = f'checklist_container-{id_suffix}'

    # Crea y devuelve el componente
    return html.Div(
        [
            html.H5(
                title_dp, 
                style={
                    'padding-left': '10px',
                    'padding-top':'7px',
                    'margin-bottom': '5px'
                }
            ),
            dbc.InputGroup(
                [
                    dbc.Input(id=input_id, value="", readonly=True,),
                    dbc.Button("▼", id=button_id, color="primary")
                ],
                style={
                    'padding-left': '10px',
                    'padding-right': '10px'
                }
            ),
            html.Div(
                [
                html.Div(
                    [   
                        dbc.Checklist(options=["All"], value=[], id=all_checklist_id, style={'padding-left': 8}),
                        dbc.Checklist(options=dp_options, value=[], id=checklist_id, style={'padding-left': 16}),
                    ],
                id=container_id,
                style={
                    'display':'none',
                    'backgroundColor': 'rgba(0, 0, 0, 0.92)', 
                    'borderRadius': '5px',
                    'overflow': 'auto',
                    'maxHeight': '180px', 
                    'position': 'absolute', 
                    'z-index': '9999',
                    'width': '100%',
                }
                ),
                ],
                style={
                    'position': 'relative',
                    'padding-left': '10px',
                    'margin-right': '20px'
                }
            ),
        ],
        style={
            
            'backgroundColor': '#222',
            'borderRadius': '4px',
            'height': '88px',
        }
    )

# Usar la función para crear componentes
dropdown1 = create_dropdown('1',options,'Bancos')
dropdown2 = create_dropdown('2',options, 'Agencias')
dropdown3 = create_dropdown('3',options, 'Otros')

app.layout = html.Div([dropdown1, dropdown2,dropdown3], 
                    style={
                          'width': '15%',
                          #'display': 'flex', 
                          #'flex-direction': 'row'
                    }
)

def create_callbacks(id_suffix):
    # Genera los IDs de los componentes con el sufijo proporcionado
    input_id = f'dp-input-{id_suffix}'
    button_id = f'dp-button-{id_suffix}'
    checklist_id = f'checklist-{id_suffix}'
    all_checklist_id = f'all-checklist-{id_suffix}'
    container_id = f'checklist_container-{id_suffix}'

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
            all_selected = ["All"] if set(item_selected) == set([i['value'] for i in options]) else []
        else:
            item_selected = [i['value'] for i in options] if all_selected else []

        return item_selected, all_selected

    @app.callback(
        Output(input_id, "value"),
        [Input(checklist_id, "value")],
    )
    def update_input(values):
        labels = [option["value"] for option in options if option["value"] in values]
        return ", ".join(labels)

# Usar la función para crear callbacks
create_callbacks('1')
create_callbacks('2')
create_callbacks('3')

if __name__ == '__main__':
    app.run_server(debug=True)