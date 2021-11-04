#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 13:42:02 2021

@author: charlie opazo and sebastian villalon

Read file "RapaNui_all_ozonesondes.csv", cleaning and interpolate data.
Remove points that measured altitude is descending.
Remove layers in ozone profiles with anomalous measurements
Interpolate variables to regular altitudes every 100 m between 0 y 35 km-
Save individual files per launch and one file with all sondes data.

Saved variables: 
    Pressure [hPa]
    Temperature [K]
    Relative Humidity [%]
    Ozone partial pressure [mba]
    Ozone [ppbv]
    Column ozone [DU]
    Zonal wind [m/s]
    Meridional wind [m/s]
    Wind Speed [m/s]
    Wind Direction [°]
    Potential temperature [K]
    Equivalent potential temperature [K]
    Water vapor mixing ratio [g/kg]


"""

# Import libraries
import numpy as np
import pandas as pd
import os
import platform
from scipy.interpolate import interp1d
import warnings




def remov_desc(df):
    """
    Remove rows with points in sonde data that are descending in altitude 
    during flight time
    
    Parameters
    ----------
    df : DataFrame
        DataFrame with data per launch.

    Returns
    -------
    df_clean : DataFrame
        DataFrame without points that are descending in profile

    """
    
    # Extract altitude
    z = df.GPHeight.values
    
    # Find z decreasing
    i_zasc = [0]
    zant = z[0]
    for i in range(1,len(z)):
        if z[i] > zant:
            zant = z[i]
            i_zasc.append(i)
        else:
            pass
            
    # remove zdec in dataframe
    df_clean = df.iloc[i_zasc]
    
    return df_clean



def ozone_column(pO3, pressure, z, z_intp, type_intp='linear', prof_val=0,  
                 Hinf=[], Hsup=[], dHmax = 0.3):
    """
    Calculate ozone column profile and interpolate to regular altitudes in array z. 
    Return profile with nan's if serie does not validate. If it is validate and Hinf 
    and Hsup are not [], there are 2 posibilities:
        - If atmospheric layer depth is less than dHmax (by defeault = 1 km), 
          points inside this layer don't be considerated for interpolation
        - If atmospheric layer depth is greater than dHmax (by defeault = 1 km), 
          points inside this layer are set to nan's.

    Parameters
    ----------
    pO3 : array
        Ozone partial pressure profile in [mPa].
    pressure : array
        Atmospheric pressure profile in [hPa].
    z : array
        Array with altitudes measured altitudes in [km].
    z_intp : array
        Array with altitudes where interpolate in [km].
    type_intp : str, optional
        Type of interpolation. The default is 'linear'.
    prof_val: int or float
        Indicate if serie is validated. If it is not validated, prof_val=0; if
        it is validated, prof_val=1 if is. By defalt prof_val=0
    Hinf: list
        Contains lower limit of atmospheric layers does not validate in [km]. By 
        default is []
    Hsup: list
        Contains upper limit of atmospheric layers does not validate in [km]. By
        default is []
    dHmax: float
        Maximum atmospheric layer depth, in km, to interpolate with missing data


    Returns
    -------
    serie_intp : array
        Variable interpolated to regular altitudes.

    """
    
    # If profile doesn't validated, return profile interpolated with nan's
    if prof_val == 0:
        
        O3_col_intp = np.nan * np.zeros(len(z_intp))
        
        return O3_col_intp
    
    
    # If profile is validated, to interpolate data
    
    # copy original data to interpolate
    z_cp = z.copy()
    pO3_cp = pO3.copy()
    pressure_cp = pressure.copy()

    # Remove individual nan's
    ind = ~np.isnan(pO3_cp) & ~np.isnan(pressure_cp)
    z_cp = z_cp[ind]    
    pressure_cp = pressure_cp[ind]
    pO3_cp = pO3_cp[ind]  

    
    if len(Hinf) > 0:
        for i in range(len(Hinf)):
            dH = Hsup[i] - Hinf[i]
            
            if dH <= dHmax:
                pO3_cp = pO3_cp[(z_cp < Hinf[i]) | (z_cp > Hsup[i])]
                pressure_cp = pressure_cp[(z_cp < Hinf[i]) | (z_cp > Hsup[i])]
                z_cp = z_cp[(z_cp < Hinf[i]) | (z_cp > Hsup[i])]
                
                
            else: #dH > dHmax
                pO3_cp[(z_cp >= Hinf[i]) & (z_cp <= Hsup[i])] = np.nan
                pressure_cp[(z_cp >= Hinf[i]) & (z_cp <= Hsup[i])] = np.nan
                z_cp[(z_cp >= Hinf[i]) & (z_cp <= Hsup[i])] = np.nan
            
    
    # Calculate ozone by layers
    dO3 =  3.9449*(pO3_cp[0:-1] + pO3_cp[1:]) * np.log(pressure_cp[0:-1]/pressure_cp[1:])
    # Integrate ozone
    O3_col = np.cumsum(dO3)
    
    # Interpolate ozone column
    O3_f = interp1d(z_cp[0:-1], O3_col, type_intp, bounds_error=False)
    O3_col_intp = O3_f(z_intp)

    
    return O3_col_intp




def interp_serie(z_intp, z, serie, type_intp='linear', prof_val=0, Hinf=[], 
                 Hsup=[], dHmax = 0.3):
    """
    Interpolate vertical profiles to regular altitudes in array z. Return
    profile with nan's if serie does not validate. If it is validate and Hinf 
    and Hsup are not [], there are 2 posibilities:
        - If atmospheric layer depth is less than dHmax (by defeault = 0.3 km), 
          points inside this layer don't be considerated for interpolation
        - If atmospheric layer depth is greater than dHmax (by defeault = 0.3 km), 
          points inside this layer are set to nan's.

    Parameters
    ----------
    z_intp : array
        Array with altitudes where interpolate in [km].
    z : array
        Array with altitudes measured altitudes in [km].
    serie : array
        Measured variable to interpolate.
    type_intp : str, optional
        Type of interpolation. The default is 'linear'.
    prof_val: int or float
        Indicate if serie is validated. If it is not validated, prof_val=0; if
        it is validated, prof_val=1 if is. By defalt prof_val=0
    Hinf: list
        Contains lower limit of atmospheric layers does not validate in [km]. By 
        default is []
    Hsup: list
        Contains upper limit of atmospheric layers does not validate in [km]. By
        default is []
    dHmax: float
        Maximum atmospheric layer depth, in km, to interpolate with missing data

    Returns
    -------
    serie_intp : array
        Variable interpolated to regular altitudes.

    """
    
    # If profile doesn't validated, return profile interpolated with nan's
    if prof_val == 0:
        
        serie_intp = np.nan * np.zeros(len(z_intp))
        
        return serie_intp
    
    
    # If profile is validated, to interpolate data
    
    # copy original data to interpolate
    z_cp = z.copy()
    serie_cp = serie.copy()

    # Remove individual nan's in serie
    z_cp = z_cp[~np.isnan(serie_cp)]    
    serie_cp = serie_cp[~np.isnan(serie_cp)]  
    
    if len(Hinf) > 0:
        for i in range(len(Hinf)):
            dH = Hsup[i] - Hinf[i]
            
            if dH <= dHmax:
                serie_cp = serie_cp[(z_cp < Hinf[i]) | (z_cp > Hsup[i])]
                z_cp = z_cp[(z_cp < Hinf[i]) | (z_cp > Hsup[i])]
                
                
            else: #dH > dHmax
                serie_cp[(z_cp >= Hinf[i]) & (z_cp <= Hsup[i])] = np.nan
                z_cp[(z_cp >= Hinf[i]) & (z_cp <= Hsup[i])] = np.nan
            
    
    # Interpolate data
    serie_f = interp1d(z_cp, serie_cp, type_intp, bounds_error=False)
    serie_intp = serie_f(z_intp)

    
    return serie_intp



def df_to_csv(df_interp, launch_datetime, z0):
    """
    Save dataFrame with sonde data to file .csv

    Parameters
    ----------
    df_interp : DataFrame
        Sonde data interpolated per launch.
    launch_datetime : datetime
        Sounding launch datetime
    z0: float
        Sounding launch altitude 

    Returns
    -------
    None.

    """
    
    
    # Lauch date and launch time to str
    date_str = date.strftime('%Y%m%d')
    time_str = date.strftime('%H:%M')
    # Launch altitude to str
    z0_str = str(z0)
    
    # Filename and path for csv file
    filename_interp = 'RapaNui_'+date_str+'.csv'
    path_fn = os.path.join(path, 'Data_Interpolate', filename_interp)
    
    # Headers: variables and units
    hd1 = ['Alt', 'Press', 'Temp', 'RH', 'O3', 'O3', 'O3', 'uwnd', 'vwnd', 
           'Speed', 'Direction', 'Theta', 'Theta_e', 'MixRatio_H2O']
    hd2 = ['km', 'hPa', 'K', '%', 'mPa', 'ppbv', 'DU', 'm/s', 'm/s', 'm/s', '°', 'K', 'K', 'g/kg']
    
    # Identify newline character for operative system
    if platform.system() == 'Windows':
        nl = '\r\n'
    elif platform.system() == 'Linux':
        nl = '\n'
    elif platform.system() == 'Darwin': #for MAC
        nl = '\r'
    
    # Add header with metadata
    with open(path_fn, 'w') as f:
        f.write('STATION                          : Easter Island (Rapa Nui), Chile' + nl)
        f.write('Data Provider                    : DMC Dirección Meteorológica de Chile, GAW Program (https://woudc.org/)' + nl)
        f.write('Data Compilation                 : 05 April, 2021, by CR2 Center for Climate and Resilience Research. Linearly interpolated data every 100 m' + nl)
        f.write('Latitude (deg)                   : -27.17' + nl)
        f.write('Longitude (deg)                  : -109.42' + nl)
        f.write('Elevation (m)                    : ' + z0_str + nl)
        f.write('Launch Date (YYYYMMDD)           : ' + date_str + nl)
        f.write('Launch Time (UTC)                : ' + time_str + nl)
        f.write('Sonde Instrument, SN             : SPC 6A' + nl)
        f.write('Radiosonde, SN                   : ' + nl)
        f.write('Solution                         : ' + nl)
        f.write('Applied pump corrections         : ' + nl)
        f.write('Pump flow rate (sec/100ml)       : 9000' + nl)
        f.write('Background current (uA)          : 9000' + nl)
        f.write('Missing or bad values            : 9000' + nl)
        f.write('Variables measured by sonde      : Geopotential Height, Pressure, Ozone Partial Pressure, Temperature, Relative Humidity, Wind Speed, Wind Direction' + nl)
        f.write('Variables calculated from data   : Mixing Ratio Ozone by volume, Column Ozone, Zonal and Meridional Winds, Potential Temperature, Equivalent Potential Temperature, Water Vapor Mixing Ratio by mass' + nl)
        f.write(nl)
        
        
    
    # Save headers for variables
    pd.DataFrame([hd1, hd2]).to_csv(path_fn, mode='a', sep='\t', header=False, index=False)
    
    # Save data
    df_clear.to_csv(path_fn, mode='a', sep='\t', header=False)
    
    
    return()





# Read files
# Get path
path = os.getcwd()

# Read data ozonosondes
fn_allsondes = os.path.join(path, 'RapaNui_all_ozonesondes.csv')
dfold = pd.read_csv(fn_allsondes, delimiter=';', index_col=0, parse_dates=True)

# Read dates launch
fn_validate = os.path.join(path, 'RapaNui_dates_valid.csv')
df_validate = pd.read_csv(fn_validate, delimiter=';', index_col=0, parse_dates=True)
# dates for ozonesondes
dates = df_validate.index


# Constants
R=8.314472; #(J/(mol K))
Cp=29.19; #(J/(mol K))


# Height to interpolate, between 0-35 km every 100 m
z = np.arange(0,35.1, 0.1)

# Output filename with all soundings interpolated
fn_clear_all = os.path.join(path, 'RapaNui_all_clear.csv')


# Make dataframe for data complete
dfold_clear = pd.DataFrame()


for date in dates:
    
    # ignore warnings
    warnings.filterwarnings("ignore")
    
    print(date)
    
    # Extract info about validation profiles at date
    val_info = df_validate.loc[date]
    # Ozone
    val_O3 = val_info.Valid_O3
    Hinf_O3 = val_info.Height_inf_O3
    Hsup_O3 = val_info.Height_sup_O3
    # Temperature
    val_T = val_info.Valid_T
    Hinf_T = val_info.Height_inf_T
    Hsup_T = val_info.Height_sup_T
    # Pressure
    val_P = val_info.Valid_P
    Hinf_P = val_info.Height_inf_P
    Hsup_P = val_info.Height_sup_P
    # Relative Humidity
    val_RH = val_info.Valid_RH
    Hinf_RH = val_info.Height_inf_RH
    Hsup_RH = val_info.Height_sup_RH
    # Winds
    val_V = val_info.Valid_V
    Hinf_V = val_info.Height_inf_V
    Hsup_V = val_info.Height_sup_V
    
    
    # If the profile is not repeated, then interpolate
    if val_O3 != -1:
    
        # Correct validate profile value according to validity of ozone profile
        # if ozone profile is not validated, the other variables will not be valid.
        if val_O3 == 0:
            val_T = 0
            val_P = 0
            val_RH = 0
            val_V = 0
        
        # Correct to list
        # Ozone
        if np.isnan(Hinf_O3): Hinf_O3 = []; Hsup_O3 = []
        else: Hinf_O3 = [Hinf_O3]; Hsup_O3 = [Hsup_O3]
        # Temperature
        if np.isnan(Hinf_T): Hinf_T = []; Hsup_T = []
        else: Hinf_T = [Hinf_T]; Hsup_T = [Hsup_T]
        # Pressure
        if np.isnan(Hinf_P): Hinf_P = []; Hsup_P = []
        else: Hinf_P = [Hinf_P]; Hsup_P = [Hsup_P]
        # Relative Humidity
        if np.isnan(Hinf_RH): Hinf_RH = []; Hsup_RH = []
        else: Hinf_RH = [Hinf_RH]; Hsup_RH = [Hsup_RH]
        # Winds
        if np.isnan(Hinf_V): Hinf_V = []; Hsup_V = []
        else: Hinf_V = [Hinf_V]; Hsup_V = [Hsup_V]
        
    
        # Extract data at date
        df = dfold.loc[date]
        
        # Check if height is monotonic increasing. If is not monotonic, remove
        # rows associated to those data
        if (df.GPHeight.is_monotonic_increasing and df.GPHeight.is_unique):
            pass
        else:
            df = remov_desc(df)
    
        
        #Lecture of Data
        GPHeight = df.GPHeight.values*10**-3
        Pressure = df.Pressure.values
        O3PartialPressure = df.O3PartialPressure.values
        Temperature = df.Temperature.values
        RelativeHumidity = df.RelativeHumidity.values
        Wind_Speed = df.WindSpeed.values
        Wind_Direction = df.WindDirection.values
        
       
        #Determination and Interpolation
        
        # Pressure interp
        Pressure_interp = interp_serie(z, GPHeight, Pressure, prof_val=val_P, Hinf=Hinf_P, Hsup=Hsup_P)
        
        # Temperature to interpolate
        Temperature_K = Temperature + 273.15
        Temperature_K_interp = interp_serie(z, GPHeight, Temperature_K, prof_val=val_T, Hinf=Hinf_T, Hsup=Hsup_T)
        
        # Relative Humidity to interpolate
        RelativeHumidity_interp = interp_serie(z, GPHeight, RelativeHumidity, prof_val=val_RH, Hinf=Hinf_RH, Hsup=Hsup_RH)
        
        # Potential Temperature
        val_Theta = min(val_T, val_P)
        Hinf_Theta = list(set(Hinf_T + Hinf_P))
        Hsup_Theta = list(set(Hsup_T + Hsup_P))
        
        T_potencial = Temperature_K*(1000/Pressure)**(R/Cp)
        T_potencial_interp = interp_serie(z, GPHeight, T_potencial, prof_val=val_Theta, Hinf=Hinf_Theta, Hsup=Hsup_Theta)
        
        
        # Mixing ratio H2O [g/kg]
        val_W = min(val_RH, val_T, val_P)
        Hinf_W = list(set(Hinf_T + Hinf_P + Hinf_RH))
        Hsup_W = list(set(Hsup_T + Hsup_P + Hsup_RH))
        
        Satured_Vapor_Pressure = 6.11*np.exp(5.42*10**3*(1/273-1/Temperature_K))
        Satured_Mixing_Ratio = 0.622*(Satured_Vapor_Pressure/(Pressure-Satured_Vapor_Pressure))
        Mixing_Ratio = 1e3*(RelativeHumidity/100)*Satured_Mixing_Ratio
        
        Mixing_Ratio_interp = interp_serie(z, GPHeight, Mixing_Ratio, prof_val=val_W, Hinf=Hinf_W, Hsup=Hsup_W)
    
        
        # Equivalent Potential Temperature (Stull 1988, p.546)
        val_Thetae = min(val_T, val_P, val_RH)
        Hinf_Thetae = list(set(Hinf_T + Hinf_P + Hinf_RH))
        Hsup_Thetae = list(set(Hsup_T + Hsup_P + Hsup_RH))
        
        T_potencial_e = (Temperature_K + (2.5e6/1005)*Mixing_Ratio*1e-3)*((1000/Pressure)**(287.04/1005))
        T_potencial_e_interp = interp_serie(z, GPHeight, T_potencial_e, prof_val=val_Thetae, Hinf=Hinf_Thetae, Hsup=Hsup_Thetae)
        
        
        # Winds to interpolate
        # CAlculate zonal and meridional components
        U = - Wind_Speed*np.sin((np.pi/180)*Wind_Direction) 
        V = - Wind_Speed*np.cos((np.pi/180)*Wind_Direction)
        
        U_interp = interp_serie(z, GPHeight, U, prof_val=val_V, Hinf=Hinf_V, Hsup=Hsup_V)
        V_interp = interp_serie(z, GPHeight, V, prof_val=val_V, Hinf=Hinf_V, Hsup=Hsup_V)
        
        # Calculate magnitude and direction
        Wind_Speed_interp = np.sqrt(U_interp**2 + V_interp**2)
        Wind_Direction_interp = np.arctan2(-U_interp, -V_interp) * (180/np.pi)
        Wind_Direction_interp[Wind_Direction_interp < 0] = Wind_Direction_interp[Wind_Direction_interp<0] + 360
        
        
        # Ozone
        # Ozone partial pressure
        O3PartialPressure_interp = interp_serie(z, GPHeight, O3PartialPressure, prof_val=val_O3, Hinf=Hinf_O3, Hsup=Hsup_O3)
        
        # Ozone mixing ratio by volume [ppbv]
        val_O3ppbv = min(val_O3, val_P)
        Hinf_O3ppbv = list(set(Hinf_O3 + Hinf_P))
        Hsup_O3ppbv = list(set(Hsup_O3 + Hsup_P))
        
        O3_ppbv = (O3PartialPressure*10**-3)/ (Pressure*10**2)*10**9
        O3_ppbv_interp = interp_serie(z, GPHeight, O3_ppbv, prof_val=val_O3ppbv, Hinf=Hinf_O3ppbv, Hsup=Hsup_O3ppbv)
        
        # Ozone column
        val_O3col = min(val_O3, val_P)
        Hinf_O3col = list(set(Hinf_O3 + Hinf_P))
        Hsup_O3col = list(set(Hsup_O3 + Hsup_P))
        
        Sum_Omega_S_interp = ozone_column(O3PartialPressure, Pressure, GPHeight, z, prof_val=val_O3col, Hinf=Hinf_O3, Hsup=Hsup_O3)
        
        
        
        # Make dataframe with variables
        df_clear = pd.DataFrame(data={'Pressure':Pressure_interp,'Temp':Temperature_K_interp, 
                                      'RH':RelativeHumidity_interp, 'O3_mPa': O3PartialPressure_interp,
                                      'O3_ppbv':O3_ppbv_interp, 'O3_column':Sum_Omega_S_interp,
                                      'U':U_interp, 'V':V_interp, 'WndSpd' : Wind_Speed_interp,
                                      'WndDir' : Wind_Direction_interp, 'Theta':T_potencial_interp,
                                      'Theta_e':T_potencial_e_interp, 'Mixing_Ratio':Mixing_Ratio_interp}, 
                                index=z)
        df_clear.index.rename('Alt', inplace=True)
        
        # Change nan to 9000
        df_clear.fillna(9000, inplace=True)
        
        # Round values in dataframe
        df_clear.index = np.around(df_clear.index, 1)
        df_clear['Pressure'] = df_clear['Pressure'].map('{:.3f}'.format)
        df_clear['Temp'] = df_clear['Temp'].map('{:.3f}'.format)
        df_clear['RH'] = df_clear['RH'].map('{:.3f}'.format)
        df_clear['O3_mPa'] = df_clear['O3_mPa'].map('{:.3f}'.format)
        df_clear['O3_ppbv'] = df_clear['O3_ppbv'].map('{:.3f}'.format)
        df_clear['O3_column'] = df_clear['O3_column'].map('{:.3f}'.format)
        df_clear['U'] = df_clear['U'].map('{:.3f}'.format)
        df_clear['V'] = df_clear['V'].map('{:.3f}'.format)
        df_clear['WndSpd'] = df_clear['WndSpd'].map('{:.3f}'.format)
        df_clear['WndDir'] = df_clear['WndDir'].map('{:.3f}'.format)
        df_clear['Theta'] = df_clear['Theta'].map('{:.3f}'.format)
        df_clear['Theta_e'] = df_clear['Theta_e'].map('{:.3f}'.format)
        df_clear['Mixing_Ratio'] = df_clear['Mixing_Ratio'].map('{:.5f}'.format)
        
        
        # Save sounding interpolated
        df_to_csv(df_clear, date, 1e3*GPHeight[0])
        
        
        
        # Add ozonesonde to dataframe with all soundings
        df_clear2 = df_clear.copy()
        
        # Make index datetime
        N = len(z)
        time = []
        for i in range(N):
            time.append(date)
        time = pd.to_datetime(time)
        time.name ='Datetime'
        
        # Add multi index to dataframe [datetime, altitude]
        df_clear2.set_index([time, df_clear2.index], inplace=True)
        
        # Add to dataframe complete
        dfold_clear = pd.concat([dfold_clear, df_clear2])
                

    
# Save in .csv all ozonesondes interpolated
dfold_clear.replace(to_replace=9000, value=np.nan, inplace=True)
dfold_clear.to_csv(fn_clear_all, sep=';')
