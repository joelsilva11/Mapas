import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, callback_context

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

options = [{'label': f'Opción {i+1}', 'value': f'Valor {i+1}'} for i in range(10)]

app.layout = html.Div(
    [
        html.Div(
            [
                html.H5("Bancos", style={'padding-left': '10px','padding-top':'7px','margin-bottom': '5px'}),
                dbc.InputGroup(
                    [
                        dbc.Input(id="input", value="", readonly=True,),
                        dbc.Button("▼", id="kde-button", color="primary")
                    ],
                    style={'padding-left': '10px','padding-right': '10px'}
                ),
            
        html.Div(
            [   
                dbc.Checklist(options=["All"], value=[], id="all-checklist"),
                dbc.Checklist(options=options, value=[], id="checklist",style={'padding-left': 8}),
            ],
            id='checklist_container',
            style={'display':'none','backgroundColor': 'black','margin-left': '10px','margin-right': '10px','borderRadius': '4px','overflow': 'auto','maxHeight': '180px'}
        ),
        ],
            style={'backgroundColor': '#333','borderRadius': '4px','height': '88px'}
        ),
    ],
    style={'width': '15%'}
)

@app.callback(
    Output("checklist", "value"),
    Output("all-checklist", "value"),
    Input("checklist", "value"),
    Input("all-checklist", "value"),
)
def sync_checklists(cities_selected, all_selected):
    print('Valor del opciones: ',cities_selected, end='     ') 
    print('Valor All: ', all_selected)

    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if input_id == "checklist":
        all_selected = ["All"] if set(cities_selected) == set([i['value'] for i in options]) else []
    else:
        cities_selected = [i['value'] for i in options] if all_selected else []
    return cities_selected, all_selected

@app.callback(
    Output("input", "value"),
    [Input("checklist", "value")],
)
def update_input(values):
    # Convert the values to their corresponding labels
    #labels = [option["label"] for option in options if option["value"] in values]
    labels = [option["value"] for option in options if option["value"] in values]

    # Join all labels with commas and return the result
    return ", ".join(labels)

if __name__ == '__main__':
    app.run_server(debug=True)
