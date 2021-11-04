#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 11:32:58 2021

@author: charlie opazo and sebastian villalon

Reading and plotting Rapa Nui ozonesondes data per launch: ozone [mPa], 
temperature [K], relative humidity [%], wind speed [m/s] and wind direction [°].

In file 'RapaNui_dates_valid.csv', must be indicated which ozone profiles are 
validated by visual inspection.

"""

# Import libraries
import pandas as pd              # Data structures
import numpy as np
import matplotlib.pyplot as plt  # Plotting
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import ScalarFormatter
import os as os                  # Directory management
import platform


def plot_sonde(df, date, station, save=False, path_to_save=None):
    """
    Plot sonde data for a date.
    
    Parameters
    ----------
    df : DataFrame
        DataFrame with sounding data.
    date: datetime
        Lauch datetime
    station: str
        Lauch station
    save : bool, optional
        Indicates if you want to look at the graph. The default is False.
    path_to_save: bool, optional
        Path where to save plot

    Returns
    -------
    None.

    """
    
    
    # Extract variables 
    Temp = df.Temperature + 273.15
    O3 = df.O3PartialPressure
    HR = df.RelativeHumidity
    Pres = df.Pressure
    WSpd = df.WindSpeed
    WDir = df.WindDirection
            
    z = 1e-3 * df.GPHeight


        
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(7.5,6.2), sharey=True)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.08, top=0.84, wspace=0.15)
    
    # Ozone Partial Pressure
    ax1.plot(O3[~np.isnan(O3)], z[~np.isnan(O3)], color='b', marker='.', markersize=1, linestyle='-', linewidth=0.3)
    ax1.set_ylim(ymin=0, ymax=40)
    ax1.set_xlim(xmin=0, xmax=28)
    ax1.yaxis.set_minor_locator(MultipleLocator(1))
    ax1.set_xticks(np.arange(0, 30, 5))
    ax1.set_xlabel(r'Ozone [mPa]', color='b')
    ax1.set_ylabel('Altitude [km]')
    ax1.spines['bottom'].set_color('#dddddd')
    ax1.tick_params(axis='x', colors='b')
    
    # Temperature
    ax1_2 = ax1.twiny()
    ax1_2.plot(Temp[~np.isnan(Temp)], z[~np.isnan(Temp)], color='r', marker='.', markersize=1, linestyle='-', linewidth=0.3)
    ax1_2.set_xlim(xmin=190, xmax=310)
    ax1_2.set_xticks(np.arange(190, 311, 30))
    ax1_2.set_xlabel('Temperature [K]', color='r')
    ax1_2.spines['top'].set_color('r')
    ax1_2.tick_params(axis='x', colors='r')
    
    
    # Relative Humidity
    ax2.plot(HR[~np.isnan(HR)], z[~np.isnan(HR)], color='b', marker='.', markersize=1, linestyle='-', linewidth=0.3)
    ax2.set_xlim(xmin=0, xmax=100)
    ax2.set_xlabel(r'Relative Humidity [%]', color='b')
    ax2.spines['bottom'].set_color('b')
    ax2.tick_params(axis='x', colors='b')
    
    # Pressure
    ax2_2 = ax2.twiny()
    ax2_2.plot(Pres[~np.isnan(Pres)], z[~np.isnan(Pres)], color='r', marker='.', markersize=1, linestyle='-', linewidth=0.3)
    ax2_2.set_xlim(xmin=1, xmax=1025)
    ax2_2.set_xscale('log')
    ax2_2.set_xticks([1, 10, 100, 1000])
    ax2_2.get_xaxis().set_major_formatter(ScalarFormatter())
    ax2_2.set_xlabel(r'Pressure [hPa]', color='r')
    ax2_2.spines['top'].set_color('r')
    ax2_2.tick_params(axis='x', colors='r')
    
    
    # Wind Speed
    ax3.plot(WSpd[~np.isnan(WSpd)], z[~np.isnan(WSpd)], color='b', marker='.', markersize=1, linestyle='-', linewidth=0.3)
    ax3.set_xlim(xmin=0, xmax=80)
    ax3.set_xticks(np.arange(0, 81, 20))
    ax3.set_xlabel(r'Wind Speed [m/s]', color='b')
    ax3.spines['bottom'].set_color('b')
    ax3.tick_params(axis='x', colors='b')
    
    # Wind Direction
    ax3_2 = ax3.twiny()
    ax3_2.plot(WDir[~np.isnan(WDir)], z[~np.isnan(WDir)], color='r', marker='.', markersize=1, linestyle='-', linewidth=0.3)
    ax3_2.set_xlim(xmin=0, xmax=360)
    ax3_2.set_xticks(np.arange(0, 361, 90))
    ax3_2.set_xlabel(r'Wind Direction [°]', color='r')
    ax3_2.spines['top'].set_color('r')
    ax3_2.tick_params(axis='x', colors='r')



    # Date to string
    date_str = date.strftime('%Y-%m-%d')
    
    # Identify newline character for operative system
    if platform.system() == 'Windows':
        nl = '\r\n'
    elif platform.system() == 'Linux':
        nl = '\n'
    elif platform.system() == 'Darwin': #for MAC
        nl = '\r'
    
    
    # Add suptitle
    fig.suptitle(station+nl+'Date : '+date_str, fontsize=14)
    
    # Save figure
    if save == True:
        fig_name = os.path.join(path_to_save, station+'_'+date_str+".png")
        fig.savefig(fig_name, dpi=400)    

    return()




# Get path
path = os.getcwd()

# Path to save figures
path_save= os.path.join(path, "Graphs_Inspection_Valid")

# Read data ozonosondes
fn_sondes = os.path.join(path, "RapaNui_all_ozonesondes.csv")
dfold = pd.read_csv(fn_sondes, delimiter=';', index_col=0, parse_dates=True)

# Sounding datess
dates = dfold.index.drop_duplicates()

# Estacion
station = 'Rapa Nui'

# years to be plotted
yi = 1994
yf = 2020

# Iterations for make plots per launch
for date in dates:
    if date.year in range(yi, yf+1):
        
        # extract profile per date
        df = dfold.loc[date]
        
        # plot
        plot_sonde(df, date, station, save=True, path_to_save=path_save)
        
        plt.close('all')
       
        
