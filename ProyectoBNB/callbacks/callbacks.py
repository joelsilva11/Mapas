import os
os.environ['USE_PYGEOS'] = '0'
import dash
import base64
import io
import pandas as pd
import geopandas as gpd
#import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from layout.layout import create_dropdown

token = 'pk.eyJ1Ijoiam1zczExIiwiYSI6ImNsN3RsbHpldDEwNDIzdm1rMG1qZWx6cmUifQ.svDPURTTxi1aHuHpzPU8sQ'
###################################################################### Funcion para verificar la carga del csv 
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        else:
            return html.Div([
                'Archivo no soportado: {}'.format(filename)
            ])
    except Exception as e:
        print(e)
        return html.Div([
            'Hubo un error al procesar este archivo.'
        ])

    if 'Latitud' not in df.columns or 'Longitud' not in df.columns:
        return html.Div([
            'El archivo no contiene las columnas necesarias: Latitud y Longitud.'
        ])

    return df


###################################################################### Funcion para crear un geodataframe a partir del csv
def toGeojson(df,latitud,longitud):
    return gpd.GeoDataFrame(df,geometry=gpd.points_from_xy(df[longitud],df[latitud],crs="EPSG:4326"))


###################################################################### Funcion para crear la figura del mapa
def create_map_figure(df):
    fig = go.Figure(go.Scattermapbox(
        #gdf,
        lat= df.Latitud,
        lon= df.Longitud,
        mode='markers',
        marker=go.scattermapbox.Marker(size=9),
        #zoom=11,
        #center={'lat': gdf.geometry.y.mean(), 'lon': gdf.geometry.x.mean()},
        #mapbox_style='carto-positron',
        #height=850,
        #hover_data=['Nombre', 'Direccion', 'Clase']
    ))

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        margin=dict(l=0, r=0, t=0, b=0),
        mapbox=dict(
            accesstoken = token,
            style='dark',
            center={'lat': df.Latitud.mean(), 'lon': df.Longitud.mean()},
            zoom = 12
        ),
        
    )

    return fig



##########################################################################################################################################################
#Inicio Callback que almacena el df y crea los dropdowns
##########################################################################################################################################################
def load_data_and_dropdowns(contents, filename):
    if contents is None:
        return dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update

    df = parse_contents(contents, filename)

    if isinstance(df, pd.DataFrame):
        # Convierte el DataFrame a un formato que sea serializable
        dp1 = create_dropdown(df,'Clase','Dropdown_1','Tipo Punto')
        dp2 = create_dropdown(df,'Banco','Dropdown_2','Bancos')
        dp3 = create_dropdown(df,'TipoAgencia','Dropdown_3','Tipo Agencia')
        dp4 = create_dropdown(df,'TipoCentroMedico','Dropdown_4','Tipo Centro Médico')
        dp5 = create_dropdown(df,'TipoHotel','Dropdown_5','Tipo Hospedaje')
        return df.to_dict('records'), dp1, dp2, dp3, dp4, dp5
    else:
        raise dash.exceptions.PreventUpdate
##########################################################################################################################################################
#Fin Callback que almacena el df
##########################################################################################################################################################


##########################################################################################################################################################
#Inicio Callback que crea el mapa y los dropdowns
##########################################################################################################################################################
def generate_map(dropdown_value_1, df_dict):
    '''Si no se carga el csv el callback retorna:
    Un contenedor del mapa escondido para css no existe
    Un contenedor del upload bloqueado y se muestra hasta que se cargue con existo el csv
    No actualiza el mapa porque no hay puntos evitando errores
    tampoco actualiza el contenedor del dropdown 
    '''
    if df_dict is None:
        return {'display': 'none'}, {'display': 'block'}, dash.no_update

    # Convierte el dict de vuelta a un DataFrame
    df = pd.DataFrame(df_dict)
    print('Valor de dp', dropdown_value_1)
    # Si dropdown_value_1 es None, no filtra el DataFrame
    if dropdown_value_1 is None or len(dropdown_value_1) == 0:
        filtered_df = df
    else:
        print(dropdown_value_1)
        filtered_df = df[df['Clase'].isin(dropdown_value_1)]

    # Verifica si el DataFrame tiene las columnas requeridas
    if 'Latitud' not in filtered_df.columns or 'Longitud' not in filtered_df.columns:
        raise dash.exceptions.PreventUpdate

    #gdf = toGeojson(df, 'Latitud', 'Longitud')
    fig = create_map_figure(filtered_df)
    return {'display': 'block'}, {'display': 'none'}, fig

##########################################################################################################################################################
#Inicio Callback que modifica el mapa con los dropdowns
##########################################################################################################################################################

def update_map(value, df_dict):
    df = pd.DataFrame(df_dict)
    # Filtrar df según el valor de Dropdown_1...
    filtered_df = df[df['Clase'] == value]
    fig = create_map_figure(filtered_df)
    return fig

