import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output, State

path = 'C:/Users/joels/altitudesolutions.org/AS - Clientes/57 BNB/2. Datos/POI/PuntosDeInteresCBB2.csv'
df = pd.read_csv(path)

app = dash.Dash(__name__)

def create_dropdown(id):
    return dcc.Dropdown(
        id=id,
        options=[{'label': i, 'value': i} for i in df.columns]
    )

app.layout = html.Div([
    html.Div(children=[
        html.Label('Dropdown'),
        create_dropdown('column-dropdown1'),
        html.Br(),
        html.Label('Multi-Select Dropdown'),
        dcc.Dropdown(id='item-dropdown1',multi=True),

        html.Label('Dropdown'),
        create_dropdown('column-dropdown2'),
        html.Br(),
        html.Label('Multi-Select Dropdown'),
        dcc.Dropdown(id='item-dropdown2',multi=True),

        html.Label('Dropdown'),
        create_dropdown('column-dropdown3'),
        html.Br(),
        html.Label('Multi-Select Dropdown'),
        dcc.Dropdown(id='item-dropdown3',multi=True),

        html.Label('Dropdown'),
        create_dropdown('column-dropdown4'),
        html.Br(),
        html.Label('Multi-Select Dropdown'),
        dcc.Dropdown(id='item-dropdown4',multi=True),

    ], style={'padding': 10, 'flex': 1}),
])

@app.callback(
    Output('column-checklist', 'options'),
    Input('column-dropdown', 'value')
)
def set_checklist_options(selected_column):
    if selected_column is None:
        raise dash.exceptions.PreventUpdate
    unique_values = df[selected_column].dropna().unique()
    unique_values = sorted(unique_values, key=str)  # Ordenar los valores
    return [{'label': str(i), 'value': str(i)} for i in unique_values]


if __name__ == '__main__':
    app.run_server(debug=True)

