import os
os.environ['USE_PYGEOS'] = '0'
import dash
import base64
import io
import pandas as pd
import geopandas as gpd
import numpy as np
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import plotly.graph_objects as go
from dash import html
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
def create_map_figure(df, polygon_geojson=None):

 
    fig = go.Figure()

    if polygon_geojson is not None:
        gdf = gpd.GeoDataFrame.from_features(polygon_geojson['features'])
        choropleth_layer = go.Choroplethmapbox(
            geojson=polygon_geojson,
            locations=gdf.index.astype(str),
            z=gdf['Nivel'], # Usar la columna '0' como valores de color 
            colorscale='Turbo',
            hoverinfo='all', # Muestra toda la información en el hover
            hovertemplate='Nivel: %{z}<extra></extra>', # Personaliza el hover para mostrar solo la información que deseas
            #marker_opacity=0.2,
            showscale=False,
            #marker_line_width=10
            marker=go.choroplethmapbox.Marker(
                opacity=0.2,
                line_width=2,  # Ajustar este valor para cambiar el grosor de las líneas de contorno
                line_color='rgba(0,0,0,0.9)'  # Ajustar este valor para cambiar el color de las líneas de contorno
            )
            # Resto de las configuraciones para la capa de polígonos...
        )
        fig.add_trace(choropleth_layer)

    scatter_trace = go.Scattermapbox(
        lat= df.Latitud,
        lon= df.Longitud,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=10,
            color=df['Color'],
        ),
        
        hovertemplate=
        '<b>Latitud</b>: %{lat}<br>' +
        '<b>Longitud</b>: %{lon}<br>' +
        '<b>Tipo de punto</b>: %{customdata[0]}<extra></extra>',
        customdata=df[['Clase']].values
    )

    fig.add_trace(scatter_trace)

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        margin=dict(l=0, r=0, t=0, b=0),
        mapbox=dict(
            accesstoken = token,
            style='dark',
            center={'lat': df.Latitud.mean(), 'lon': df.Longitud.mean()},
            zoom = 12,
            uirevision = 'constant' # agrega esta línea
        ),
        
    )

    return fig
###################################################################### hace todo los calculos para generar el KDE
def perform_kde(df, contour_levels=12):

    #Creo el gdf y cambio a UTM
    gdf = toGeojson(df,'Latitud','Longitud')
    gdf2 = gdf.to_crs(32720)

    #Obtiene los valores UTM
    lon = gdf2.geometry.x
    lat = gdf2.geometry.y
    peso = gdf2.Peso
    radio = gdf2.Radio

    #Los convierte a listas
    x = lon.to_list()
    y = lat.to_list()
    weights = peso.to_list()
    radii = radio.to_list()

    # Crear una cuadrícula de puntos
    x_grid, y_grid = np.meshgrid(np.linspace(min(x), max(x), 400), np.linspace(min(y), max(y), 200))

    # Calcular la influencia de cada punto en la cuadrícula
    influence = np.zeros_like(x_grid)
    for xi, yi, w, r in zip(x, y, weights, radii):
        dist = np.sqrt((x_grid - xi)**2 + (y_grid - yi)**2)
        #influence += np.exp(-dist**2 / (2 * r**2)) * w #Gaussian 95.1%
        #influence += np.maximum(1 - dist / r, 0) * w #Triangular 98.6%
        influence += np.maximum((1 - (dist / r) ** 2) ** 3, 0) * w  #Triweight 98.7%
    
    # Obtener los contornos sin relleno
    contours = plt.contour(x_grid, y_grid, influence, levels=contour_levels, colors='k').allsegs
    # Cerrar la figura para evitar que se muestre
    plt.close()

    # Crear los polígonos y el diccionario de atributos
    polygons = []
    for level, contour in zip(range(contour_levels), contours):
        for segment in contour:
            if len(segment) > 4:
                polygon = Polygon(segment)
                polygons.append({'Nivel': level, 'geometry': polygon})

    # Crear el GeoDataFrame de polígonos
    gdf_polygons = gpd.GeoDataFrame(polygons,crs="EPSG:32720")

    return gdf_polygons.to_crs(epsg=4326)
