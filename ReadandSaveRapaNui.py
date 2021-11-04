#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 13:53:36 2021

@author: charlie opazo and sebastian villalon

Reading and saving Rapa Nui ozonesounding data. Except for removing negative 
values, no cleansing or resampling is applied to the data.

Read data from CR2 database and GAW database. This script returns one file in 
.csv, 'RapaNui_GAW_ozonesondes.csv', with all soundings in GAW database, and 
one file .csv, 'RapaNui_CR2_ozonesondes.csv', with all soundings in CR2 database.

CR2 database for the period 1994-2014 was downloaded from http://www.cr2.cl/datos-ozonosonda/
GAW database for the period 1995-2020 was downloaded from https://woudc.org/
This sets correspond to sounding data per launch in Eastern Island station


"""

# Import
import pandas as pd
import numpy as np
from glob import glob
import os
import csv
import chardet


def lecture_GAW(filename):
    """
    Read individual sounding file obtained from GAW data base and return 
    dataframe with:
        - datetime launch [datetime format]
        - geopotential height [m]
        - pressure [hPa]
        - temperature [°C]
        - relative humidity [%]
        - ozone partial pressure [mPa]
        - wind speed [m/s], if it is measured
        - wind direction [°], if it is measured

    Parameters
    ----------
    filename : str
        Path + filename soundig data.

    Returns
    -------
    dataframes : DataFrame
        Datraframe with sounding data.

    """
    
    # Buscar tipo de encode del archivo
    with open(filename, 'rb') as file:
        enc=chardet.detect(file.read())['encoding']

    
    # Buscar lineas a saltar del header para leer datos del archivo.
    # Tambien busca fecha y hora de lanzamiento del sondeo en el archivo
    with open(filename, 'r', encoding=enc) as file:
        reader = csv.reader(file, delimiter=',')
             
        iline = 0
        for row in reader:
            if row == []:
                pass
            elif row[0] == 'UTCOffset':
                date = next(reader)[1:3]
                fecha = date[0]
                hora = date[1]
                fechahora = date[0] + ' ' + hora
            elif row[0] == '#PROFILE' or row[0] == '#PROFILE ':
                iline += 2
                break
            iline += 1
    
    # Cargar mediciones del sonde en dateframe
    if fecha == '2008-7-5':
        # Excepcion para archivo del 2008-7-5, distinto encode y error en header
        rows = []
        rows.extend(range(iline))
        rows.extend(range(iline+1, iline+3))
        dataframes = pd.read_csv(filename, skiprows=rows, encoding=enc, float_precision='round_trip')
    else:
        dataframes = pd.read_csv(filename, skiprows=iline, na_values= ['///'], float_precision='round_trip')
    
    # Crear vector de tiempo, con el tiempo de lanzamiento para agregar index
    # a dateframes
    N = dataframes.shape
    time = []
    for i in range(N[0]):
        time.append(fechahora)
    time = pd.to_datetime(time)
        
    dataframes.index = time
    dataframes.index.rename('Datetime', inplace=True)
    
    # Renombrar columnas que estan mal ordenadas
    badfiles = ['2007', '2008']
    
    if fecha[0:4] in badfiles:
        dataframes.rename(columns={'WindSpeed' : 'GPHeight', 'WindDirection' : 'RelativeHumidity',
                                  'GPHeight' : 'WindSpeed', 'RelativeHumidity' : 'WindDirection'},
                          inplace=True)
    

    
    # Extraer variables a ocupar
    if 'WindSpeed' in dataframes.keys():
        # Si el archivo tiene mediciones de viento
        variables = ['GPHeight','Pressure', 'Temperature', 'RelativeHumidity',
                      'O3PartialPressure', 'WindSpeed', 'WindDirection']
    else:
        # Si el archivo no tiene mediciones de viento
        variables = ['GPHeight','Pressure', 'Temperature', 'RelativeHumidity',
                      'O3PartialPressure']
        
    dataframes = dataframes[variables]
    
    
    return dataframes    



def lecture_CR2(filename):
    """
    Read individual sounding file obtained from CR2 database and return 
    dataframe with:
        - datetime launch [datetime format]
        - geopotential height [m]
        - pressure [hPa]
        - temperature [°C]
        - relative humidity [%]
        - ozone partial pressure [mPa]
        - wind speed [m/s]
        - wind direction [°]

    Parameters
    ----------
    filename : str
        Path + filename soundig data.

    Returns
    -------
    dataframes : DataFrame
        Datraframe with sounding data.

    """
    
    
    df = pd.read_csv(filename, skiprows=list(range(19))+[20], sep='\s+', 
                     na_values=9000, float_precision='round_trip')
    
    
    ti_df = pd.read_csv(filename,nrows=1, skiprows=7, delimiter=":", header=None, parse_dates=[1])
    ti = ti_df[1][0]
    
    # Crear vector de tiempo, con el tiempo de lanzamiento para agregar index
    # a dateframes
    N = df.shape
    time = []
    for i in range(N[0]):
        time.append(ti)
        
    df.index = time
    df.index.rename('Datetime', inplace=True)
    
    WSpeed = np.sqrt(df['u']**2 + df['v']**2)
    WDir = np.arctan2(-df['u'], -df['v']) * (180/np.pi)
    WDir[WDir<0] = WDir[WDir<0] + 360
    WDir[WDir==-0] = 0
    
    df['WindSpeed'] = WSpeed
    df['WindDirection'] = WDir
    
    # Cambiar unidades a m y °C
    df['Temp'] = df['Temp'] - 273.15
    df['Alt'] = 1000 * df['Alt']
    
    # Extraer columnas necesarias y renombrarlas
    var_names = ['Alt', 'Press', 'Temp', 'RH', 'O3', 'WindSpeed', 'WindDirection']
    df = df[var_names]
    df.rename(columns={'Alt':'GPHeight', 'Press':'Pressure', 'Temp':'Temperature',
                       'RH':'RelativeHumidity', 'O3':'O3PartialPressure'},
              inplace=True)
    
    return df





# Get path
path = os.getcwd()# use your path

# Cargar los nombres de todos los archivos en las carpetas de la base de datos
# de GAW
filenames_GAW = []
for year in range(1995, 2021):
    # Path de carpeta de año en base datos de GAW
    fns = os.path.join(path, "Data", "DB-GAW", str(year), str(year)+"*.csv")
    filenames_GAW += glob(fns)


# cargar todos los datos de ozonosondas en mismo dateframe
dfold_GAW_aux = pd.DataFrame()
for filename in filenames_GAW:
    df = lecture_GAW(filename)
    dfold_GAW_aux = pd.concat([dfold_GAW_aux, df])

# Datetime de lanzamiento
dates_GAW = dfold_GAW_aux.index.drop_duplicates()
dates_GAW = dates_GAW.sort_values()

# sort dataframe by launch datetime
dfold_GAW = pd.DataFrame()
for dat in dates_GAW:
    dfold_GAW = pd.concat([dfold_GAW, dfold_GAW_aux.loc[dat]])
    
# remove negative values in O3PartialPressure
dfold_GAW.O3PartialPressure[dfold_GAW.O3PartialPressure<0] = np.nan

# Save all profiles in one file
out_GAW = os.path.join(path, 'RapaNui_GAW_ozonesondes.csv')
dfold_GAW.to_csv(out_GAW, sep=';')





# Cargar los nombres de todos los archivos en la carpeta DB-CR2
path_CR2 = os.path.join(path, "Data", "DB-CR2", "*.dat")
filenames_CR2 = glob(path_CR2)


dfold_CR2_aux = pd.DataFrame()
for filename in filenames_CR2:
    df = lecture_CR2(filename)
    dfold_CR2_aux = pd.concat([dfold_CR2_aux, df])


dates_CR2 = dfold_CR2_aux.index.drop_duplicates()
dates_CR2 = dates_CR2.sort_values()

# sort dataframe by launch datetime
dfold_CR2 = pd.DataFrame()
for dat in dates_CR2:
    dfold_CR2 = pd.concat([dfold_CR2, dfold_CR2_aux.loc[dat]])

out_CR2 = os.path.join(path, 'RapaNui_CR2_ozonesondes.csv')
dfold_CR2.to_csv(out_CR2, sep=';')

