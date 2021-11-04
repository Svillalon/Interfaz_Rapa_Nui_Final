# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 21:05:58 2021

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

def tendencia(radio_tendencia, radio_altura, ozonosondes_data):
    df_m = ozonosondes_data[ozonosondes_data.Alt==radio_altura].loc['1995':'2020']
    df_m = df_m.fillna(df_m.mean()) 
    s    = df_m.O3_ppbv.values 
    s_df = df_m.O3_ppbv
    s_df = s_df.resample('M').mean().fillna(s_df.mean())
    if radio_altura ==1:
    	scale = [0,60]
    	text_y = 50
    elif radio_altura ==6:
        scale = [10,100]
        text_y = 90
    elif radio_altura ==15:
        scale = [40,420]
        text_y = 50 
    ###################
    if radio_tendencia == 'Lamsal':        
        model_trend =  lamsal_trend(s)
    elif radio_tendencia == 'Linear':
        model_trend = linear_trend(s)
    elif radio_tendencia == 'EMD':
        model_trend = emd_trend(s)    
    elif radio_tendencia == 'STL':
        model_trend = stl_trend(s_df)    
    elif radio_tendencia == 'ThielSen':
        model_trend = TheillSen_trend(s)
    elif radio_trends == 'Cooper':
    	model_trend = cooper_trend(s)
    elif radio_trends == 'EEMD':
    	model_trend = eemd_trend(s)     




    fig = go.Figure()       
    fig.add_trace(go.Scatter(
            x=df_m.index,
            y=df_m["O3_ppbv"],
            mode='markers',
            #text = aux_a    ,  
            marker={
                'size': 6,
                #'color': aux_b,
                'opacity': 0.5,
                'line': {'width': 0.9, 'color': 'black'}
            }
        ))
    fig.add_trace(go.Scatter( 
                x=df_m.index, 
                y=model_trend[0],
                mode='markers', 
                marker=dict(size= 6, color='black')
                ))

    fig.add_trace(go.Scatter( 
                    x=df_m.index[0:1], 
                    y= [scale[1],scale[1]] , #df_m[0:1]*2.0
                    mode='text', 
                    marker=dict(size= 6, color='black'),
                    text=["Tendencia Decadal= " + 			str(round(model_trend[1]*10*12,1)) + ' ± ' + 		str(round(tiao(model_trend[0], s)*10,2)) +'[ppbv]  		<br>Promedio= '+ str(round(df_m["O3_ppbv"].mean(),1)) + 		" [ppbv]" + "     n = " + str(df_m.O3_ppbv.count()) ]
                    
                    ,
                    textposition="top right",
                    textfont=dict(
                    family="Times New Roman",
                    size=14,
                    color="black")  #
                    ))
    fig.update_layout(
            showlegend = False,
            title_font_family="Times New Roman",
    #        title_font_color="red",        
            title_font_size=30,
#            yaxis=dict(
#                range=[0, 65]),
            margin=dict(t=0, b=0, l=0, r = 0),
            title_font_color = 'dimgray',
            plot_bgcolor='#f6f6f6',
            paper_bgcolor='#f6f6f6',
            titlefont=dict(size=14,color='black'),
            xaxis_title='Fecha',
            yaxis_title="O<sub>3</sub> [ppbv]") 
    return fig


def trend(radio_trend, radio_height, ozonosondes_data):
    df_m = ozonosondes_data[ozonosondes_data.Alt==radio_height].loc['1995':'2020']
    df_m = df_m.fillna(df_m.mean()) 
    s    = df_m.O3_ppbv.values 
    s_df = df_m.O3_ppbv
    s_df = s_df.resample('M').mean().fillna(s_df.mean())
    if radio_height ==1:
    	scale = [0,60]
    	text_y = 50
    elif radio_height ==6:
        scale = [10,100]
        text_y = 90
    elif radio_height ==15:
        scale = [40,420]
        text_y = 50    	 
    ###################
    if radio_trend == 'Lamsal':        
        model_trend =  lamsal_trend(s)
    elif radio_trend == 'Linear':
        model_trend = linear_trend(s)
    elif radio_trend == 'EMD':
        model_trend = emd_trend(s)    
    elif radio_trend == 'STL':
        model_trend = stl_trend(s_df)    
    elif radio_trend == 'ThielSen':
        model_trend = TheillSen_trend(s)




    fig = go.Figure()       
    fig.add_trace(go.Scatter(
            x=df_m.index,
            y=df_m["O3_ppbv"],
            mode='markers',
            #text = aux_a    ,  
            marker={
                'size': 6,
                #'color': aux_b,
                'opacity': 0.5,
                'line': {'width': 0.9, 'color': 'black'}
            }
        ))
    fig.add_trace(go.Scatter( 
                x=df_m.index, 
                y=model_trend[0],
                mode='markers', 
                marker=dict(size= 6, color='black')
                ))

    fig.add_trace(go.Scatter( 
                    x=df_m.index[0:1], 
                    y= [scale[1],scale[1]] , #df_m[0:1]*2.0
                    mode='text', 
                    marker=dict(size= 6, color='black'),
   		     text=["Decadal Trend = " + 			str(round(model_trend[1]*10*12,1)) + ' ± ' + 		str(round(tiao(model_trend[0], s)*10,2)) +'[ppbv]'   + ' 		<br>Mean= '+ str(round(df_m["O3_ppbv"].mean(),1)) + " [ppbv]" + "     n = " + str(df_m.O3_ppbv.count())],
                    textposition="top right",
                    textfont=dict(
                    family="Times New Roman",
                    size=14,
                    color="black")  #
                    ))
    fig.update_layout(
            showlegend = False,
            title_font_family="Times New Roman",
    #        title_font_color="red",        
            title_font_size=30,
 #           yaxis=dict(
 #               range=scale),
            margin=dict(t=0, b=0, l=0, r = 0),
            title_font_color = 'dimgray',
            plot_bgcolor='#f6f6f6',
            paper_bgcolor='#f6f6f6',
            titlefont=dict(size=14,color='black'),
            xaxis_title='Date',
            yaxis_title="O<sub>3</sub> [ppbv]") 
    return fig