###################################################################### hace obtine los valores peso y radio del df
def transform_df(df_t):

    df = pd.DataFrame(df_t)
    classes = ['Agencia', 'ATM', 'Supermercado', 'Centro Médico', 'Hotel']
    other_classes = ['Centro Comercial', 'Mercado','Restaurante','Universidad']
    store_data = {}
    
    for i, cls in enumerate(classes):
        if cls == 'Agencia':
            p = df[(df['Clase'] == cls) & (df['Banco'] == 'Banco Nacional de Bolivia S.A.')]['Peso'].iloc[0]
            r = df[(df['Clase'] == cls) & (df['Banco'] == 'Banco Nacional de Bolivia S.A.')]['Radio'].iloc[0]
            store_data[str(2*i)] = p
            store_data[str(2*i + 1)] = r
            p = df[(df['Clase'] == cls) & (df['Banco'] != 'Banco Nacional de Bolivia S.A.')]['Peso'].iloc[0]
            r = df[(df['Clase'] == cls) & (df['Banco'] != 'Banco Nacional de Bolivia S.A.')]['Radio'].iloc[0]
            store_data[str(2*i + 2)] = p
            store_data[str(2*i + 3)] = r
        else:
            p = df[df['Clase'] == cls]['Peso'].iloc[0]
            r = df[df['Clase'] == cls]['Radio'].iloc[0]
            store_data[str(2*i + 2)] = p
            store_data[str(2*i + 3)] = r

    p = df[df['Clase'].isin(other_classes)]['Peso'].iloc[0]
    r = df[df['Clase'].isin(other_classes)]['Radio'].iloc[0]
    store_data[str(2*len(classes) + 2)] = p
    store_data[str(2*len(classes) + 3)] = r
    
    return store_data



##########################################################################################################################################################
#Inicio Callback que almacena el df, crea los dropdowns y los botones
##########################################################################################################################################################
def load_data_and_dropdowns(contents, filename):
    colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf', '#999999']

    if contents is None:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    df = parse_contents(contents, filename)

    if isinstance(df, pd.DataFrame):
        # Convierte el DataFrame a un formato que sea serializable
        dp1 = create_dropdown(df,'Clase','Dropdown_1','Tipo Punto')
        dp2 = create_dropdown(df,'Banco','Dropdown_2','Bancos')
        dp3 = create_dropdown(df,'TipoAgencia','Dropdown_3','Tipo Agencia')
        dp4 = create_dropdown(df,'TipoCentroMedico','Dropdown_4','Tipo Centro Médico')
        dp5 = create_dropdown(df,'TipoHotel','Dropdown_5','Tipo Hospedaje')
        dp6 = create_dropdown(df,'DepositoATM','Dropdown_6','ATM con depósito')

        # Generar la columna de colores según la categoría
        categories = df['Clase'].unique()
        color_mapping = {category: colors[i % len(colors)] for i, category in enumerate(categories)}
        df['Color'] = df['Clase'].map(color_mapping)
        
        #retorna el estilo con que se debe ver el boton kde
        kde_style = {'display': 'block','padding-left': '145px'}
        off_canvas_button = {'display': 'block','padding-bottom': 10, 'padding-top': 5}
        return df.to_dict('records'), dp1, dp2, dp3, dp4, dp5, dp6,kde_style, off_canvas_button
    else:
        raise dash.exceptions.PreventUpdate
##########################################################################################################################################################
#Fin Callback que almacena el df
##########################################################################################################################################################


