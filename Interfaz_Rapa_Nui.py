#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 21:16:25 2021

@author: sebastian
"""

import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os as os
import numpy as np
import datetime
import base64
from datetime import date
from datetime import timedelta
from textwrap import dedent
from datetime import datetime as dt
from scipy.optimize import leastsq
from __toolsTrend import *
from __Anim import *
from __Traject import *
from __Profiles import *
from __Climatology import*
from __TrendGraphs import *

#Se importan datos

orig = os.getcwd()
fn_ozonosondes = orig + '/' + 'RapaNui_all_clear.csv' 
fn_ozonosondes_10 = orig + '/' + 'Ozonosondes_quantile10.csv'
fn_ozonosondes_30 = orig + '/' + 'Ozonosondes_quantile30.csv'
fn_ozonosondes_mean = orig + '/' + 'Ozonosondes_mean.csv'
fn_ozonosondes_70 = orig + '/' + 'Ozonosondes_quantile70.csv'
fn_ozonosondes_90 = orig + '/' + 'Ozonosondes_quantile90.csv'
fn_table = orig + '/Table_content.csv'
fn_trayect = orig + '/' +"RapaNui_BackTrajectories.csv"

ozonosondes_data = pd.read_csv(fn_ozonosondes, index_col=0, delimiter=';',parse_dates=True)
ozonosondes_climatology_10= pd.read_csv(fn_ozonosondes_10, index_col=0)
ozonosondes_climatology_30= pd.read_csv(fn_ozonosondes_30, index_col=0)
ozonosondes_climatology_mean= pd.read_csv(fn_ozonosondes_mean, index_col=0)
ozonosondes_climatology_70= pd.read_csv(fn_ozonosondes_70, index_col=0)
ozonosondes_climatology_90= pd.read_csv(fn_ozonosondes_90, index_col=0)
df_trayect = pd.read_csv(fn_trayect, index_col=[0,1,2], delimiter=';', parse_dates=True)
table_data = pd.read_csv(fn_table)

ozonosondes_data = ozonosondes_data.replace(9000, np.nan)
ozonosondes_data = ozonosondes_data.replace(9000000, np.nan)
################################### Mapa #####################################
Rapa_Nui = pd.DataFrame(data={"lat": [-27.13], "lon":[-109.35]})

fig = px.scatter_mapbox(Rapa_Nui, lat="lat", lon="lon",
                        color_discrete_sequence=["blue"], zoom=10)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

############################### fechas de las ozonosondas ####################

###############diccionario con fechas##########################################
df_year =  ozonosondes_data.iloc[~ozonosondes_data.index.year.duplicated(keep='first')].index.year
dates = {str(i):{str(j): ozonosondes_data[str(i)+'-'+str(j)][~ozonosondes_data[str(i)+'-'+str(j)].index.day.duplicated(keep='first')].index.day 
                 for j in ozonosondes_data[str(i)][~ozonosondes_data[str(i)].index.month.duplicated(keep='first')].index.month} for i in df_year}
dates_years = list(dates.keys())


ozonosondes_dates = ozonosondes_data.index[ozonosondes_data.index.duplicated(keep='first')==False]
# #Fechas en las cual no hay sondeo
# all_dates = pd.date_range(start=ozonosondes_dates[0], end=ozonosondes_dates[-1], freq="D")

# dates_disabled = all_dates[all_dates.isin(ozonosondes_dates.date)==False]
#imagenes
image_filename_cr2 = 'logo_footer110.png'
encoded_image_cr2 = base64.b64encode(open(image_filename_cr2, 'rb').read()).decode('ascii')
image_filename_DMC = 'logoDMC_140x154.png'
encoded_image_DMC = base64.b64encode(open(image_filename_DMC, 'rb').read()).decode('ascii')
image_filename_tololo = 'RapaNui.png'
encoded_image_tololo = base64.b64encode(open(image_filename_tololo, 'rb').read()).decode('ascii')
image_filename_cr2_celeste = 'cr2_celeste.png'
encoded_image_cr2_celeste = base64.b64encode(open(image_filename_cr2_celeste, 'rb').read()).decode('ascii')
image_filename_GWA = 'gaw_logo.png'
encoded_image_GWA = base64.b64encode(open(image_filename_GWA, 'rb').read()).decode('ascii')
image_filename_Rapa_Nui_Map = 'Easter-Island-Map.png'
encoded_image_Rapa_Nui_Map = base64.b64encode(open(image_filename_Rapa_Nui_Map, 'rb').read()).decode('ascii')

##### Ajustes para descarga de datos
title=[i for i in table_data.columns if i!='Download_url']
df_table=table_data.drop(['Download_url'], axis = 1)

df_table['Download'] = pd.Series(html.A(html.P(str(i)), href=str(j)) for i,j in zip(table_data['Download'], table_data['Download_url']))

############################# estilo de pestañas##############################

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'color': '#0668a1',
}

tab_selected_style = {
    'borderTop': '#1766a0',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#1766a0',
    'color': 'white',
    'padding': '6px'
}
###
colors = {
    'background': 'white',
    'text': '#7FDBFF',
    'background_2': 'white',
    'background_3': 'cyan'

}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}], title='Wayra') 
mathjax = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'
####### opciones matemáticas
app.scripts.append_script({ 'external_url' : mathjax })

navbar = dbc.Navbar(
    dbc.Container([
        dbc.Col([
            html.A([
            dbc.NavbarBrand("Wayra", style = {'font-size': '22pt',
                                      'font-family': 'times',
                                      'color':'white', 'display':'inline-block'})],
                style={'display':'inline-block'}),
            html.A([       
            html.Img(src = 'data:image/png;base64,{}'.format(encoded_image_cr2_celeste), 
                                                           style = {"height":"50px"})], 
                                                           href = 'http://www.cr2.cl/',
                                                           style = {'margin-left':'20px',
                                                                    'display':'inline-block'},
                                                           ),
                                                        
            html.A([
            html.Img(src = 'data:image/png;base64,{}'.format(encoded_image_DMC), 
                                                           style = {"height":"50px"})],
                                                           href = 'http://www.meteochile.gob.cl/PortalDMC-web',
                                                           style = {'margin-left':'20px',
                                                                    'display':'inline-block'}),
           html.A([
           html.Img(src='data:image/png;base64,{}'.format(encoded_image_GWA),
                                                        style = {"height":"50px"})],
                                                        href = 'https://www.wmo.int/pages/prog/arep/gaw/gaw_home_en.html',
                                                        style = {'margin-left':'20px',
                                                                 'display':'inline-block'})
            ], style={'display':'inline-block'}, xs=12, sm=12, md=4, lg=4, xl=4),
        dbc.Col([
            html.Div([
            html.P("Language:" , style={'font-size':'15pt','color': 'white', 'margin-top': '30px', 'text-align': 'center'})], style={'display':'inline-block'}),
            html.Div([
            daq.ToggleSwitch(
                id='Switch_Lang',
                className='SwicthLang',
                value=True,
                )], style={'display':'inline-block','margin-left':'2%'})
            ], style={'margin-left':'20%'},xs=10, sm=12, md=4, lg=4, xl=4)
    ]), color="#1766a0")



content =  html.Div(id='tabs-content', style={'backgroundcolor':'#f6f6f6'})
#Footer = html.Footer(style={'background-color':'#1766a0', 'height':'55px', 'margin-top':'20px'})
@app.callback(Output('tabs-content', 'children'),
              Input('Switch_Lang', 'value'))
def Web_Language(Switch_Lang):
#####################################Versión en Ingles###############################    
    if Switch_Lang==False:
        return [html.Div([
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-1',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Information',
                value='tab-1',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Graphs',
                value='tab-2',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Download Data',
                value='tab-3', className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Information',
                value='tab-4',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
        ]),
    html.Div(id='tabs-content-classes', style={'backgroundColor':'#f6f6f6'})
])]
#######################################Version en Español ##########################      
    if Switch_Lang==True:
        return [html.Div([
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-1',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Presentación',
                value='tab-1',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Gráficos',
                value='tab-2',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Descargar Datos',
                value='tab-3', className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Información',
                value='tab-4',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
        ]),
    html.Div(id='tabs-content-classes', style={'backgroundColor':'#f6f6f6'})
])]

@app.callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'),
              Input('Switch_Lang', 'value'))
def render_content(tab, Switch_Lang):
    if tab == 'tab-1':
        if Switch_Lang==False:
            return [html.Div([
                dbc.Row([
                dbc.Col([
                html.H1("Rapa Nui(27.16S, 109.43W, 41m)", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6', 'margin-top':'20px'})
                ,dcc.Markdown(dedent(f'''
                Rapa Nui (27ºS, 109ºW, 51 m a.s.l.) is influenced year-around by the eastern edge of the Pacific high resulting in to easterly and southeasterly boundary layer winds. Precipitation is generally convective in connection with the nearness of the South Pacific Convergence Zone (SPCZ). Precipitation also occurs in connection with mid-latitude disturbances and deep trough passages. Another prominent circulation feature affecting Rapa Nui is the subtropical jet stream (STJ), and its variability along the year. The main subsidence area associated with the subtropical high is located in between Rapa Nui and Western South America. Subsidence associated with the subtropical high peaks in summer, and it is suppressed in fall when the SPCZ reaches the island. Although weaker than in summer, subsidence also prevails in winter and spring. The STJ remains stationary over the island between fall and spring. A convective signature is found along the year, but it is particularly important in fall and winter. El Niño Southern Oscillation (ENSO) explains a significant part of the variability referred to above is linked to changes in atmospheric circulation due ENSO. The Pacific Decadal Oscillation (PDO) also affects weather and climate over Rapa Nui. 
                The seasonally averaged soundings indicate a fall minimum and a late spring maximum in ozone in the upper troposphere. The former occurs as the SPCZ approaches the island. The latter is suggestive of stratosphere-troposphere-exchange linked to the strength of the subtropical high and the nearness of the STJ in late winter and spring, allowing downward transport of stratospheric O3 present above 200 hPa. Occasionally, mid-latitude disturbances reach Rapa Nui inducing tropopause breaks and intrusions of stratospheric ozone. In the lower troposphere, extremes are found in summer and winter and they appear to be modulated by changes in insolation and static stability, showing larger ozone mixing ratios in winter than in summer. 
                Anthropogenic climate change, and the expansion of the Hadley cell is expected to affect the underlying dynamics that explain stratosphere-troposphere exchange affecting ozone profile. Also, there is evidence of increasing ozone trends near the surface that might be explained in part by the increase of anthropogenic activities on Rapa Nui. Hence, the remote location of Rapa Nui provides a unique and privileged position to observe global change, and to verify satellite borne measurements and modeling.

                Principal Investigators: Laura Gallardo, Carmen Vega        
                Emails: [lgallard@u.uchile.cl](mailto:lgallard@u.uchile.cl), [carmen.vega@dgac.gob.cl](mailto:carmen.vega@dgac.gob.cl)
                
                Data Site Manager: Francisca Muñoz, CR2 – Center for Climate and Resilience Research.            
                Email: [fmunoz@dgf.uchile.cl](mailto:fmunoz@dgf.uchile.cl)
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Data scientist: Charlie Opazo, CR2 - Center for Climate and Resilence Research.          
                Email: [charlie.opazo@ug.uchile.cl](mailto:charlie.opazo@ug.uchile.cl)
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Data scientist: Sebastian Villalón, CR2 - Center for Climate and Resilence Research.             
                Email: [sebastian.villalon@ug.uchile.cl](mailto:sebastian.villalon@ug.uchile.cl)
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Data Disclaimer: These data have been collected at Rapa Nui by the Chilean Weather Office (DMC) under the auspices of the Global Atmospheric Watch (GAW) Programme of the World Meteorological Organization (WMO).
    
                The data on this website are subject to revision and reprocessing. Check dates of creation to download the most current version.
    
                Contact the station principal investigator(s) for questions concerning data techniques and quality.
                
                
                
                '''), style={'margin-left':'6%', 'margin-right':'6%', 'display':'inline-block'})],
                md=10, lg={'size': 6,  "offset": 0, 'order': 0}),
                dbc.Col([
                                html.Img(src='data:image/png;base64,{}'.format(encoded_image_tololo),
                                         style={'height':'auto', 'width':'75%', 
                                                 'border': '0px solid #0668a1', 'border-radius': '10px',
                                                 'margin-top':'6%','margin-left':'12%'
                                                }
                                   ), 
                                    dcc.Markdown(dedent(f'''
                                                        Island location and photograph of Motu Nui and Motu Iti as seen from Orongo on the Rano Kau volcano, 
                                                        around 280 meters above sea level. Looking southwest. Photograph 2003 by Macarena San Martín'''), 
                                                 style={'font-size':'13px', 'margin-left':'75px'}),
                                    html.H1("Map", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}), 
                                    dcc.Graph(figure=fig, style={'height':'40%', 'width':'75%', 'margin-left':'12%'})
                                    ]
                                    
                                    , md=10, lg={'size': 6,  "offset": 0, 'order': 1})
                              ])
                              ]
                    )]
        elif Switch_Lang==True:
                    return[html.Div([
                        dbc.Row([
                        dbc.Col([
                        html.H1("Rapa Nui(27.16S, 109.43W, 41m)", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6', 'margin-top':'20px'})
                        ,dcc.Markdown(dedent(f'''
                        Rapa Nui (27ºS, 109ºW, 51 m s.n.m.) está influenciado durante todo el año por el borde oriental del Pacífico, lo que resulta en vientos de la capa límite del este y sureste. La precipitación es 
                        generalmente convectiva en relación con la proximidad de la Zona de Convergencia del Pacífico Sur (SPCZ). La precipitación también ocurre en relación con perturbaciones de latitudes medias y pasajes 
                        de vaguadas profundas. Otra característica de circulación prominente que afecta a Rapa Nui es la corriente en chorro subtropical (STJ) y su variabilidad a lo largo del año. El área de hundimiento principal 
                        asociada con el alto subtropical se encuentra entre Rapa Nui y el oeste de América del Sur. Subsidencia asociada con los picos subtropicales altos en verano, y se suprime en otoño cuando la SPCZ llega a la isla. Aunque 
                        más débil que en verano, el hundimiento también prevalece en invierno y primavera. El STJ permanece estacionario sobre la isla entre el otoño y la primavera. Se encuentra una firma convectiva a lo largo del año, pero es 
                        particularmente importante en otoño e invierno. El Niño Oscilación del Sur (ENOS) explica que una parte significativa de la variabilidad mencionada anteriormente está vinculada a cambios en la circulación atmosférica debido 
                        al ENOS. La Oscilación Decadal del Pacífico (DOP) también afecta el clima y el clima en Rapa Nui. Los sondeos promediados estacionalmente indican un mínimo de otoño y un máximo de finales de primavera en el ozono en la troposfera 
                        superior. Lo primero ocurre cuando la SPCZ se acerca a la isla. Esto último sugiere un intercambio estratosfera-troposfera vinculado a la fuerza del alto subtropical y la proximidad del STJ a fines del invierno y la primavera, lo que 
                        permite el transporte descendente del O3 estratosférico presente por encima de 200 hPa. Ocasionalmente, las perturbaciones de latitudes medias llegan a Rapa Nui provocando rupturas de la tropopausa e intrusiones de ozono estratosférico. 
                        En la troposfera inferior, los extremos se encuentran en verano e invierno y parecen estar modulados por cambios en la insolación y la estabilidad estática, mostrando mayores proporciones de mezcla de ozono en invierno que en verano. 
                        Se espera que el cambio climático antropogénico y la expansión de la célula de Hadley afecten la dinámica subyacente que explica el intercambio estratosfera-troposfera que afecta el perfil del ozono. Además, hay evidencia de tendencias 
                        crecientes del ozono cerca de la superficie que podrían explicarse en parte por el aumento de las actividades antropogénicas en Rapa Nui. Por lo tanto, la ubicación remota de Rapa Nui proporciona una posición única y privilegiada para observar 
                        el cambio global y verificar las mediciones y modelos satelitales.
                        
                        Investigadoras Principales: Laura Gallardo, Carmen Vega        
                        Emails: [lgallard@u.uchile.cl](mailto:lgallard@u.uchile.cl), [carmen.vega@dgac.gob.cl](mailto:carmen.vega@dgac.gob.cl)
                        
                        Data Site Manager: Francisca Muñoz, CR2 – Centro de Ciencia del Clima y la Resiliencia.         
                        Email: [fmunoz@dgf.uchile.cl](mailto:fmunoz@dgf.uchile.cl)
                        
                        Data scientist: Charlie Opazo, CR2 - Center for Climate and Resilence Research.          
                        Email: [charlie.opazo@ug.uchile.cl](mailto:charlie.opazo@ug.uchile.cl)
                        Av. Blanco Encalada 2002, Santiago, Chile
                        
                        Data scientist: Sebastian Villalón, CR2 - Center for Climate and Resilence Research.             
                        Email: [sebastian.villalon@ug.uchile.cl](mailto:sebastian.villalon@ug.uchile.cl)
                        Av. Blanco Encalada 2002, Santiago, Chile
                        
                        Descargo de responsabilidad sobre los datos: estos datos han sido recopilados en Rapa Nui por la Oficina Meteorológica de Chile (DMC) bajo los auspicios del Programa de Vigilancia Atmosférica Global (GAW) de la Organización Meteorológica Mundial (OMM).

                        Los datos de este sitio web están sujetos a revisión y reprocesamiento. Consulta las fechas de creación para descargar la versión más actual.
            
                        Comuníquese con el investigador principal de la estación si tiene preguntas sobre las técnicas y la calidad de los datos.

                        '''), style={'margin-left':'6%', 'margin-right':'6%', 'display':'inline-block'})],
                        md=10, lg={'size': 6,  "offset": 0, 'order': 0}),
                        dbc.Col([
                                        html.Img(src='data:image/png;base64,{}'.format(encoded_image_tololo),
                                                 style={'height':'auto', 'width':'75%', 
                                                         'border': '0px solid #0668a1', 'border-radius': '10px',
                                                         'margin-top':'6%','margin-left':'12%'
                                                        }
                                           ), 
                                            dcc.Markdown(dedent(f'''
                                                                Ubicación y fotografia de la isla de Moto Nui y Motu Iti que se observa desde Orongo en el volcán Rano Kau,
                                                                sobre los 280 metros del nivel del mar. Hacia el suroeste. 
                                                                Fotográfia tomada el 2003 por Macarena San Martín.
                                                                '''), 
                                                         style={'font-size':'13px', 'margin-left':'75px'}),
                                            html.H1("Mapa", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}), 
                                            dcc.Graph(figure=fig, style={'height':'40%', 'width':'75%', 'margin-left':'12%'})
                                            ]
                                            
                                            , md=10, lg={'size': 6,  "offset": 0, 'order': 1})
                                      ])
                                      ]
                            )]
    elif tab == 'tab-2':
        if Switch_Lang==False:
                return [html.Div([
                    dbc.Row([dbc.Col(html.H1("Vertical Profiles", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1'}))]),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Label('Date:', style={'color':'#0668a1','display': 'inline-block', 'margin-left':'15%'}),
                                  html.Div(
                                      [
                                          html.Div([
                                      dcc.Dropdown(id='dropdown_years_eng',style={'margin-top':'10px'}, options=[{'label':year,'value':year} for year in dates_years], placeholder="Year",value='1997')
                                      ], style={'width': '20%','margin-left':'5px', 'display': 'inline-block'}),
                                      html.Div([
                                      dcc.Dropdown(id='dropdown_months_eng', placeholder="Month",value = '3')
                                      ], style={'width': '20%','margin-top':'10px', 'display': 'inline-block'}),
                                      html.Div([
                                      dcc.Dropdown(id='dropdown_days_eng', placeholder="Day",value='7')
                                      ], style={'width': '20%','margin-top':'10px', 'display': 'inline-block'})
                                      
                                          
                                      ], style= {'width': '50%','display':'inline-block', 'margin-left':'0%', 'margin-top':'-13px'})
                            ])
                        ]),
              dbc.Row([
                  dbc.Col([
                      dcc.Graph(id='Vertical_profile_graph', figure={"layout":{"height":400, "width":1080}}, style={'margin-left':'10vw'})
                   
                                    ], xs=10, sm=10, md=10, lg=10, xl=10)]),
              
              dbc.Row([
                  dbc.Col([
                      html.Div([
                          html.H1("Climatology", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}),
                          html.Div([ html.Label('Date Range:', style={'color':'#0668a1','font-size':'18px', 'backgroundColor':'#f6f6f6'}),
                                    dcc.DatePickerRange(
                          id='calendar_1',
                         start_date=date(1997, 5, 3),
                         end_date=date(2014,5,3)
                          )], style={'margin-left':'50px'}),
                          html.Div([
                              html.Label('Variable:', style={'margin-right':'5px','color': '#0668a1','font-size':'18px'}), 
                                    html.Div([dbc.Container(
                                  [dbc.RadioItems(
                                      options=[
                          {"label": "Ozone", "value": "O3_ppbv"},
                          {"label": "Temperature", "value": "Temp"},
                          {"label": "Mixing Ratio", "value": "Mixing_Ratio"},
                          {"label": "HR", "value": "RH"},
                          {"label": "U", "value": "U"},
                          {"label": "V", "value": "V"}
                          
                      ],
                      id="radio_Climatology",
                      labelClassName="date-group-labels",
                      labelCheckedClassName="date-group-labels-checked",
                      className="date-group-items",
                      inline=True,
                      value="O3_ppbv"
                  ),
              ],
              className="p-3",
              )], style={'display':'inline-block'})
                  ],  style={'display':'inline-block', 'margin-left':'20px'}),
                          dcc.Graph(id="Climatology")], style={'margin-left':'100px','margin-top':'20px','width':'525px','height':'650px', 'display': 'inline-block'})
                      ])
                 ,
                  dbc.Col([
                      html.Div([
                      html.H1("Ozone Profile Animations", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'})
                  ,dcc.Graph(figure= AnimENG(ozonosondes_data, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA,
                                             ozonosondes_climatology_90, ozonosondes_climatology_70,
                             ozonosondes_climatology_30, ozonosondes_climatology_10, 
                             ozonosondes_climatology_mean))
                  ], style={'margin-left':'5px','width':'525px','height':'650px', 'display': 'inline-block'})
                      ])
                  ]),
              
              dbc.Row([
                  dbc.Col([
                      html.Div([html.H1('Trend', style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}), html.Label('Trend: ', style = {'color':'#0668a1'}), 
                                html.Div([dbc.Container(
              [
                  dbc.RadioItems(
                      options=[
                          {"label":"TOAR", "value":"Cooper"},
                          {"label": "EMD", "value": "EMD"},
                          {"label":"EEMD", "value":"EEMD"},
                          {"label": "Lamsal", "value": "Lamsal"},
                          {"label": "Linear", "value": "Linear"},
                          {"label": "STL", "value":"STL"},
                          {"label": "ThielSen", "value":"ThielSen"},
                          
                      ],
                      id="radio_trend",
                      labelClassName="date-group-labels",
                      labelCheckedClassName="date-group-labels-checked",
                      className="date-group-items",
                      inline=True,
                      value="Lamsal"
                  ),
              ],
              className="p-3",
          )
              ], style={'display':'inline-block'}),
                          html.Div([
                          html.Label('Height: ', style={'color':'#0668a1'}),html.Div([dbc.Container(
              [
                  dbc.RadioItems(
                      options=[
                          {"label": "1 [km]", "value": 1},
                          {"label": "6 [km]", "value": 6},
                          {"label": "15 [km]", "value": 15}
                          
                      ],
                      id="radio_height",
                      labelClassName="date-group-labels",
                      labelCheckedClassName="date-group-labels-checked",
                      className="date-group-items",
                      inline=True,
                      value=1
                  ),
              ],
              className="p-3",
          )
              ], style={'display':'inline-block'}), dcc.Graph(id='Trend')
                      ])          
                      ],  style={'margin-left':'100px','width':'525px','height':'400px', 'display': 'inline-block'})
                      ]),
                  dbc.Col([
                      html.Div([ 
                      html.H1('Air Parcel Trajectory', style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}),
                      html.Div(
                          [html.Label('Date:', style={'color':'#0668a1','display': 'inline-block', 'margin-left':'6%'}),
                          html.Div([
                          html.Div([
                          dcc.Dropdown(id='dropdown_years_eng_2',style={'margin-top':'10px'}, options=[{'label':year,'value':year} for year in dates_years], placeholder="Year",value='1997')
                          ], style={'width': '33%','margin-left_2':'5px', 'display': 'inline-block'}),
                          html.Div([
                          dcc.Dropdown(id='dropdown_months_eng_2', placeholder="Month",value = '3')
                          ], style={'width': '33%','margin-top':'10px', 'display': 'inline-block'}),
                          html.Div([
                          dcc.Dropdown(id='dropdown_days_eng_2', placeholder="Day",value='7')
                          ], style={'width': '33%','margin-top':'10px', 'display': 'inline-block'})
                          ], style={'display': 'inline-block'})
                          ], style= {'width': '80%','display':'inline-block', 'margin-left':'0%', 'margin-top':'-13px'}),
                      html.Div([
                          html.Label('Trajectory:', style={'color':'#0668a1','display': 'inline-block', 'margin-left':'6%'}),
                          html.Div([dbc.Container(
              [
                  dbc.RadioItems(
                      options=[
                          {"label":"Horizontal", "value":"Horizontal"},
                          {"label": "Vertical", "value": "Vertical"},
                          
                          
                      ],
                      id="radio_traject",
                      labelClassName="date-group-labels",
                      labelCheckedClassName="date-group-labels-checked",
                      className="date-group-items",
                      inline=True,
                      value="Horizontal"
                  ),
              ],
              className="p-3",
          )
              ], style={'display':'inline-block'})
                          ]),
                      dcc.Graph(id='trayectory')
                      ], style={'margin-left':'5px','margin-top':'20px','width':'525px','height':'400px', 'display': 'inline-block'})
                      ])
                  ])
              
              ], style={'backgroundColor':'#f6f6f6'})]
        if Switch_Lang==True:
            return [html.Div([
                dbc.Row([dbc.Col(html.H1("Perfiles Verticales", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1'}))]),
                
                dbc.Row([
                    dbc.Col([
                        html.Label('Fecha:', style={'color':'#0668a1','display': 'inline-block', 'margin-left':'15%'}),
                              html.Div(
                                  [
                                      html.Div([
                                  dcc.Dropdown(id='dropdown_years_esp',style={'margin-top':'10px'}, options=[{'label':year,'value':year} for year in dates_years], placeholder="Año",value='1997')
                                  ], style={'width': '20%','margin-left':'5px', 'display': 'inline-block'}),
                                  html.Div([
                                  dcc.Dropdown(id='dropdown_months_esp', placeholder="Mes",value = '3')
                                  ], style={'width': '20%','margin-top':'10px', 'display': 'inline-block'}),
                                  html.Div([
                                  dcc.Dropdown(id='dropdown_days_esp', placeholder="Dia",value='7')
                                  ], style={'width': '20%','margin-top':'10px', 'display': 'inline-block'})
                                  
                                      
                                  ], style= {'width': '50%','display':'inline-block', 'margin-left':'0%', 'margin-top':'-13px'})
                        ])
                    ]),
          dbc.Row([
              dbc.Col([
                  dcc.Graph(id='Perfil_vertical_graf', figure={"layout":{"height":400, "width":1080}}, style={'margin-left':'10vw'})
               
                                ], xs=10, sm=10, md=10, lg=10, xl=10)]),
          
          dbc.Row([
              dbc.Col([
                  html.Div([
                      html.H1("Climatología", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}),
                      html.Div([ html.Label('Fechas:', style={'color':'#0668a1','font-size':'18px', 'backgroundColor':'#f6f6f6'}),
                                dcc.DatePickerRange(
                      id='calendario_1',
                     start_date=date(1997, 5, 3),
                     end_date=date(2014,5,3)
                      )], style={'margin-left':'50px'}),
                      html.Div([
                          html.Label('Variable:', style={'margin-right':'5px','color': '#0668a1','font-size':'18px'}), 
                                html.Div([dbc.Container(
                              [dbc.RadioItems(
                                  options=[
                      {"label": "Ozone", "value": "O3_ppbv"},
                      {"label": "Temperature", "value": "Temp"},
                      {"label": "Mixing Ratio", "value": "Mixing_Ratio"},
                      {"label": "HR", "value": "RH"},
                      {"label": "U", "value": "U"},
                      {"label": "V", "value": "V"}
                      
                  ],
                  id="radio_Climatologia",
                  labelClassName="date-group-labels",
                  labelCheckedClassName="date-group-labels-checked",
                  className="date-group-items",
                  inline=True,
                  value="O3_ppbv"
              ),
          ],
          className="p-3",
          )], style={'display':'inline-block'})
              ],  style={'display':'inline-block', 'margin-left':'20px'}),
                      dcc.Graph(id="Climatologia")], style={'margin-left':'100px','margin-top':'20px','width':'525px','height':'650px', 'display': 'inline-block'})
                  ])
             ,
              dbc.Col([
                  html.Div([
                  html.H1("Perfiles de Ozono Animados", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'})
              ,dcc.Graph(figure= AnimESP(ozonosondes_data, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA,
                                         ozonosondes_climatology_90, ozonosondes_climatology_70,
                         ozonosondes_climatology_30, ozonosondes_climatology_10, 
                         ozonosondes_climatology_mean))
              ], style={'margin-left':'5px','width':'525px','height':'650px', 'display': 'inline-block'})
                  ])
              ]),
          
          dbc.Row([
              dbc.Col([
                  html.Div([html.H1('Tendencia', style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}), html.Label('Trend: ', style = {'color':'#0668a1'}), 
                            html.Div([dbc.Container(
          [
              dbc.RadioItems(
                  options=[
                      {"label":"TOAR", "value":"Cooper"},
                      {"label": "EMD", "value": "EMD"},
                      {"label":"EEMD", "value":"EEMD"},
                      {"label": "Lamsal", "value": "Lamsal"},
                      {"label": "Linear", "value": "Linear"},
                      {"label": "STL", "value":"STL"},
                      {"label": "ThielSen", "value":"ThielSen"},
                      
                  ],
                  id="radio_tendencia",
                  labelClassName="date-group-labels",
                  labelCheckedClassName="date-group-labels-checked",
                  className="date-group-items",
                  inline=True,
                  value="Lamsal"
              ),
          ],
          className="p-3",
      )
          ], style={'display':'inline-block'}),
                      html.Div([
                      html.Label('Altura: ', style={'color':'#0668a1'}),html.Div([dbc.Container(
          [
              dbc.RadioItems(
                  options=[
                      {"label": "1 [km]", "value": 1},
                      {"label": "6 [km]", "value": 6},
                      {"label": "15 [km]", "value": 15}
                      
                  ],
                  id="radio_altura",
                  labelClassName="date-group-labels",
                  labelCheckedClassName="date-group-labels-checked",
                  className="date-group-items",
                  inline=True,
                  value=1
              ),
          ],
          className="p-3",
      )
          ], style={'display':'inline-block'}), dcc.Graph(id='Tendencia')
                  ])          
                  ],  style={'margin-left':'100px','width':'525px','height':'400px', 'display': 'inline-block'})
                  ]),
              dbc.Col([
                      html.Div([ 
                      html.H1('Trayectoria Parcela de Aire', style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}),
                      html.Div(
                          [html.Label('Fecha:', style={'color':'#0668a1','display': 'inline-block', 'margin-left':'6%'}),
                          html.Div([
                          html.Div([
                          dcc.Dropdown(id='dropdown_years_esp_2',style={'margin-top':'10px'}, options=[{'label':year,'value':year} for year in dates_years], placeholder="Year",value='1997')
                          ], style={'width': '33%','margin-left_2':'5px', 'display': 'inline-block'}),
                          html.Div([
                          dcc.Dropdown(id='dropdown_months_esp_2', placeholder="Month",value = '3')
                          ], style={'width': '33%','margin-top':'10px', 'display': 'inline-block'}),
                          html.Div([
                          dcc.Dropdown(id='dropdown_days_esp_2', placeholder="Day",value='7')
                          ], style={'width': '33%','margin-top':'10px', 'display': 'inline-block'})
                          ], style={'display': 'inline-block'})
                          ], style= {'width': '80%','display':'inline-block', 'margin-left':'0%', 'margin-top':'-13px'}),
                      html.Div([
                          html.Label('Trayectoria:', style={'color':'#0668a1','display': 'inline-block', 'margin-left':'6%'}),
                          html.Div([dbc.Container(
              [
                  dbc.RadioItems(
                      options=[
                          {"label":"Horizontal", "value":"Horizontal"},
                          {"label": "Vertical", "value": "Vertical"},
                          
                          
                      ],
                      id="radio_traject_esp",
                      labelClassName="date-group-labels",
                      labelCheckedClassName="date-group-labels-checked",
                      className="date-group-items",
                      inline=True,
                      value="Horizontal"
                  ),
              ],
              className="p-3",
          )
              ], style={'display':'inline-block'})
                          ]),
                      dcc.Graph(id='trayectoria')
                      ], style={'margin-left':'5px','margin-top':'20px','width':'525px','height':'400px', 'display': 'inline-block'})
                      ])
              ])
          
          ], style={'backgroundColor':'#f6f6f6'})]
    elif tab == 'tab-3':
        if Switch_Lang== False:
            return dbc.Row([dbc.Col([html.H1("Download data", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'})
                ,html.Div([dcc.Markdown(dedent(f'''
                               CITATION – If you use this dataset please acknowledge the Chilean Weather Office, and cite L. Gallardo, A. Henríquez, A. M. Thompson, R. Rondanelli, J. Carrasco, A. Orfanoz-Cheuquelaf and P. Velásquez, The first twenty years (1994-2014) of Ozone soundings from Rapa Nui (27°S, 109°W, 51m a.s.l.), Tellus B, 2016. (DOI: 10.3402/tellusb.v68.29484)                    
                                                   ''')),
               dbc.Table.from_dataframe(df_table, striped=True, bordered=True, hover=True)
            ], style={'padding':'100px', 'padding-top':'0px'})], xs=12, sm=12, md=12, lg=12, xl=12)])
        elif Switch_Lang==True:
            return dbc.Row([dbc.Col([html.H1("Descargar datos", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'})
                ,html.Div([
                dcc.Markdown(dedent(f'''
                CITATION – If you use this dataset please acknowledge the Chilean Weather Office, and cite L. Gallardo, A. Henríquez, A. M. Thompson, R. Rondanelli, J. Carrasco, A. Orfanoz-Cheuquelaf and P. Velásquez, The first twenty years (1994-2014) of Ozone soundings from Rapa Nui (27°S, 109°W, 51m a.s.l.), Tellus B, 2016. (DOI: 10.3402/tellusb.v68.29484)                                   
                                                   '''))
                ,
                dbc.Table.from_dataframe(df_table, striped=True, bordered=True, hover=True)
                ], style={'padding':'100px', 'padding-top':'0px'})], xs=12, sm=12, md=12, lg=12, xl=12)])
    elif tab == 'tab-4':
         if Switch_Lang==False:
             return [html.Div([
                 
                 dbc.Row([dbc.Col([html.H1("Data", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),

                dcc.Markdown(dedent(f''' 
                         The data shown in this platform corresponds to the set collected between August 1994 and 2019 by DMC consists of 294 soundings. These soundings provide information 
                         on ozone, air pressure, temperature, dew point, and relative humidity from the surface to the lower stratosphere (30-35 km). Since 1999, wind speed and direction were added 
                         to the collection. These data are available at World Ozone and Ultraviolet Radiation Data Centre (WOUDC, http://www.woudc.org/).
                         
                         The O3 sensor used is the so-called Electrochemical Concentration Cell (ECC). The measuring principle is based on the titration of ozone in a potassium iodide (KI) sensing 
                         solution. A Science Pump Corporation (SPC) type of ECC ozonesonde instrument is used at Rapa Nui. The sensing solution KI strength is 1%, with 100% buffer. The ECC sonde is 
                         launched with a Väisälä RS92 radiosonde. Between 1995 and 1997, an OS815N sensor was used, thereafter, a CCE64B was utilized.             '''), 
                 
                 style={'margin-left':'6%'}) ,
                 
                 html.H1("Quality assurance and quality control", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                              

                dcc.Markdown(dedent(f''' 
                                    We carried out a careful visual inspection of all soundings available. Each sounding was reviewed trying to identify anomalous values, instrument malfunctioning, 
                                    etc. We used concurrent standard meteorological soundings to support the inspection of ozone soundings. We only excluded soundings that seemed to us evidently anomalous. 
                                    The number of analyzed and selected soundings per year and season are shown in Table 1. Once the cleansing and review process was completed, we linearly interpolated all soundings every 100 m. 
                                    A few soundings (5) were only available for mandatory pressure levels in 2012.                '''), 
                 
                 style={'margin-left':'6%'}) ,


                 html.H1("Back trajectories", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                              
 #                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
                dcc.Markdown(dedent(f'''
                 We use reanalysis data sets from National Centers for Environmental Prediction/Atmospheric Research (NCEP/NCAR) to characterize the large-scale meteorological features affecting Rapa Nui. 
                 We use three-dimensional (3-D) wind fields every six hours to calculate seven-day back trajectories for each ozone sonde.Trajectories were initialized at sounding launch time for 3 initial heights, 4, 8 and 12 km 
                 above mean sea level. For this purpose, we apply the Hybrid Single Particle Lagrangian Integrated Trajectory (HYSPLIT) model.                 '''), 
                 
                 style={'margin-left':'6%'}) ,
                                         
                             
             ], style={'display':'inline-block', 'margin-top':'50px'}, md=10, lg={'size': 6,  "offset": 0, 'order': 0})
                 ,
                     dbc.Col([
                         html.Div([html.H1("Trends", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                                      
         #                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
                        dcc.Markdown(dedent(f'''
                         Trends were calculated using several methods found in the literature. These methods are summarized below:

                                                            
                         **STL:**
                         This method  (Cleveland et al. 1990) of decomposing signals uses Loess techniques to generate local smoother functions. Then by decoupling the seasonality and separating the noise obtaining a monotonic function for the trend. Cleveland et al. 1990 
                        
                         **EMD**
                         In this method (Huang et al. 1998), the signal is decomposed as a superposition of local sums of oscillatory components called Intrinsic Mode Functions (IMF). The IMF modes added to a function without oscillatory components reconstruct the original signal. 
                         
                         **Lamsal-Fourier:**
                         This method (Lamsal et al. 2015) uses a multilinear regression model based on harmonic functions (Fourier regression) to determine the components in the linear trends.                

                         **Thiel Sen:**
                         In the Theil-Sen method (Theil 1992, Sen 1960), multiple slopes are calculated to select the final slope as the median of all these
                         '''), 
                         
                         style={'margin-left':'6%'}),
                                                    
     html.H1("Paper Rapa Nui", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
     dcc.Markdown(dedent(f'''

     Calderón, J. and Fuenzalida, H. 2014. Radiación ultravioleta en Isla de Pascua: factores climáticos y ozono total. Stratus 2, 8. Revista de la Dirección Meteorológica de Chile. ISSN 0719-4544

     Gallardo, L., Henríquez, A., Thompson, A. M., Rondanelli, R., Carrasco, J., Orfanoz-Cheuquelaf, A., et al. (2016). The first twenty years (1994-2014) of ozone soundings from Rapa Nui (27°S, 109°W, 51m a.s.l.). Tellus, Ser. B Chem. Phys. Meteorol. 68, 29484. doi:10.3402/tellusb.v68.29484.
     
     '''), style={'margin-left':'6%'}),                        
     html.H1("Papers using/analyzing Rapa Nui data", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
     dcc.Markdown(dedent(f'''
     Anet, G. J., Steinbacher, M., Gallardo, L., Velásquez Álvarez, A. P., Emmenegger, L., and Buchmann, B. (2017). Surface ozone in the Southern Hemisphere: 20 years of data from a site with a unique setting in El Tololo, Chile. Atmos. Chem. Phys. 17, 6477–6492. doi:10.5194/acp-17-6477-2017.
     
     Gallardo, L., Carrasco, J., and Olivares, G. (2000). An analysis of ozone measurements at Cerro Tololo (30°S, 70°W, 2200 m.a.s.l.) in Chile. Tellus, Ser. B Chem. Phys. Meteorol. 52, 50–59. doi:10.3402/tellusb.v52i1.16081.
     
     
     Kalthoff, N., Bischoff-Gauß, I., Fiebig-Wittmaack, M., Fiedler, F., Thürauf, J., Novoa, E., et al. (2002). Mesoscale wind regimes in Chile at 30°S. J. Appl. Meteorol. 41, 953–970. doi:10.1175/1520-0450(2002)041<0953:MWRICA>2.0.CO;2.
     
     Rondanelli, R., Gallardo, L., and Garreaud, R. D. (2002). Rapid changes in ozone mixing ratios at Cerro Tololo (30°10′S, 70°48′W, 2200 m) in connection with cutoff lows and deep troughs. J. Geophys. Res. Atmos. 107, ACL 6-1-ACL 6-15. doi:10.1029/2001JD001334. 
     
    '''), style={'margin-left':'6%'}) ,
     html.H1("Papers on trend calculations", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
     dcc.Markdown(dedent(f'''
     Cleveland, R., Cleveland, W., of official, J.M.J., undefined 1990,
     1990. STL: A seasonal-trend decomposition. nniiem.ru URL: http:
     //www.nniiem.ru/file/news/2016/stl-statistical-model.pdf .
                         
     Huang, N.E., Shen, Z., Long, S.R., Wu, M.C., Snin, H.H., Zheng, Q., Yen, N.C., Tung, C.C., Liu, H.H., 1998. The empirical mode decom- position and the Hubert spectrum for nonlinear and non-stationary time series analysis. Proceedings of the Royal Society A: Mathemat- ical, Physical and Engineering Sciences 454, 903–995. doi: 10.1098/rspa.1998.0193 .
                     
     Lamsal, L.N., Duncan, B.N., Yoshida, Y., Krotkov, N.A., Pickering,K.E., Streets, D.G., Lu, Z., 2015. U.S. NO2 trends (2005–2013): EPA Air Quality System (AQS) data versus improved observations from the Ozone Monitoring Instrument (OMI). Atmospheric Environment 110, 130–143. URL: http://linkinghub.elsevier.com/re
     
     Sen, P.K., 1960. On Some Convergence Properties of U-Statistics. Calcutta Statistical Association Bulletin 10, 1–18. URL:https://journals.sagepub.com/doi/abs/10.1177/00
     
    '''), style={'margin-left':'6%'})
     ], style={'margin-top':'50px','display':'inline-block'})
                         ], md=10, lg={'size': 6,  "offset": 0, 'order': 1})
                     ])
                         ])
                                     
                                     ]
         if Switch_Lang==True:
               return  [html.Div([
                   
                   dbc.Row([dbc.Col([html.H1("Datos", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),

                  dcc.Markdown(dedent(f''' 
                           Los datos mostrados en esta plataforma corresponden al conjunto recolectado entre agosto de 1994 y 2019 por DMC compuesto por 294 sondeos de O3. Estos sondeos proporcionan información
                           sobre el ozono, la presión del aire, la temperatura, el punto de rocío y la humedad relativa desde la superficie hasta la estratosfera inferior (30-35 km). Desde 1999, se agregaron la velocidad y la dirección del viento
                           a la colección. Estos datos están disponibles en el Centro mundial de datos sobre el ozono y la radiación ultravioleta (WOUDC, http://www.woudc.org/).
                           
                           El sensor de O3 utilizado es la llamada celda de concentración electroquímica (ECC). El principio de medición se basa en la valoración del ozono en un sensor de yoduro de potasio (KI)
                           solución. En Rapa Nui se utiliza un instrumento de sonda de ozono ECC de Science Pump Corporation (SPC). La concentración de KI de la solución de detección es del 1%, con tampón al 100%. La sonda ECC es
                           lanzado con una radiosonda Väisälä RS92. Entre 1995 y 1997, se utilizó un sensor OS815N, a partir de entonces, se utilizó un CCE64B. '''), 
                   
                   style={'margin-left':'6%'}) ,
                   
                   html.H1("Control de calidad de datos", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                                

                  dcc.Markdown(dedent(f''' 
                                      Nosotros realizamos una cuidadosa inspección visual de todos los sondeos disponibles. Cada sondeo fue revisado tratando de identificar valores anómalos, mal funcionamiento del instrumento,
                                      etc. Usamos sondeos meteorológicos estándar concurrentes para apoyar la inspección de sondeos de ozono. Solo excluimos los sondeos que nos parecían evidentemente anómalos.
                                      El número de sondeos analizados y seleccionados por año y temporada se muestra en la Tabla 1. Una vez que se completó el proceso de limpieza y revisión, interpolamos linealmente todos los sondeos cada 100 m.
                                      Algunos sondeos (5) solo estaban disponibles para niveles de presión obligatorios en 2012.             '''), 
                   
                   style={'margin-left':'6%'}) ,


                   html.H1("Seguimiento de trajectorias", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                                
   #                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
                  dcc.Markdown(dedent(f'''
                   Utilizamos conjuntos de datos de reanálisis de los Centros Nacionales de Predicción Ambiental / Investigación Atmosférica (NCEP / NCAR) para caracterizar las características meteorológicas a gran escala que afectan a Rapa Nui.
                    Usamos campos de viento tridimensionales (3-D) cada seis horas para calcular las trayectorias de retroceso de siete días para cada sonda de ozono. Las trayectorias se inicializaron en el momento del lanzamiento del sondeo para 3 alturas iniciales, 4, 8 y 12 km.
                    sobre el nivel medio del mar. Para ello, aplicamos el modelo de Trayectoria Integrada Lagrangiana Híbrida de Partícula Única (HYSPLIT, por su sigla en ingles). '''), 
                   
                   style={'margin-left':'6%'}) ,
                                           
                               
               ], style={'display':'inline-block', 'margin-top':'50px'}, md=10, lg={'size': 6,  "offset": 0, 'order': 0})
                   ,
                       dbc.Col([
                           html.Div([html.H1("Tendencias", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                                        
           #                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
                          dcc.Markdown(dedent(f'''
                           Las tendencias se calcularon utilizando varios métodos encontrados en la literatura. Estos métodos se resumen a continuación.
                           
                           
                           **Seasonal and Trend decomposition using Loess (STL):**
                           Este método (def en Cleveland et al. 1990) para descomponer señales, usa las técnicas de Loess con el fin de generar funciones smoother locales. Con esto desacopla la estacionalidad (Yt) y separa el ruido (Rt) obteniendo una función monótona para la tendencia (Tt).
                           
                           
                           **Empirical Mode Decomposition (EMD):**
                           EMD (Huang et al. 1998) es un método para analizar datos no lineales y no estacionarios. En este método, los datos o la señal se descomponen como una superposición de sumas locales de componentes oscilatorios denominados Funciones de modo intrínseco (IMF). Los modos IMF sumados a una función sin componentes oscilatorios  reconstruyen la señal original. 
                           
                           **Lamsal-Fourier:**
                           Lamsal et al. 2015 utiliza un modelo de regresión multilineal basado en funciones armónicas para determinar los componentes en las tendencias lineales. La señal de frecuencia mensual es calculada como la suma de tres subcomponentes. Un regresión de fourier (α) de n componentes armonicas, un ruido (R) y una componente constante (β) multiplicada por el tiempo, esta ultima la tendencia de la señal.
                                           
                           '''), 
                           
                           style={'margin-left':'6%'}),
                                                      
       html.H1("Artículos Rapa Nui", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
       dcc.Markdown(dedent(f'''

       Calderón, J. and Fuenzalida, H. 2014. Radiación ultravioleta en Isla de Pascua: factores climáticos y ozono total. Stratus 2, 8. Revista de la Dirección Meteorológica de Chile. ISSN 0719-4544

       Gallardo, L., Henríquez, A., Thompson, A. M., Rondanelli, R., Carrasco, J., Orfanoz-Cheuquelaf, A., et al. (2016). The first twenty years (1994-2014) of ozone soundings from Rapa Nui (27°S, 109°W, 51m a.s.l.). Tellus, Ser. B Chem. Phys. Meteorol. 68, 29484. doi:10.3402/tellusb.v68.29484.
       
       
      '''), style={'margin-left':'6%'}),                        
       html.H1("Artículos Tendencia", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
       dcc.Markdown(dedent(f'''
       Anet, G. J., Steinbacher, M., Gallardo, L., Velásquez Álvarez, A. P., Emmenegger, L., and Buchmann, B. (2017). Surface ozone in the Southern Hemisphere: 20 years of data from a site with a unique setting in El Tololo, Chile. Atmos. Chem. Phys. 17, 6477–6492. doi:10.5194/acp-17-6477-2017.
       
       Gallardo, L., Carrasco, J., and Olivares, G. (2000). An analysis of ozone measurements at Cerro Tololo (30°S, 70°W, 2200 m.a.s.l.) in Chile. Tellus, Ser. B Chem. Phys. Meteorol. 52, 50–59. doi:10.3402/tellusb.v52i1.16081.
       
       
       Kalthoff, N., Bischoff-Gauß, I., Fiebig-Wittmaack, M., Fiedler, F., Thürauf, J., Novoa, E., et al. (2002). Mesoscale wind regimes in Chile at 30°S. J. Appl. Meteorol. 41, 953–970. doi:10.1175/1520-0450(2002)041<0953:MWRICA>2.0.CO;2.
       
       Rondanelli, R., Gallardo, L., and Garreaud, R. D. (2002). Rapid changes in ozone mixing ratios at Cerro Tololo (30°10′S, 70°48′W, 2200 m) in connection with cutoff lows and deep troughs. J. Geophys. Res. Atmos. 107, ACL 6-1-ACL 6-15. doi:10.1029/2001JD001334. 
       
      '''), style={'margin-left':'6%'}) ,
       html.H1("Artículos sobre cálculos de tendencia", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
       dcc.Markdown(dedent(f'''
       Cleveland, R., Cleveland, W., of official, J.M.J., undefined 1990,
       1990. STL: A seasonal-trend decomposition. nniiem.ru URL: http:
       //www.nniiem.ru/file/news/2016/stl-statistical-model.pdf .
                           
       Huang, N.E., Shen, Z., Long, S.R., Wu, M.C., Snin, H.H., Zheng, Q., Yen, N.C., Tung, C.C., Liu, H.H., 1998. The empirical mode decom- position and the Hubert spectrum for nonlinear and non-stationary time series analysis. Proceedings of the Royal Society A: Mathemat- ical, Physical and Engineering Sciences 454, 903–995. doi: 10.1098/rspa.1998.0193 .
                       
       Lamsal, L.N., Duncan, B.N., Yoshida, Y., Krotkov, N.A., Pickering,K.E., Streets, D.G., Lu, Z., 2015. U.S. NO2 trends (2005–2013): EPA Air Quality System (AQS) data versus improved observations from the Ozone Monitoring Instrument (OMI). Atmospheric Environment 110, 130–143. URL: http://linkinghub.elsevier.com/re
       
       Sen, P.K., 1960. On Some Convergence Properties of U-Statistics. Calcutta Statistical Association Bulletin 10, 1–18. URL:https://journals.sagepub.com/doi/abs/10.1177/00
       
      '''), style={'margin-left':'6%'})
       ], style={'margin-top':'50px','display':'inline-block'})
                           ], md=10, lg={'size': 6,  "offset": 0, 'order': 1})
                       ])
                           ])
                                       
                                       ]                                   
    
app.layout = html.Div(
    [navbar,
     content]
)


################################# dropdown dinamicos##########################
@app.callback(
    dash.dependencies.Output('dropdown_months_eng', 'options'),
    [dash.dependencies.Input('dropdown_years_eng', 'value')]
)
def update_date_dropdown(year):
    return [{'label': i, 'value': i} for i in list(dates[year].keys())]

@app.callback(
    dash.dependencies.Output('dropdown_days_eng', 'options'),
    [dash.dependencies.Input('dropdown_years_eng', 'value'),
     dash.dependencies.Input('dropdown_months_eng', 'value')]
)
def update_date_dropdown3(dropdown_years_eng, dropdown_months_eng):
    return [{'label': i, 'value': i} for i in dates[dropdown_years_eng][dropdown_months_eng]]

###############################################################################

#################################dynamic dropdown##########################
@app.callback(
    dash.dependencies.Output('dropdown_months_esp', 'options'),
    [dash.dependencies.Input('dropdown_years_esp', 'value')]
)
def update_date_dropdown(year):
    return [{'label': i, 'value': i} for i in list(dates[year].keys())]

@app.callback(
    dash.dependencies.Output('dropdown_days_esp', 'options'),
    [dash.dependencies.Input('dropdown_years_esp', 'value'),
     dash.dependencies.Input('dropdown_months_esp', 'value')]
)
def update_date_dropdown3(dropdown_years_esp, dropdown_months_esp):
    return [{'label': i, 'value': i} for i in dates[dropdown_years_esp][dropdown_months_esp]]


################################# dropdown dinamicos##########################
@app.callback(
    dash.dependencies.Output('dropdown_months_eng_2', 'options'),
    [dash.dependencies.Input('dropdown_years_eng_2', 'value')]
)
def update_date_dropdown(year):
    return [{'label': i, 'value': i} for i in list(dates[year].keys())]

@app.callback(
    dash.dependencies.Output('dropdown_days_eng_2', 'options'),
    [dash.dependencies.Input('dropdown_years_eng_2', 'value'),
     dash.dependencies.Input('dropdown_months_eng_2', 'value')]
)
def update_date_dropdown3(dropdown_years_eng_2, dropdown_months_eng_2):
    return [{'label': i, 'value': i} for i in dates[dropdown_years_eng_2][dropdown_months_eng_2]]

###############################################################################

#################################dynamic dropdown##########################
@app.callback(
    dash.dependencies.Output('dropdown_months_esp_2', 'options'),
    [dash.dependencies.Input('dropdown_years_esp_2', 'value')]
)
def update_date_dropdown(year):
    return [{'label': i, 'value': i} for i in list(dates[year].keys())]

@app.callback(
    dash.dependencies.Output('dropdown_days_esp_2', 'options'),
    [dash.dependencies.Input('dropdown_years_esp_2', 'value'),
     dash.dependencies.Input('dropdown_months_esp_2', 'value')]
)
def update_date_dropdown3(dropdown_years_esp_2, dropdown_months_esp_2):
    return [{'label': i, 'value': i} for i in dates[dropdown_years_esp_2][dropdown_months_esp_2]]

###############################################################################

############################ Vertical Profiles ###############################
@app.callback(
    Output('Vertical_profile_graph', 'figure'),
    [Input('dropdown_years_eng', 'value'),
     Input('dropdown_months_eng', 'value'),
     Input('dropdown_days_eng', 'value')
     ]
    
    )
def update_graph(dropdown_years_eng, dropdown_months_eng, dropdown_days_eng):
    fig = vertical_profiles(dropdown_years_eng, dropdown_months_eng, dropdown_days_eng,
                      ozonosondes_climatology_90, ozonosondes_climatology_70,
                       ozonosondes_climatology_30, ozonosondes_climatology_10, 
                       ozonosondes_climatology_mean, ozonosondes_data)   
    return fig 

############################ Perfiles Verticales###############################
@app.callback(
    Output('Perfil_vertical_graf', 'figure'),
    [Input('dropdown_years_esp', 'value'),
     Input('dropdown_months_esp', 'value'),
     Input('dropdown_days_esp', 'value')
     ]
    
    )
def update_graph(dropdown_years_esp, dropdown_months_esp, dropdown_days_esp):
    fig = periles_verticales(dropdown_years_esp, dropdown_months_esp, dropdown_days_esp,
                             ozonosondes_climatology_90, ozonosondes_climatology_70,
                       ozonosondes_climatology_30, ozonosondes_climatology_10, 
                       ozonosondes_climatology_mean, ozonosondes_data)  
   
    return fig
#######################################Climatologia###################### 
@app.callback(
    Output('Climatologia', 'figure'),
      [Input('calendario_1', 'start_date'),
      Input('calendario_1', 'end_date'),
      Input('radio_Climatologia', 'value')
      ])
def update_graph(start_date, end_date, radio_Climatologia):
 
    fig =  Climatologia(start_date, end_date, radio_Climatologia, ozonosondes_data, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA)
    return fig 


#######################################Climatologya###################### 
@app.callback(
    Output('Climatology', 'figure'),
      [Input('calendar_1', 'start_date'),
      Input('calendar_1', 'end_date'),
      Input('radio_Climatology','value')])
def update_graph(start_date, end_date, radio_Climatology):
 
    fig = Climatology(start_date, end_date, radio_Climatology, ozonosondes_data, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA)
    return fig
####################################Tendencia#################################
@app.callback(Output('Tendencia', 'figure'),
              Input('radio_tendencia', 'value'),
              Input('radio_altura', 'value'))
def update_graph(radio_tendencia, radio_altura):
        fig = tendencia(radio_tendencia, radio_altura, ozonosondes_data)
        return fig
    
#################################### Trend ##################################

@app.callback(Output('Trend', 'figure'),
              Input('radio_trend', 'value'),
              Input('radio_height', 'value'))
def update_graph(radio_trend, radio_height):
        fig = trend(radio_trend, radio_height, ozonosondes_data)
        return fig
    

####################################### Trajectory ##########################

@app.callback(
    Output('trayectory', 'figure'),
    [Input('dropdown_years_eng_2', 'value'),
     Input('dropdown_months_eng_2', 'value'),
     Input('dropdown_days_eng_2', 'value'),
     Input('radio_traject', 'value')
     ])
def update_graph(dropdown_years_eng_2, dropdown_months_eng_2, dropdown_days_eng_2, radio_traject):
    fig = Trayectory(df_trayect,int(dropdown_years_eng_2), int(dropdown_months_eng_2), int(dropdown_days_eng_2), radio_traject)
    return fig
####################################### Trayectoria ##########################

@app.callback(
    Output('trayectoria', 'figure'),
    [Input('dropdown_years_esp_2', 'value'),
     Input('dropdown_months_esp_2', 'value'),
     Input('dropdown_days_esp_2', 'value'),
     Input('radio_traject_esp', 'value')
     ])
def update_graph(dropdown_years_esp_2, dropdown_months_esp_2, dropdown_days_esp_2, radio_traject_esp):
    fig = Trayectoria(df_trayect,int(dropdown_years_esp_2), int(dropdown_months_esp_2), int(dropdown_days_esp_2), radio_traject_esp)
    return fig
if __name__ == '__main__':
    app.run_server(debug=True, port=8888)