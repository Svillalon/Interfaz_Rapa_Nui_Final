#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 19:21:16 2021

@author: sebastian
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
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
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc

orig = os.getcwd()
fn_ozonosondes = orig + '/' + 'RapaNui_all_clear.csv' 
ozonosondes_data = pd.read_csv(fn_ozonosondes, index_col=0, parse_dates=True)

ozonosondes_climatology_10 = pd.DataFrame()
ozonosondes_climatology_30 = pd.DataFrame()
ozonosondes_climatology_mean = pd.DataFrame()
ozonosondes_climatology_70 = pd.DataFrame()
ozonosondes_climatology_90 = pd.DataFrame()

for i in np.linspace(0,35,351):
    var_10 = ozonosondes_data[ozonosondes_data.Alt== round(i,2)].quantile(0.1).to_frame().T
    var_10 =  var_10.set_index('Alt')
    ozonosondes_climatology_10 = pd.concat([ozonosondes_climatology_10, var_10])
    
    var_30 = ozonosondes_data[ozonosondes_data.Alt== round(i,2)].quantile(0.3).to_frame().T
    var_30 =  var_30.set_index('Alt')
    ozonosondes_climatology_30 = pd.concat([ozonosondes_climatology_30, var_30])
    
    var_mean = ozonosondes_data[ozonosondes_data.Alt== round(i,2)].mean().to_frame().T
    var_mean =  var_mean.set_index('Alt')
    ozonosondes_climatology_mean = pd.concat([ozonosondes_climatology_mean, var_mean])
    
    var_70 = ozonosondes_data[ozonosondes_data.Alt== round(i,2)].quantile(0.7).to_frame().T
    var_70 =  var_70.set_index('Alt')
    ozonosondes_climatology_70 = pd.concat([ozonosondes_climatology_70, var_70])
    
    var_90 = ozonosondes_data[ozonosondes_data.Alt== round(i,2)].quantile(0.9).to_frame().T
    var_90 =  var_90.set_index('Alt')
    ozonosondes_climatology_90 = pd.concat([ozonosondes_climatology_90, var_90])

ozonosondes_climatology_10.to_csv(orig+'/'+'Ozonosondes_quantile10'+'.csv')    
ozonosondes_climatology_30.to_csv(orig+'/'+'Ozonosondes_quantile30'+'.csv')    
ozonosondes_climatology_mean.to_csv(orig+'/'+'Ozonosondes_mean'+'.csv')    
ozonosondes_climatology_70.to_csv(orig+'/'+'Ozonosondes_quantile70'+'.csv')    
ozonosondes_climatology_90.to_csv(orig+'/'+'Ozonosondes_quantile90'+'.csv')    