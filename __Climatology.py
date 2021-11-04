#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 19:35:40 2021

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

def Climatologia(start_date, end_date, radio_Climatologia, ozonosondes_data, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA):
    g =ozonosondes_data.loc[start_date:end_date]
    a = g.groupby([g.index.month, g.Alt]).mean()
    O3_mesh =np.transpose( [a[str(radio_Climatologia)][i][a[str(radio_Climatologia)][i].index[0:151]] for i in range (1,13)])

    Months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    xlabel = 'Mes'
    ylabel = 'Altura [km]'
    radio_Climatologia
    if radio_Climatologia == 'O3_ppbv':
        text= 'O<sub>3</sub> [mPa]'
    elif radio_Climatologia == 'Temp':
        text = 'Temperatura [K]'
    elif radio_Climatologia == 'RH':
        text = 'Humedad Relativa [%]'
    elif radio_Climatologia == 'U':
        text = 'Velocidad Zonal [m/s]'
    elif radio_Climatologia == 'V':
        text = 'Velocidad Meridional [m/s]'    
    elif radio_Climatologia == 'Mixing_Ratio':
        text = 'Mixing Ratio [gr/kg]'
    fig = go.Figure(data=(go.Contour(z=O3_mesh,
                                  #x = [i for i in range(24)],
                                 # y = [i for i in range(1,13)
                                  y =np.linspace(0,15,151),
                                  x = Months, 
                                  colorscale= 'jet',
                                  
                                  colorbar=dict(
            title=text, # title here
            titleside='right',
            titlefont=dict(
                size=14,
                family='Arial, sans-serif')), contours=dict(
            coloring ='heatmap',
            showlabels = True, # show labels on contours
            labelfont = dict( # label font properties
                size = 13,
                color = 'black')
            ))))

    fig.update_layout(
        width=525,
        height=400,
        autosize=False,
        margin=dict(t=25, b=0, l=0, r = 0),
        title_font_family="Times New Roman",
#        title_font_color="red",        
        title_font_size=30,
        title_font_color = 'dimgray',
        plot_bgcolor='#f6f6f6',
        paper_bgcolor='#f6f6f6',
        titlefont=dict(size=14,color='black'),
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        )
    # # Update 3D scene options
#     fig.update_scenes(
#         aspectratio=dict(x=1, y=1, z=0.7),
#         aspectmode="manual"
#         )

# Add drowdowns
# button_layer_1_height = 1.08

    fig.update_layout(
            images= [       dict(
                    source='data:image/png;base64,{}'.format(encoded_image_cr2_celeste),
                    xref="paper", yref="paper",
                    x=0.25, y=1.0,
                    sizex=0.2, sizey=0.2,
                    xanchor="right",
                    yanchor="bottom",
                    #sizing="stretch",
                    layer="above")    ,dict(
                    source='data:image/png;base64,{}'.format(encoded_image_DMC),
                    xref="paper", yref="paper",
                    x=0.58, y=1.05,
                    sizex=0.15, sizey=0.15,
                    xanchor="right",
                    yanchor="bottom",
                    #sizing="stretch",
                    layer="above"), dict(
                    source='data:image/png;base64,{}'.format(encoded_image_GWA),
                    xref="paper", yref="paper",
                    x=0.95, y=1.05,
                    sizex=0.17, sizey=0.17,
                    xanchor="right",
                    yanchor="bottom",
                    #sizing="stretch",
                    layer="above")])
    
    # update layout properties
    fig.update_layout(
        autosize=False,
        height=480,
        width=525,
        bargap=0.15,
        bargroupgap=0.1,
        barmode="stack",
        hovermode="x",
        margin=dict(t=100, b=10, l=10, r = 10),
    )
    
    return fig

def Climatology(start_date, end_date, radio_Climatology, ozonosondes_data, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA):
    
    g =ozonosondes_data.loc[start_date:end_date]
    a = g.groupby([g.index.month, g.Alt]).mean()
    O3_mesh =np.transpose( [a[str(radio_Climatology)][i][a[str(radio_Climatology)][i].index[0:151]] for i in range (1,13)])

    Months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    xlabel = 'Month'
    ylabel = 'Height [km]'
    if radio_Climatology == 'O3_ppbv':
        text= 'O<sub>3</sub> [mPa]'
    elif radio_Climatology == 'Temp':
        text = 'Temperature [K]'
    elif radio_Climatology == 'RH':
        text = 'Humedad Relativa [%]'
    elif radio_Climatology == 'U':
        text = 'Zonal Wind[m/s]'
    elif radio_Climatology == 'V':
        text = 'Meridional Wind [m/s]'    
    elif radio_Climatology == 'Mixing_Ratio':
        text = 'Mixing_Ratio [gr/kg]'
    fig = go.Figure(data=(go.Contour(z=O3_mesh,
                                  #x = [i for i in range(24)],
                                 # y = [i for i in range(1,13)
                                  y =np.linspace(0,15,151),
                                  x = Months, 
                                  colorscale= 'jet',
                                  
                                  colorbar=dict(
            title=text, # title here
            titleside='right',
            titlefont=dict(
                size=14,
                family='Arial, sans-serif')), contours=dict(
            coloring ='heatmap',
            showlabels = True, # show labels on contours
            labelfont = dict( # label font properties
                size = 13,
                color = 'black')
            ))))

    fig.update_layout(
        width=540,
        height=400,
        autosize=False,
        margin=dict(t=25, b=0, l=0, r = 0),
        title_font_family="Times New Roman",
#        title_font_color="red",        
        title_font_size=30,
        title_font_color = 'dimgray',
        plot_bgcolor='#f6f6f6',
        paper_bgcolor='#f6f6f6',
        titlefont=dict(size=14,color='black'),
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        )
    # # Update 3D scene options
#     fig.update_scenes(
#         aspectratio=dict(x=1, y=1, z=0.7),
#         aspectmode="manual"
#         )

# Add drowdowns
# button_layer_1_height = 1.08
    fig.update_layout(
            images= [       dict(
                    source='data:image/png;base64,{}'.format(encoded_image_cr2_celeste),
                    xref="paper", yref="paper",
                    x=0.25, y=1.0,
                    sizex=0.2, sizey=0.2,
                    xanchor="right",
                    yanchor="bottom",
                    #sizing="stretch",
                    layer="above")    ,dict(
                    source='data:image/png;base64,{}'.format(encoded_image_DMC),
                    xref="paper", yref="paper",
                    x=0.58, y=1.05,
                    sizex=0.15, sizey=0.15,
                    xanchor="right",
                    yanchor="bottom",
                    #sizing="stretch",
                    layer="above"), dict(
                    source='data:image/png;base64,{}'.format(encoded_image_GWA),
                    xref="paper", yref="paper",
                    x=0.95, y=1.05,
                    sizex=0.17, sizey=0.17,
                    xanchor="right",
                    yanchor="bottom",
                    #sizing="stretch",
                    layer="above")])
    
    # update layout properties
    fig.update_layout(
        autosize=False,
        height=480,
        width=540,
        bargap=0.15,
        bargroupgap=0.1,
        barmode="stack",
        hovermode="x",
        margin=dict(t=100, b=10, l=10, r = 10),
    )
    return fig
