#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 02:09:07 2021

@author: charlie opazo

Make a file with all trajectories generated by hysplit for Rapa Nui.
The trajectories are in fold /Trajectories/ with format: 
RP_bt_{year}{month}{day}{hour}_{level}

The output file will be "RapaNui_BackTrajectories.csv". This will have:
    - Launch Date and Time
    - Arrival Height to Rapa Nui [m]
    - DateTime in every time step
    - Longitude [°]
    - Latitude [°]
    - Height above mean sea level [m]

This code use pysplit package. It allows read trajectory files generated by
hysplit.

Pysplit is compatible with Python 2.7, 3.6, and 3.7. To install pysplit:
https://github.com/mscross/pysplit

"""

# Import libraries
import numpy as np
import pandas as pd
import pysplit
import os


# Get path and filenames
path = os.getcwd()# use your path
prefix_files = 'RN_bt_*'
fn = os.path.join(path, 'Trajec', prefix_files)

# Output file
out_file = "RapaNui_BackTrajectories.csv"

# Load trajectories with pysplit functions
trajgroup = pysplit.make_trajectorygroup(fn)


# Make dataframe for to save all trajectories in one file .csv
dfold = pd.DataFrame()

# Year of correction to fix trajectory date
yr_correc = 2020

# For every trajectory, make a dataframe and add to dfold
for traj in trajgroup:
    
    # Correct datetime for trajectories release before 2000
    datetime = pd.Index(traj.data.DateTime)
    if datetime[0].year > yr_correc:
        datetime = pd.to_datetime(datetime.strftime('%y %m %d %H'))
    
    # Extract lon, lat and altitude from data
    lon = traj.data.geometry.x
    lat = traj.data.geometry.y
    z = traj.data.geometry.z
    
    # Make dataframe per trajectorie
    df = pd.DataFrame({'Latitude': lat, 'Longitude' : lon, 'Altitude' : z})    
    
    # Set index for df: index=['Launch Datetime', 'Arrival_Altitude, 'Datetime']
    df.set_index([np.repeat(datetime[0], df.shape[0]), np.repeat(z[0], df.shape[0]),
                  datetime], inplace=True)
    df.index.set_names(['Launch_Datetime', 'Arrival_Altitude', 'DateTime'], inplace=True)
    
    # Concatenate df with dfold
    dfold = pd.concat([dfold, df])
    
    


# Sort DataFrame by sounding date and arrival height
dfold.sort_index(level=[0,1], inplace=True, sort_remaining=False)

    
# Round and fix decimals
dfold['Latitude'] = dfold['Latitude'].map('{:.3f}'.format)
dfold['Longitude'] = dfold['Longitude'].map('{:.3f}'.format)
dfold['Altitude'] = dfold['Altitude'].map('{:.1f}'.format)
    

# Save all trajectories in one file .csv
dfold.to_csv(out_file, sep=';')