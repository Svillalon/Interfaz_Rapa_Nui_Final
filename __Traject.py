#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 16:24:47 2021

@author: Sebastián Villalón
"""
import datetime
import pandas as pd
import os
from plotly.subplots import make_subplots
import plotly.graph_objects as go
def Trayectoria(df_trayect,dropdown_years_esp_2, dropdown_months_esp_2, dropdown_days_esp_2, radio_traject):
    
    dfold = df_trayect
    
    t = dfold[dfold.index.get_level_values(0).date == datetime.date(int(dropdown_years_esp_2)
                                                                    ,int(dropdown_months_esp_2),
                                                                    int(dropdown_days_esp_2))].index[0][0]
    z1 = 4000
    z2 = 8000
    z3 = 12000
    if radio_traject=='Horizontal':	
        	fig = make_subplots(rows=1, cols=1, specs=[[{"type": "scattergeo"}]])
            
        	fig.add_trace(go.Scattergeo(lat= dfold.loc[(t,z1)].Latitude.values, 
                                     	 lon=dfold.loc[(t,z1)].Longitude.values, 
                                      	name="4 [km]",legendgroup='4 [km]',
                                      	showlegend=True, line_color='blue'), row=1, col=1
            		)
        	fig.add_trace(go.Scattergeo(lat= dfold.loc[(t,z2)].Latitude.values, 
                                      	lon=dfold.loc[(t,z2)].Longitude.values,
                                      	name="8 [km]",legendgroup='8 [km]',
                                      	showlegend=True, line_color='red'), 
                      	row=1, col=1)
        	fig.add_trace(go.Scattergeo(lat= dfold.loc[(t,z3)].Latitude.values, 
                                    	  lon=dfold.loc[(t,z3)].Longitude.values,
                                      	name="12 [km]",legendgroup='12 [km]',
                                      	showlegend=True, line_color='green'),
                      	row=1, col=1)
          
        	fig.update_geos(
                        	bgcolor='#f6f6f6',
                        	lataxis_showgrid=True, lonaxis_showgrid=True
                        
                          	)
    elif radio_traject=='Vertical':
            fig = make_subplots(rows=1, cols=1,
                        specs=[[{"type": "scatter"}]])

            fig.add_trace(
            go.Scatter(
            x = dfold.loc[(t,z1)].index,
            y = dfold.loc[(t,z1)].Altitude.values/1000,
            name="4 [km]",legendgroup='4 [km]',
            line_color='blue'
            )
            ,
            row=1, col=1
            )
            fig.add_trace(
            go.Scatter(
            x = dfold.loc[(t,z2)].index,
            y = dfold.loc[(t,z2)].Altitude.values/1000,
            name="8 [km]",legendgroup='8 [km]',
            line_color='red'
            )
            ,
            row=1, col=1
            )
            fig.add_trace(
            go.Scatter(
            x = dfold.loc[(t,z3)].index,
            y = dfold.loc[(t,z3)].Altitude.values/1000,
            name="12 [km]",legendgroup='12 [km]',
            line_color='green'
            )
            ,
            row=1, col=1
            )
            fig.update_yaxes(title_text="Altura [km]", row=1, col=1) 

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, 
                          paper_bgcolor='#f6f6f6',
                          plot_bgcolor='#f6f6f6',
                          )
        
    return fig

def Trayectory(df_trayect,dropdown_years_eng_2, dropdown_months_eng_2, dropdown_days_eng_2, radio_traject):
    
    dfold = df_trayect
    
    t = dfold[dfold.index.get_level_values(0).date == datetime.date(int(dropdown_years_eng_2)
                                                                    ,int(dropdown_months_eng_2),
                                                                    int(dropdown_days_eng_2))].index[0][0]
    z1 = 4000
    z2 = 8000
    z3 = 12000
    if radio_traject=='Horizontal':	
        	fig = make_subplots(rows=1, cols=1, specs=[[{"type": "scattergeo"}]])
            
        	fig.add_trace(go.Scattergeo(lat= dfold.loc[(t,z1)].Latitude.values, 
                                     	 lon=dfold.loc[(t,z1)].Longitude.values, 
                                      	name="4 [km]",legendgroup='4 [km]',
                                      	showlegend=True, line_color='blue'), row=1, col=1
            		)
        	fig.add_trace(go.Scattergeo(lat= dfold.loc[(t,z2)].Latitude.values, 
                                      	lon=dfold.loc[(t,z2)].Longitude.values,
                                      	name="8 [km]",legendgroup='8 [km]',
                                      	showlegend=True, line_color='red'), 
                      	row=1, col=1)
        	fig.add_trace(go.Scattergeo(lat= dfold.loc[(t,z3)].Latitude.values, 
                                    	  lon=dfold.loc[(t,z3)].Longitude.values,
                                      	name="12 [km]",legendgroup='12 [km]',
                                      	showlegend=True, line_color='green'),
                      	row=1, col=1)
          
        	fig.update_geos(
                        	bgcolor='#f6f6f6',
                        	lataxis_showgrid=True, lonaxis_showgrid=True
                        
                          	)
    elif radio_traject=='Vertical':
            fig = make_subplots(rows=1, cols=1,
                        specs=[[{"type": "scatter"}]])

            fig.add_trace(
            go.Scatter(
            x = dfold.loc[(t,z1)].index,
            y = dfold.loc[(t,z1)].Altitude.values/1000,
            name="4 [km]",legendgroup='4 [km]',
            line_color='blue'
            )
            ,
            row=1, col=1
            )
            fig.add_trace(
            go.Scatter(
            x = dfold.loc[(t,z2)].index,
            y = dfold.loc[(t,z2)].Altitude.values/1000,
            name="8 [km]",legendgroup='8 [km]',
            line_color='red'
            )
            ,
            row=1, col=1
            )
            fig.add_trace(
            go.Scatter(
            x = dfold.loc[(t,z3)].index,
            y = dfold.loc[(t,z3)].Altitude.values/1000,
            name="12 [km]",legendgroup='12 [km]',
            line_color='green'
            )
            ,
            row=1, col=1
            )
            fig.update_yaxes(title_text="Height [km]", row=1, col=1) 

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, 
                          paper_bgcolor='#f6f6f6',
                          plot_bgcolor='#f6f6f6',
                          )
        
    return fig
                  


