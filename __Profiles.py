#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 17:34:01 2021

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

def periles_verticales(dropdown_years_esp, dropdown_months_esp, dropdown_days_esp, 
                       ozonosondes_climatology_90, ozonosondes_climatology_70,
                       ozonosondes_climatology_30, ozonosondes_climatology_10, 
                       ozonosondes_climatology_mean, ozonosondes_data):
    fig = make_subplots(rows=1, cols=3)
##################### O3 #####################################################         
    fig.add_trace(
        go.Scatter(
            name="90%",legendgroup='90%',
            x=ozonosondes_climatology_90.O3_mba,
            y=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Alt,
            marker=dict(color="#444"),
            line=dict(width=0),
             mode='lines',
            
        ),
        row=1, col=1
        )
    
    fig.add_trace(
        go.Scatter(
        x=ozonosondes_climatology_10.O3_mba,
        y=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Alt,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
         name="10%",legendgroup='10%')
        ,
        row=1, col=1
        )
    
    fig.add_trace(
        go.Scatter(
            name="30%",legendgroup='30%',
            x=ozonosondes_climatology_30.O3_mba,
            y=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Alt,
            marker=dict(color="#444"),
            line=dict(width=0),
             mode='lines',
            
        ),
        row=1, col=1
        )
    
    fig.add_trace(
        go.Scatter(
        name="70%",legendgroup='70%',
        x=ozonosondes_climatology_70.O3_mba,
        y=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Alt,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty')
        ,
        row=1, col=1
        )
    
    fig.add_trace(
        go.Scatter(x=ozonosondes_climatology_mean.O3_mba, y=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Alt
        ,showlegend=False, line_color='red',  name="Promedio",legendgroup='Promedio'),  
        row=1, col=1
        )
    fig.add_trace(
        go.Scatter(x=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].O3_mPa, y=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Alt
       ,line_color='blue', legendgroup='Sondeo' ,showlegend=False),  
        row=1, col=1
        )
################### temp #####################################################  
    fig.add_trace(
        go.Scatter(
            name="90%",legendgroup='90%',
            x=ozonosondes_climatology_90.Temp,
            y=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Alt,
            marker=dict(color="#444"),
            line=dict(width=0),
             mode='lines',
            showlegend=False
        ),
        row=1, col=2
        )
    
    fig.add_trace(
        go.Scatter(
        name="10%",legendgroup='10%',
        x=ozonosondes_climatology_10.Temp,
        y=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Alt,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
        showlegend=False)
        ,
        row=1, col=2
        )
    
    fig.add_trace(
        go.Scatter(
            name="30%",legendgroup='30%',
            x=ozonosondes_climatology_30.Temp,
            y=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Alt,
            marker=dict(color="#444"),
            line=dict(width=0),
             mode='lines',
            showlegend=False
        ),
        row=1, col=2
        )
    
    fig.add_trace(
        go.Scatter(
        name="70%",legendgroup='70%',
        x=ozonosondes_climatology_70.Temp,
        y=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Alt,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
        showlegend=False)
        ,
        row=1, col=2
        ) 
    fig.add_trace(
        go.Scatter(x=ozonosondes_climatology_mean.Temp, y=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Alt,
                   line_color='red', showlegend=False, name="Promedio",legendgroup='Promedio'),
        row=1, col=2
    )          
    fig.add_trace(
        go.Scatter(x=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Temp, y=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Alt, 
                   line_color='blue', legendgroup='Sondeo',showlegend=False),
        row=1, col=2
    )
#################################### RH#######################################    
    fig.add_trace(
        go.Scatter(
            name="90%",legendgroup='90%',
            x=ozonosondes_climatology_90.RH,
            y=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Alt,
            marker=dict(color="#444"),
            line=dict(width=0),
             mode='lines',
            showlegend=False
        ),
        row=1, col=3
        )
    
    fig.add_trace(
        go.Scatter(
        name="10%",legendgroup='10%',
        x=ozonosondes_climatology_10.RH,
        y=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Alt,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
        showlegend=False)
        ,
        row=1, col=3
        )
    
    fig.add_trace(
        go.Scatter(
            name="30%",legendgroup='30%',
            x=ozonosondes_climatology_30.RH,
            y=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Alt,
            marker=dict(color="#444"),
            line=dict(width=0),
             mode='lines',
            showlegend=False
        ),
        row=1, col=3
        )
    
    fig.add_trace(
        go.Scatter(
        name="70%",legendgroup='70%',
        x=ozonosondes_climatology_70.RH,
        y=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Alt,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
        showlegend=False)
        ,
        row=1, col=3
        )
    fig.add_trace(
        go.Scatter(x=ozonosondes_climatology_mean.RH, y=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Alt,
                   line_color='red',name="Promedio",legendgroup='Promedio'),
        row=1, col=3
    )
    fig.add_trace(
        go.Scatter(x=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].RH, y=ozonosondes_data[dropdown_years_esp+'-'+dropdown_months_esp+'-'+str(dropdown_days_esp)].Alt, 
                   line_color='blue', name="Sondeo",legendgroup='Sondeo'),
        row=1, col=3
    )
    fig.update_layout(
            title_font_family="Times New Roman",  
            title_font_size=30,
            title_font_color = 'dimgray',
            plot_bgcolor='#f6f6f6',
            paper_bgcolor='#f6f6f6',
            margin=dict(t=20, b=10, l=10, r = 10)
            
            )
    fig.update_xaxes(title_text="O<sub>3</sub> [mPa]", row=1, col=1) 
    fig.update_yaxes(title_text="Altura [km]", row=1, col=1) 
    fig.update_xaxes(title_text="Temperatura [K]", row=1, col=2) 
    fig.update_xaxes(title_text="HR [%]", row=1, col=3) 

    
    return fig 