##########################################################################################################################################################
#Inicio Callback que crea el mapa
##########################################################################################################################################################
def generate_map(df_dict, current_figure, current_config, kde_output):
    # Si no se creo el df la funcion se sale directamente
    if df_dict is None:
        return {'display': 'none'}, {'display': 'block'}, dash.no_update, dash.no_update

    ctx = dash.callback_context
    triggered_by_kde_output = ctx.triggered and ctx.triggered[0]['prop_id'] == 'kde-output.data'

    filtered_df = pd.DataFrame(df_dict)

    # esta es un verificacion de refuerzo para ver si el csv tien columnas latitud y longitud si no tiene sale del callback
    if 'Latitud' not in filtered_df.columns or 'Longitud' not in filtered_df.columns:
        raise dash.exceptions.PreventUpdate
    
    # Comprobar si se generó un nuevo JSON de polígonos mediante el kde-output
    if triggered_by_kde_output:
        # Obtener el GeoJSON de los polígonos
        kde_geojson = json.loads(kde_output)
    else:
        kde_geojson = None

    #Comprueba si existe una figura, si existe solo actualiza los puntos si no pasa crear la figura y tambien si no se disparo el KDE
    if current_figure is not None and current_config is not None and not triggered_by_kde_output:
        fig = go.Figure(current_figure)

        # Encuentra la traza Scattermapbox
        scatter_trace = None
        for trace in fig.data:
            if isinstance(trace, go.Scattermapbox):
                scatter_trace = trace
                break


        # Si encontramos la traza Scattermapbox, actualizamos los datos
        if scatter_trace is not None:
            scatter_trace.lat = filtered_df['Latitud']
            scatter_trace.lon = filtered_df['Longitud']
            scatter_trace.marker = dict(
                size=10,  # Actualizar el tamaño de los puntos
                color=filtered_df['Color'],    
            )  # Actualizar los colores
            scatter_trace.customdata = filtered_df[['Clase']].values  # Actualizar las clases
            fig.update_traces(scatter_trace, selector=dict(type='scattermapbox'))
            #print('siempre estoy aqui?')
            
            ##if triggered_by_dropdown:
                ##return dash.no_update, dash.no_update, fig, current_config
        
    else:
        fig = create_map_figure(filtered_df, kde_geojson)

    config = {
        'scrollZoom': True,
        'displayModeBar': True,
        'editable': True,
        'displaylogo': False,
        'autosizable': True,
    }

    return {'display': 'block'}, {'display': 'none'}, fig, config
##########################################################################################################################################################
#Fin Callback que crea el mapa
##########################################################################################################################################################


##########################################################################################################################################################
#Inicio Callback para modificar el dataframe
##########################################################################################################################################################
def filter_df(dropdown_value_1,dropdown_value_2,dropdown_value_3,dropdown_value_4,dropdown_value_5,dropdown_value_6,df_dict):
    
    # Si no se creo el df la funcion se sale directamente
    if df_dict is None:
        return dash.no_update

    #convierte la entrada df_dict en un df
    df = pd.DataFrame(df_dict)

    # esta es un verificacion de refuerzo para ver si el csv tien columnas latitud y longitud si no tiene sale del callback
    if 'Latitud' not in df.columns or 'Longitud' not in df.columns:
        raise dash.exceptions.PreventUpdate

    #si el trigger fue por el dropdown1 entonces el df se filtra y si no el df es el mismo
    #filtra los tipo de puntos
    if dropdown_value_1 is None or len(dropdown_value_1) == 0:
        df_t = df
    else:
        df_t = df[df['Clase'].isin(dropdown_value_1)]

    #filtra los Bancos
    if dropdown_value_2 is None or len(dropdown_value_2) == 0:
        df_banco = df_t
    else:
        df_banco = df_t[df_t['Banco'].isin(dropdown_value_2)]


    _df_agn = df_banco[df_banco['Clase'] == 'Agencia']
    _df_atm = df_banco[df_banco['Clase']== 'ATM']
    df_poi = df_t[df_t['Clase'].isin(['Centro Comercial','Mercado','Supermercado','Restaurante','Universidad'])]
    _df_hot = df_t[df_t['Clase']== 'Hotel']
    _df_cem = df_t[df_t['Clase']== 'Centro Médico']

    #filtra los tipo de agencias
    if dropdown_value_3 is None or len(dropdown_value_3) == 0:
        df_agn =_df_agn
    else:
        df_agn = _df_agn[_df_agn['TipoAgencia'].isin(dropdown_value_3)]

    #filtra los tipo de ATM
    if dropdown_value_6 is None or len(dropdown_value_6) == 0:
        df_atm = _df_atm
    else:
        df_atm = _df_atm[_df_atm['DepositoATM'].isin(dropdown_value_6)]

    #filtra los tipo de centros medicos
    if dropdown_value_4 is None or len(dropdown_value_4) == 0:
        df_cem = _df_cem
    else:
        df_cem = _df_cem[_df_cem['TipoCentroMedico'].isin(dropdown_value_4)]

    #filtra los tipo de hotel
    if dropdown_value_5 is None or len(dropdown_value_5) == 0:
        df_hot = _df_hot
    else:
        df_hot = _df_hot[_df_hot['TipoHotel'].isin(dropdown_value_5)]


    filtered_df = pd.concat([df_agn,df_atm,df_poi,df_hot,df_cem])
    print(filtered_df.Peso.unique())

    print('El numero de datos es:', len(filtered_df))

    if isinstance(filtered_df, pd.DataFrame):
        return filtered_df.to_dict('records')
    else:
        raise dash.exceptions.PreventUpdate
