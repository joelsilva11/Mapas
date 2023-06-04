import dash
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

options=[{'label': f'Opción {i+1}', 'value': str(i+1)} for i in range(10)]
all_option = {'label': 'Todos', 'value': 'ALL'}

checklist_visible = False

dropdown_button = dbc.Button("Opciones", id="dropdown-button", color="primary", className="mb-3")

dropdown_checklist = html.Div([
    dbc.Checklist(
        id=f"checkbox-{opt['value']}",
        options=[{'label': opt['label'], 'value': opt['value']}],
        inline=True,
        #style={'display': 'none'}
    ) for opt in options
    
], id='dropdown-checklist',style={'display': 'none'})

store = dbc.Checklist(id='selected-values', options=[{'label': opt['label'], 'value': opt['value']} for opt in options])

app.layout = html.Div([
    html.Div(id='output_div'),
    dropdown_button,
    dropdown_checklist,
    store
])

@app.callback(
    Output('dropdown-button', 'children'),
    Output('dropdown-button', 'color'),
    Output('dropdown-checklist', 'style'),
    Input('dropdown-button', 'n_clicks'),
    State('dropdown-checklist', 'style')
)
def toggle_checklist(n_clicks, checklist_style):
    global checklist_visible
    if n_clicks is None:
        n_clicks = 0
    if n_clicks % 2 == 0:
        checklist_visible = False
        return "Opciones", "primary", {'display': 'none'}
    else:
        checklist_visible = True
        return "Ocultar Opciones", "success", {'display': 'block'}

@app.callback(
    Output('output_div', 'children'),
    [Input('selected-values', 'value')]
)
def update_output(checked_values):
    return html.Div(f'Has seleccionado: {checked_values}')

if __name__ == '__main__':
    app.run_server(debug=True)