def vertical_profiles(dropdown_years_eng, dropdown_months_eng, dropdown_days_eng,
                      ozonosondes_climatology_90, ozonosondes_climatology_70,
                       ozonosondes_climatology_30, ozonosondes_climatology_10, 
                       ozonosondes_climatology_mean, ozonosondes_data):
    fig = make_subplots(rows=1, cols=3)
##################### O3 #####################################################         
    fig.add_trace(
        go.Scatter(
            name="90%",legendgroup='90%',
            x=ozonosondes_climatology_90.O3_mba,
            y=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Alt,
            marker=dict(color="#444"),
            line=dict(width=0),
             mode='lines'
            
        ),
        row=1, col=1
        )
    
    fig.add_trace(
        go.Scatter(
        name="10%",legendgroup='10%',
        x=ozonosondes_climatology_10.O3_mba,
        y=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Alt,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty')
        ,
        row=1, col=1
        )
    
    fig.add_trace(
        go.Scatter(
            name="30%",legendgroup='30%',
            x=ozonosondes_climatology_30.O3_mba,
            y=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Alt,
            marker=dict(color="#444"),
            line=dict(width=0),
             mode='lines'
        ),
        row=1, col=1
        )
    
    fig.add_trace(
        go.Scatter(
        name="70%",legendgroup='70%',
        x=ozonosondes_climatology_70.O3_mba,
        y=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Alt,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty')
        ,
        row=1, col=1
        )
    fig.add_trace(
        go.Scatter(x=ozonosondes_climatology_mean.O3_mba, y=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Alt
      ,line_color='red', name="Mean",legendgroup='Mean'  ),  
        row=1, col=1
        )
    fig.add_trace(
        go.Scatter(x=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].O3_mPa, y=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Alt,
        line_color='blue',name='Sounding', legendgroup='Sounding'           
        ),  
        row=1, col=1
        )
################### temp #####################################################  
    fig.add_trace(
        go.Scatter(
            name="90%",legendgroup='90%',
            x=ozonosondes_climatology_90.Temp,
            y=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Alt,
            marker=dict(color="#444"),
            line=dict(width=0),
             mode='lines',
            showlegend=False
        ),
        row=1, col=2
        )
    
    fig.add_trace(
        go.Scatter(
        name="10%",legendgroup='10%',
        x=ozonosondes_climatology_10.Temp,
        y=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Alt,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
        showlegend=False)
        ,
        row=1, col=2
        )
    
    fig.add_trace(
        go.Scatter(
            name="30%",legendgroup='30%',
            x=ozonosondes_climatology_30.Temp,
            y=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Alt,
            marker=dict(color="#444"),
            line=dict(width=0),
             mode='lines',
            showlegend=False
        ),
        row=1, col=2
        )
    
    fig.add_trace(
        go.Scatter(
        name="70%",legendgroup='70%',
        x=ozonosondes_climatology_70.Temp,
        y=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Alt,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
        showlegend=False)
        ,
        row=1, col=2
        ) 
    fig.add_trace(
        go.Scatter(x=ozonosondes_climatology_mean.Temp, y=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Alt, 
        line_color='red',
        name="Mean", legendgroup='Mean',
        showlegend=False),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(x=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Temp, y=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Alt,
        line_color='blue',legendgroup='Sounding',
        showlegend=False),
        row=1, col=2
    )    

#################################### RH#######################################    
    fig.add_trace(
        go.Scatter(
            name="90%",legendgroup='90%',
            x=ozonosondes_climatology_90.RH,
            y=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Alt,
            marker=dict(color="#444"),
            line=dict(width=0),
             mode='lines',
            showlegend=False
        ),
        row=1, col=3
        )
    
    fig.add_trace(
        go.Scatter(
        name="10%",legendgroup='10%',
        x=ozonosondes_climatology_10.RH,
        y=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Alt,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
        showlegend=False)
        ,
        row=1, col=3
        )
    
    fig.add_trace(
        go.Scatter(
            name="30%",legendgroup='30%',
            x=ozonosondes_climatology_30.RH,
            y=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Alt,
            marker=dict(color="#444"),
            line=dict(width=0),
             mode='lines',
            showlegend=False
        ),
        row=1, col=3
        )
    
    fig.add_trace(
        go.Scatter(
        name="70%",legendgroup='70%',
        x=ozonosondes_climatology_70.RH,
        y=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Alt,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
        showlegend=False)
        ,
        row=1, col=3
        )
    fig.add_trace(
        go.Scatter(x=ozonosondes_climatology_mean.RH, y=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Alt, line_color='red',
                   name="Mean",legendgroup='Mean', showlegend=False),
        row=1, col=3
    )
    fig.add_trace(
        go.Scatter(x=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].RH, y=ozonosondes_data[dropdown_years_eng+'-'+dropdown_months_eng+'-'+str(dropdown_days_eng)].Alt,
                   line_color='blue', legendgroup='Sounding', showlegend=False),
        row=1, col=3
    )
    fig.update_layout(
            title_font_family="Times New Roman",
    #        title_font_color="red",        
            title_font_size=30,
            title_font_color = 'dimgray',
            plot_bgcolor='#f6f6f6',
            paper_bgcolor='#f6f6f6',
            margin=dict(t=20, b=10, l=10, r = 10)
            )
    fig.update_xaxes(title_text="O<sub>3</sub> [mPa]", row=1, col=1) 
    fig.update_yaxes(title_text="Height [km]", row=1, col=1) 
    fig.update_xaxes(title_text="Temperature [K]", row=1, col=2) 
    fig.update_xaxes(title_text="HR [%]", row=1, col=3) 

    return fig
