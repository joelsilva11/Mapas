import dash
from dash import dcc, html,Input,Output
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_daq as daq

app = dash.Dash(__name__)
#label = visto por el cliente
#value = filtrado por el callback
opciones = [{"label":"La Paz","value":"LPZ"}, {"label":"Santa Cruz","value":"SCZ"}, {"label":"Cochabamba","value":"CBB"}, {"label":"Oruro","value":"ORU"}, {"label":"Potosi","value":"POT"}, {"label":"Chuquisaca","value":"CHQ"}, {"label":"Beni","value":"BEN"},{"label":"Pando","value":"PND"}, {"label":"Tarija","value":"TJA"}]


dropdown = dcc.Dropdown(id = "DP1", options = opciones, value = None, multi = True)
# Si el estilo no funciona bien, ponerlo dentro de otro div
info_div = html.Div(["Ninguna Seleccion"],id = "seleccion",style = {"color": "white"})



app.layout = html.Div([
    html.Div([dropdown],
        style = {"width": "80%"}), 
    info_div], 
    style = {'backgroundColor': '#333', "height":"100vh" })

@app.callback(
    Output("seleccion", "children"),
    Output("seleccion", "style"),
    #State()
    Input("DP1", "value")
    #Input("DP2", "value")
    #State
    )
def cambiar_texto(drop):#,drop2):
    print(drop)
    if drop == None or drop == []:
        return "Ninguna Seleccion", {"backgroundColor":"red"}
    else: return drop, {"backgroundColor":"green"}




if __name__ == "__main__":
    app.run_server(debug=True, port = 8051)