#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 17:37:00 2021

@author: charlie opazo

This script returns one file .csv, 'RapaNui_DatesStr_hysplit.csv', with 
launching datetimes of all soundings.
Repeated soundings (Valid_O3 = -1) are not counted.

"""

# Importar librerias necesarias
import pandas as pd
import os

# Get path
path = os.getcwd()
# Ruta y nombre del archivo que contiene fechas e indicatriz de validez de los
# datos
fn_validate = os.path.join(path, 'RapaNui_dates_valid.csv')
# Lee el archivo y no considera para los conteos los sondeos repetidos 
# identificados (Valid_O3 = -1)
df = pd.read_csv(fn_validate, delimiter=';', index_col=0, parse_dates=True)
df = df[df.Valid_O3.values!=-1]

dates = df.index

# Generar archivo con fechas en formato %yy %mm %dd %HH %MM´ para utilizar en 
# codigo generador de trayectores
filename_datestr = os.path.join(path, 'RapaNui_DatesStr_hysplit.csv')
dates_str = pd.DataFrame(dates.strftime('%y %m %d %H %M'))
dates_str.to_csv(filename_datestr, header=False,index=False)