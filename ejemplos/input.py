import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from dash.dependencies import MATCH, ALL
import json
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

num_of_inputs = 14

# Dummy DataFrame
df = pd.DataFrame({'Values': range(1, num_of_inputs+1)})

inputs = []
texts = [
    'Banco BNB',
    'Otros Bancos',
    'ATMs',
    'SuperMercados',
    'Centros Médicos',
    'Hoteles',
    'Otros'
]

for i in range(num_of_inputs):
    if i % 2 == 0:
        text_index = i // 2  # Índice para determinar el texto correspondiente
        input_item = dbc.Row(
            [
                dbc.Col(html.H5(texts[text_index]), width=12),  # Texto en la parte superior
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Peso",style={'width': '60px'}),
                            dcc.Input(
                                id={'type': 'input', 'index': i},
                                type='number',
                                min=0,
                                max=10,
                                placeholder=f'Enter something here...',
                            ),
                        ]
                    ), width=12
                )
            ]
        )
    else:
        input_item = dbc.Row(
            [
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Radio",style={'width': '60px'}),
                            dcc.Input(
                                id={'type': 'input', 'index': i},
                                type='number',
                                min=0,
                                max=500,
                                placeholder=f'Enter something here...',
                            ),
                        ]
                    ), width=12
                )
            ]
        )
    inputs.append(input_item)


app.layout = html.Div([
    dbc.Button("Open Offcanvas", id="open-offcanvas", n_clicks=0),
    dcc.Store(id='store-inputs', data=df['Values'].to_dict()),
    dbc.Offcanvas(
        dbc.Container(
            dbc.Row(
                dbc.Col(
                    inputs,
                    width=12
                ),
                justify="center"
            )
        ),
        id="offcanvas",
        title="Title",
        is_open=False,
        scrollable=True,
    )
])

@app.callback(
    [
        Output("offcanvas", "is_open"),
        Output({'type': 'input', 'index': ALL}, 'value'),
        Output('store-inputs', 'data')
    ],
    [
        Input("open-offcanvas", "n_clicks"),
        Input({'type': 'input', 'index': ALL}, 'n_blur')
    ],
    [
        State("offcanvas", "is_open"),
        State({'type': 'input', 'index': ALL}, 'value'),
        State('store-inputs', 'data')
    ]
)
def toggle_offcanvas(n1, n2, is_open, input_values, store_data):
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open, input_values, store_data
    else:
        prop_id = ctx.triggered[0]['prop_id']
        if 'open-offcanvas' in prop_id:
            return not is_open, [store_data.get(str(i), '') for i in range(num_of_inputs)], store_data
        elif 'input' in prop_id:
            index = json.loads(prop_id.split('.')[0])['index']
            if input_values[index] is None:
                input_values[index] = store_data.get(str(index), '')
                return is_open, input_values, store_data
            else:
                store_data[str(index)] = input_values[index]
                return is_open, input_values, store_data
    return is_open, input_values, store_data

if __name__ == '__main__':
    app.run_server(debug=True)