##########################################################################################################################################################
#Fin Callback para modificar el dataframe
##########################################################################################################################################################


##########################################################################################################################################################
#Inicio Callback que despliega el off-canvas
##########################################################################################################################################################
def toggle_offcanvas(n1, n2,df_dict, is_open, input_values, store_data):
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open, input_values, store_data
    else:
        prop_id = ctx.triggered[0]['prop_id']
        if 'open-offcanvas' in prop_id:
            # Si 'store_data' está vacío, entonces inicializa con 'intermediate-value', 'data'
            if not store_data:
                store_data = transform_df(df_dict)  # Aquí debes implementar tu función de transformación
            return not is_open, [store_data.get(str(i), '') for i in range(14)], store_data
        elif 'input' in prop_id:
            index = json.loads(prop_id.split('.')[0])['index']
            if input_values[index] is None:
                input_values[index] = store_data.get(str(index), '')
                return is_open, input_values, store_data
            else:
                store_data[str(index)] = input_values[index]
                return is_open, input_values, store_data
    return is_open, input_values, store_data
##########################################################################################################################################################
#Fin Callback que despliega el off-canvas
##########################################################################################################################################################


##########################################################################################################################################################
#Fin Callback que transforma los datos
##########################################################################################################################################################
def export_dataframe(n_clicks, store_data, intermediate_data):
    if n_clicks is None:  # el botón no ha sido presionado
        return intermediate_data
    else:
        df = pd.DataFrame(intermediate_data)
        # debes reordenar los valores en el store_data para que coincidan con las columnas correspondientes en tu dataframe
        # por ejemplo:
        new_weights = [store_data[str(i)] for i in range(0, 14, 2)]
        new_radii = [store_data[str(i)] for i in range(1, 14, 2)]
        df.loc[(df['Clase'] == 'Agencia') & (df['Banco'] == 'Banco Nacional de Bolivia S.A.'), 'Peso']= new_weights[0]
        df.loc[(df['Clase'] == 'Agencia') & (df['Banco'] == 'Banco Nacional de Bolivia S.A.'), 'Radio']= new_radii[0]
        df.loc[(df['Clase'] == 'Agencia') & (df['Banco'] != 'Banco Nacional de Bolivia S.A.'), 'Peso']= new_weights[1]
        df.loc[(df['Clase'] == 'Agencia') & (df['Banco'] != 'Banco Nacional de Bolivia S.A.'), 'Radio']= new_radii[1]
        df.loc[df['Clase'] == 'ATM', 'Peso'] = new_weights[2]
        df.loc[df['Clase'] == 'ATM', 'Radio'] = new_radii[2]
        df.loc[df['Clase'] == 'Supermercado', 'Peso'] = new_weights[3]
        df.loc[df['Clase'] == 'Supermercado', 'Radio'] = new_radii[3]
        df.loc[df['Clase'] == 'Centro Médico', 'Peso'] = new_weights[4]
        df.loc[df['Clase'] == 'Centro Médico', 'Radio'] = new_radii[4]
        df.loc[df['Clase'] == 'Hotel', 'Peso'] = new_weights[5]
        df.loc[df['Clase'] == 'Hotel', 'Radio'] = new_radii[5]
        df.loc[df['Clase'].isin(['Centro Comercial', 'Mercado', 'Restaurante', 'Universidad']), 'Peso'] = new_weights[6]
        df.loc[df['Clase'].isin(['Centro Comercial', 'Mercado', 'Restaurante', 'Universidad']), 'Radio'] = new_radii[6]

        return df.to_dict(orient='records')
##########################################################################################################################################################
#Fin Callback que despliega el off-canvas
##########################################################################################################################################################



##########################################################################################################################################################
#Inicio Callback desarrolla el KDE
##########################################################################################################################################################
def generate_gson(n_clicks, df_dict):

    if n_clicks is None or df_dict is None:
        raise dash.exceptions.PreventUpdate
    
    #genero el df
    df = pd.DataFrame(df_dict)
    
    if len(df)<2:
        raise dash.exceptions.PreventUpdate
    
    levels = 12  # Número de niveles de contorno
    kde_gdf = perform_kde(df,levels)

    #convierte el geodataframe en json
    kde_geojson = kde_gdf.to_json()
    print('Se genero el KDE')
    return kde_geojson
##########################################################################################################################################################
#Fin Callback desarrolla el KDE
##########################################################################################################################################################

