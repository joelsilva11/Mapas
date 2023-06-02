import dash
from dash import dcc, html,dash_table,exceptions
import pandas as pd
from dash.dependencies import Input, Output, State


# Crea un DataFrame de ejemplo
df = pd.DataFrame({
    'Category': ['A', 'B', 'A', 'B', 'C', 'C', 'A', 'B', 'C'],
    'Number': [1, 2, 3, 4, 5, 6, 7, 8, 9]
})

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Button('Edit', id='edit-button', n_clicks=0),
    html.Div(id='inputs-container', children=[
        dcc.Input(id='input-A', type='number', value=''),
        dcc.Input(id='input-B', type='number', value=''),
        dcc.Input(id='input-C', type='number', value=''),
    ], style={'display': 'none'}),  # Ocultar por defecto
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        editable=False
    )
])

@app.callback(
    Output('inputs-container', 'style'),
    Output('input-A', 'value'),
    Output('input-B', 'value'),
    Output('input-C', 'value'),
    Input('edit-button', 'n_clicks'),
    State('table', 'data')
)
def show_inputs(n_clicks, rows):
    if n_clicks % 2 == 0:  # Si es par, ocultar
        return {'display': 'none'}, dash.no_update, dash.no_update, dash.no_update
    else:  # Si es impar, mostrar y cargar valores originales
        df = pd.DataFrame(rows)
        values_a = df[df['Category'] == 'A']['Number'].iloc[0]
        values_b = df[df['Category'] == 'B']['Number'].iloc[0]
        values_c = df[df['Category'] == 'C']['Number'].iloc[0]
        return {'display': 'block'}, values_a, values_b, values_c

@app.callback(
    Output('table', 'data'),
    Input('edit-button', 'n_clicks'),
    [State('input-A', 'value'),
    State('input-B', 'value'),
    State('input-C', 'value'),
    State('table', 'data')]
)
def update_columns(n_clicks, value_a, value_b, value_c, rows):
    if n_clicks % 2 != 0:  # Si es par, no realizar actualizaciones
        raise exceptions.PreventUpdate

    df = pd.DataFrame(rows)

    # Verificar si se ha introducido un valor antes de realizar el cambio
    if value_a is None:
        raise exceptions.PreventUpdate("The input for category 'A' should not be empty.")
    else:
        df.loc[df['Category'] == 'A', 'Number'] = value_a

    if value_b is None:
        raise exceptions.PreventUpdate("The input for category 'B' should not be empty.")
    else:
        df.loc[df['Category'] == 'B', 'Number'] = value_b

    if value_c is None:
        raise exceptions.PreventUpdate("The input for category 'C' should not be empty.")
    else:
        df.loc[df['Category'] == 'C', 'Number'] = value_c

    return df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
