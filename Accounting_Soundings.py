#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 14 23:27:18 2021

@author: charlie opazo

This script counts the soundings in the database per season and per year. 

Returns 2 files .xlsx:
    - 'Table_TotalNumSoundings_RapaNui.xlsx': counts all soundings
    - 'Table_ValidNumSoundings_RapaNui.xlsx': counts only validated soundings

Repeated soundings (Valid_O3 = -1) are not counted in either of the 2 files.

Seasons per year:
DJF = December - January - February
MAM = March - April - May
JJA = June - July - August
SON = September - November - December



"""

# Importar librerias necesarias
import pandas as pd
import numpy as np
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


# Genera vector del periodo de años de medicion
yri = df.index.year[0]
yrf = df.index.year[-1]
years = np.arange(yri, yrf+1, 1)

# Cuenta todos los sondeos no repetidos (validos y no validos)
df_cont_all = pd.DataFrame(index=years, columns=['DJF', 'MAM', 'JJA', 'SON'])
df_cont_all.index.rename('Year',inplace=True)

# Cuenta los sondeos con perfil de ozono validos
df_cont_val = pd.DataFrame(index=years, columns=['DJF', 'MAM', 'JJA', 'SON'])
df_cont_val.index.rename('Year',inplace=True)

# Iteracion por año
for y in years:
    
    # Extrae datos asociados al año y
    df_y = df[str(y)]
    
    # Inicializa valores para contar sondeos totales
    DJF = 0
    MAM = 0
    JJA = 0
    SON = 0
    
    # Inicializa valores para contar sondeos validos
    DJF_val = 0
    MAM_val = 0
    JJA_val = 0
    SON_val = 0
    
    # Iteracion por sondeo en el año
    for d in df_y.index:
        
        m = d.month
        
        # Contabilizacion por estacion. Y si pertenece a una estacion, 
        # contabilizar si es valido o no
        if m in [1, 2, 12]:
            DJF += 1
            if (df_y.loc[str(d), 'Valid_O3'] == 1):
                DJF_val += 1
        if m in [3, 4, 5]:
            MAM += 1
            if (df_y.loc[str(d), 'Valid_O3'] == 1):
                MAM_val += 1
        if m in [6, 7, 8]:
            JJA += 1
            if (df_y.loc[str(d), 'Valid_O3'] == 1):
                JJA_val += 1
        if m in [9, 10, 11]:
            SON += 1
            if (df_y.loc[str(d), 'Valid_O3'] == 1):
                SON_val += 1

        
    # Guardar valores de conteos totales por estacion en este año y
    df_cont_all.loc[y, 'DJF'] = DJF
    df_cont_all.loc[y, 'MAM'] = MAM
    df_cont_all.loc[y, 'JJA'] = JJA
    df_cont_all.loc[y, 'SON'] = SON
            
    # Guardar valores de conteos validos por estacion en este año y
    df_cont_val.loc[y, 'DJF'] = DJF_val
    df_cont_val.loc[y, 'MAM'] = MAM_val
    df_cont_val.loc[y, 'JJA'] = JJA_val
    df_cont_val.loc[y, 'SON'] = SON_val
    
    
# Suma por año
df_cont_all['Total']=df_cont_all.sum(axis=1)
df_cont_val['Total']=df_cont_val.sum(axis=1)
    
# Suma total por estacion y año
df_cont_all.loc['Total']=df_cont_all.sum()
df_cont_val.loc['Total']=df_cont_val.sum()

# Guardar tablas con conteos
df_cont_all.to_excel('Table_TotalNumSoundings_RapaNui.xlsx')
df_cont_val.to_excel('Table_ValidNumSoundings_RapaNui.xlsx')