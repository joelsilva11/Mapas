import dash
from dash import Dash, dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

options = [{'label': f'Opción {i+1}', 'value': f'Valor {i+1}'} for i in range(10)]

app.layout = html.Div(
    [
        dbc.Button('Filter', id='kde-button', n_clicks=0, style={'width': '100%','height': '50px'}, color="success"),
        html.Div(
            [
                html.Div(
                    dcc.Checklist(options=["All"], value=[], id="all-checklist",style={'display': 'flex', 'flexDirection': 'column'}),
                    #style={'padding-right': 10}
                ),
                html.Div(
                    dcc.Checklist(options=options, value=[], id="city-checklist",style={'display': 'flex', 'flexDirection': 'column'}),
                    #style={'padding-right': 10}
                ),
            ],
            className='scrollable-div',
            id='checklist_container',
            style={'display':'none', 'maxHeight': '250px', 'backgroundColor': '#181818', 'overflow': 'auto', 'width': '10%', 'position': 'absolute', 'z-index': '9999'}
        ),
        dbc.Button('Prueba', n_clicks=0, style={'width': '7%','height': '50px'}, color="success"),
    ]
)

"""@app.callback(
    Output('checklist_container', "style"),
    [Input('kde-button', "n_clicks")],
    [State('checklist_container', 'style')]
)
def show_filter(n_clicks, current_style):
    print(current_style.get('display'))
    if n_clicks % 2 == 0:
        return {'display': 'none'}
    else:
        if current_style and current_style.get('display') == 'block':
            return current_style
        else:
            return {'display': 'block', 'maxHeight': '150px', 'background-color': 'gray', 'overflow': 'auto', 'width': '15%', 'position': 'absolute', 'z-index': '9999'}"""

@app.callback(
    Output("city-checklist", "value"),
    Output("all-checklist", "value"),
    Input("city-checklist", "value"),
    Input("all-checklist", "value"),
)
def sync_checklists(cities_selected, all_selected):
    print('Valor del opciones: ',cities_selected, end='     ') 
    print('Valor All: ', all_selected)

    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if input_id == "city-checklist":
        all_selected = ["All"] if set(cities_selected) == set([i['value'] for i in options]) else []
    else:
        cities_selected = [i['value'] for i in options] if all_selected else []
    return cities_selected, all_selected

if __name__ == "__main__":
    app.run_server(debug=True)