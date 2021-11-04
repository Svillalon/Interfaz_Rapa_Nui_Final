#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 13:06:32 2021

@author: charlie opazo

This script merges the GAW database with the CR2 database. 
There are 3 ways to save data:
    - If the soungind is only in the GAW database
    - If the soungind is only in the CR2 database
    - If sounding data is in both databases, it is saved: 1) CR2 data if it has more 
    records in the ozone profile than GAW; or 2) GAW if it has more data in the
    ozone profile than CR2. For case 2), if CR2 has wind data but GAW does not, 
    the wind data is added to the GAW sounding.


Also, this script generate one file .csv, 'RapaNui_dates_valid.csv', for to 
save info about ozone profiles validation. This file must be filled with:
    - Validate: validated profile (=1), non-validated profile (=0),
                repeated profile (=-1), per variable profile
    - Height_{inf,sup}: heights [km] to be removed in the profile per variable
                        profile
    - Comments: profile comments by launching


"""


# Import
import pandas as pd
import numpy as np
import os


def merge_winds_df(df1, df2):
    """
    Append CR2 wind sounding data to GAW sounding data in individual sounding.

    Parameters
    ----------
    df1 : dataframe
        GAW sounding data
    df2 : dataframe
        CR2 sounding data

    Returns
    -------
    df1c : dataframe
        GAW sounding data with CR2 sounding data wind

    """
    
    day = df1.index[0]
    
    df1c = df1.copy()
    
    df2c = df2.copy()
    df2c = df2c.dropna(subset=['WindSpeed', 'WindDirection'])
    
    z2 = df2c.GPHeight.values
    
    for z in z2:
        line = df2c.iloc[z2==z]
        
        z1 = df1c.GPHeight.values
        
        if z in z1:
            df1c.iloc[z1==z] = line.values
            # print(z)
        
        else:
            line = line.values.squeeze()
            line[1:5] = np.nan
            idnear = np.abs(z1 - z).argmin()
            if (z1[idnear] - z) < 0:
                idnear += 1
            x = df1c.T
            x.insert(int(idnear), day, line, allow_duplicates=True)
            x = x.T
            df1c = x
        

    df1c.index.rename('Datetime', inplace=True)
    
    return df1c



# Get path
path = os.getcwd()# use your path

# Path archivos
fn_GAW = os.path.join(path, 'RapaNui_GAW_ozonesondes.csv')
fn_CR2 = os.path.join(path, 'RapaNui_CR2_ozonesondes.csv')

# Lee los archivos de GAW y CR2
dfold_GAW = pd.read_csv(fn_GAW, index_col=[0], delimiter=';', parse_dates=[0],
                         float_precision='round_trip')
dfold_CR2 = pd.read_csv(fn_CR2, index_col=[0], delimiter=';', parse_dates=[0],
                         float_precision='round_trip')

# Obtiene las fechas de lanzamiento en ambas bases de datos
dates_GAW = dfold_GAW.index.get_level_values('Datetime').drop_duplicates()
dates_CR2 = dfold_CR2.index.get_level_values('Datetime').drop_duplicates()

# Genera un vector auxiliar de fechas de GAW con formato '%Y-%m-%d'
dates_GAW_aux = pd.to_datetime(dates_GAW.strftime('%Y-%m-%d'), format='%Y-%m-%d')

# Genera vector auxiliar juntando fechas de ambas bases de datos
dates_aux = dates_GAW_aux.copy()
dates_aux = dates_aux.append(dates_CR2)
dates_aux = dates_aux.drop_duplicates()
dates_aux = dates_aux.sort_values()

# Juntar las bases de datos
dfold = pd.DataFrame()

for d in dates_aux:
    # Si solo esta en GAW se agrega
    if (d in dates_GAW_aux) and (d not in dates_CR2):
        dgaw = dates_GAW[dates_GAW_aux.get_loc(d)]
        df_gaw = dfold_GAW.loc[[dgaw]]
        dfold = pd.concat([dfold, df_gaw])
        
    # Si solo esta en CR2 se agrega
    elif (d in dates_CR2) and (d not in dates_GAW_aux):
        df_cr2 = dfold_CR2.loc[[d]]
        dfold = pd.concat([dfold, df_cr2])
        
    # Si esta en ambas bases de datos, se guarda: 1) los datos de CR2 si
    # tienen mas registros en el perfil de ozono que GAW; o 2) GAW si tiene mas
    # datos en el perfil de ozono que CR2. Para el caso 2), si CR2 tiene datos
    # de viento pero GAW no, se agregan los datos de viento a GAW.
    elif (d in dates_GAW_aux) and (d in dates_CR2):
        dgaw = dates_GAW[dates_GAW_aux.get_loc(d)]
        df_gaw = dfold_GAW.loc[[dgaw]]
        df_cr2 = dfold_CR2.loc[[d]]
        
        N_cr2 = df_cr2.O3PartialPressure.dropna().size
        N_gaw = df_gaw.O3PartialPressure.dropna().size
        
        if N_cr2 > N_gaw:
            N = df_cr2.shape[0]
            tnew = [dgaw] * N
            df_cr2.reset_index(drop=True, inplace=True)
            df_cr2.index = tnew
            df_cr2.index.rename('Datetime', inplace=True)
            dfold = pd.concat([dfold, df_cr2])
            
        elif N_cr2 <= N_gaw:
            Nw_cr2 = df_cr2.WindSpeed.dropna().size
            Nw_gaw = df_gaw.WindSpeed.dropna().size
            
            if Nw_cr2 > Nw_gaw:
                df_gaw = merge_winds_df(df_gaw, df_cr2)
            
            dfold = pd.concat([dfold, df_gaw])


# Guardar archivo con sondeos
out_allsondes = os.path.join(path, 'RapaNui_all_ozonesondes.csv')
dfold.to_csv(out_allsondes, sep=';')





# Generar archivo que guarda fechas de lanzamiento, con formato para indicar
# lanzamientos validos, comentarios y rangos de alturas a eliminar. Actualiza
# el archivo si existe y tiene nuevas fechas, y si ya tiene las fechas cargadas
# no modifica el archivo existente. Tambien se indica si el perfil se encuentra
# repetido dentro de la base de datos.

dates = dfold.index.drop_duplicates()

# Genera dateframe para guardar datetimes en formato para validarlos
vars_df_valid = ['Valid_O3', 'Height_inf_O3', 'Height_sup_O3',
                 'Valid_T', 'Height_inf_T', 'Height_sup_T',
                 'Valid_P', 'Height_inf_P', 'Height_sup_P',
                 'Valid_RH', 'Height_inf_RH', 'Height_sup_RH',
                 'Valid_V', 'Height_inf_V', 'Height_sup_V',
                 'Comments']

df_valid_new = pd.DataFrame(columns=vars_df_valid, index=dates)

# Filename
filename_df_valid = os.path.join(path, 'RapaNui_dates_valid.csv')
# Verifica si archivo existe o no
if os.path.isfile(filename_df_valid):
    df_valid_old = pd.read_csv(filename_df_valid, delimiter=';', index_col=0, 
                                parse_dates=True)
    if df_valid_new.index.equals(df_valid_old.index) == False:
        df_valid = pd.concat([df_valid_old, df_valid_new])
        df_valid = df_valid.iloc[~df_valid.index.duplicated(keep='first')]
        df_valid.sort_index(inplace=True)
        df_valid.to_csv(filename_df_valid, sep=';')
else:
    df_valid_new.to_csv(filename_df_valid, sep=';')
    
    