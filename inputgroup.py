import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

options = [{'label': f'Opción {i+1}', 'value': f'Valor {i+1}'} for i in range(10)]

app.layout = html.Div(
    [
        dbc.InputGroup(
            [
                dbc.Input(id="input", value=""),
                dbc.Button("▼", id="dropdown-button", color="secondary")
            ]
        ),
        html.Div(
            [
                html.Div(
                    dcc.Checklist(options=options, value=[], id="checklist"),
                    style={'padding-left': 8}
                ),
            ],
            id='checklist_container',
            style={'display':'none'}
        ),
    ]
)

@app.callback(
    Output('checklist_container', 'style'),
    [Input('dropdown-button', 'n_clicks')],
    [State('checklist_container', 'style')]
)
def toggle_checklist(n, style):
    print('Veces pulsado: ',n)
    print('Estado display: ',style['display'])
    if n:
        if style['display'] == 'none':
            return {'display': 'block'}
        else:
            return {'display': 'none'}
    return style

@app.callback(
    Output("input", "value"),
    [Input("checklist", "value")],
)
def update_input(values):
    # Convert the values to their corresponding labels
    labels = [option["label"] for option in options if option["value"] in values]

    # Join all labels with commas and return the result
    return ", ".join(labels)

if __name__ == '__main__':
    app.run_server(debug=True)
