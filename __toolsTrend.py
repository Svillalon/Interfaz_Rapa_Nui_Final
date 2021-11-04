#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 01:04:04 2021

@author: cmenares
"""

import numpy as np
#from Data_config_Sinca import * # mutear si es cargado dataframe
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
from scipy.optimize import leastsq
import pandas as pd
from PyEMD import EEMD


def plot_regression(pu , pu_m,t,x,error,titulo,trend = True):
        
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams['xtick.labelsize'] = 22
    plt.rcParams['ytick.labelsize'] = 22

    pu_m_aux  = pu_m.fillna(pu_m.mean())
    ress = np.nanmean(np.abs(model(t, x)-pu_m.values))   
    corr = np.corrcoef(model(t, x),pu_m_aux.values)[0,1]
    plt.figure(figsize=(10,4))
    ax = plt.subplot(1,1,1)
    
    plt.title(titulo, fontsize=18, fontweight="bold")
    plt.plot(pu_m.index  , pu_m.values,'-o',color='black',linewidth=2.0,  markersize=2.5, label='Obs')
    plt.plot( pu_m.index , model(t, x),':',color='blue',linewidth=2.0, label='Regression')
    
    plt.xlabel('Month',fontsize=16)
    plt.ylabel('PM$_{2.5}$ $\mu g/m^3$',fontsize=16)
    plt.legend(loc='upper center',ncol=3,frameon=False, fontsize=14)
    
    plt.fill_between(pu_m.index, pu_m.resample('M').mean() , pu.resample('M').quantile(0.25),facecolor='gray', alpha=0.21) ;    
    plt.fill_between(pu_m.index, pu.resample('M').mean()   , pu.resample('M').quantile(0.75),facecolor='gray', alpha=0.21) ;    
    
    # quantile(0.75)*(pu.PM25.resample('M').std()/len(pu.PM25.resample('M'))) intervalo de confianza
    if trend == True:
   
        anchored_text = AnchoredText( "Correlation ="+ str(round(corr,2)) +
                                     "\nResidual="+str(round(ress,2))+ ' $\mu g/m^3$' +
                                    "\nDecadal Trend ="+ str(round(x[1]*10*12,2)) + '$\pm$' + str(round(error,2)*10) + ' $\mu g/m^3$', prop=dict(size=12), loc=1)
        
    else : 

        anchored_text = AnchoredText( "Residual="+str(round(ress,2))+ ' $\mu g/m^3$' +
                                 "\nCorrelation ="+ str(round(corr,2))
                                 , prop=dict(size=12), loc=1)
    
    ax.add_artist(anchored_text)
    plt.tight_layout()

    return



def plot_m(pu , pu_m, titulo):
        
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams['xtick.labelsize'] = 22
    plt.rcParams['ytick.labelsize'] = 22

    pu_m_aux  = pu_m.fillna(pu_m.mean())
    plt.figure(figsize=(20,10))
    ax = plt.subplot(1,1,1)
    
    plt.suptitle(titulo, fontsize=34)
    plt.plot(pu_m.index  , pu_m.values,'-o',color='black',linewidth=3.0,  markersize=2.5, label='Obs')
    
    plt.xlabel('Month',fontsize=20)
    plt.ylabel('PM$_{2.5}$ $\mu g/m^3$',fontsize=20)
    plt.legend(loc='upper center',ncol=3,frameon=False, fontsize=20)
    
    plt.fill_between(pu_m.index, pu_m.resample('M').mean() , pu.resample('M').quantile(0.25),facecolor='gray', alpha=0.18) ;    
#    plt.fill_between(pu_m.index, pu_m.resample('M').mean() , pu.resample('M').quantile(0.05),facecolor='gray', alpha=0.18) ;    

    plt.fill_between(pu_m.index, pu.resample('M').mean()   , pu.resample('M').quantile(0.75),facecolor='gray', alpha=0.18) ;    
#    plt.fill_between(pu_m.index, pu.resample('M').mean()   , pu.resample('M').quantile(0.95),facecolor='gray', alpha=0.18) ;    
    
    # quantile(0.75)*(pu.PM25.resample('M').std()/len(pu.PM25.resample('M'))) intervalo de confianza
    plt.tight_layout()

    return




####################### Regressions #####################################
#####################################################################

from scipy.optimize import leastsq
from PyEMD import EMD


def Linear_trend_lastq(s):

    def model(t, coeffs):
       return  coeffs[0] + coeffs[1]*t
    
    
    def residuals(coeffs, y, t):
        return y - model(t, coeffs)
    
    
    x0 = np.array([1, 1 ], dtype=float)
    
    t = np.arange(len(s))
    x, flag = leastsq(residuals, x0, args=(s, t))
    y = model(t,x)
    trend = (y[-1] - y[0])/len(y)
    
    return y , trend
    

def emd_trend(s):

    IMF = EMD().emd(s)
    N = IMF.shape[0]+1
    
    y = IMF[N-2,:]
#    trend = (y[-1] - y[0])/len(y)
    trend = np.nanmean(np.diff(y))
    
    return y , trend


def eemd_trend(s):
    
    # Assign EEMD to `eemd` variable
    eemd = EEMD()
    
    # Say we want detect extrema using parabolic method
    emd = eemd.EMD
    emd.extrema_detection="parabol"
    eIMFs = eemd.eemd(s)
    N   = eIMFs.shape[0] 
    
    y = eIMFs[N-2,:]
#    trend = (y[-1] - y[0])/len(y)
    trend = np.nanmean(np.diff(y))
    
    return y , trend



def lamsal_trend(s):

    
    def model(t, coeffs):
       return  (coeffs[0] + coeffs[1]*t + coeffs[2]*np.sin(2*np.pi*t/12) + coeffs[3]*np.cos(2*np.pi*t/12) +
                coeffs[4]*np.sin(4*np.pi*t/12) + coeffs[5]*np.cos(4*np.pi*t/12) + 
                coeffs[6]*np.sin(6*np.pi*t/12) + coeffs[7]*np.cos(6*np.pi*t/12) +
                coeffs[8]*np.sin(8*np.pi*t/12) + coeffs[9]*np.cos(8*np.pi*t/12) +
                coeffs[10]*np.sin(10*np.pi*t/12) + coeffs[11]*np.cos(10*np.pi*t/12) +
                coeffs[12]*np.sin(12*np.pi*t/12) + coeffs[13]*np.cos(12*np.pi*t/12) +
                coeffs[14]*np.sin(14*np.pi*t/12) + coeffs[15]*np.cos(14*np.pi*t/12) +
                coeffs[15]*np.sin(16*np.pi*t/12) + coeffs[16]*np.cos(16*np.pi*t/12) +
                coeffs[17]*np.sin(18*np.pi*t/12) + coeffs[18]*np.cos(18*np.pi*t/12) 
    )
    
    def residuals(coeffs, y, t):
        return y - model(t, coeffs)
    
    
    
    x0 = np.array([1, 1 ,1, 1,1 ,1,1,1,1,1,1,1,1,1,1,1,1,1,1], dtype=float)
    
    t = np.arange(len(s))
    x, flag = leastsq(residuals, x0, args=(s, t))
    y = model(t,x)
    y = x[0] + x[1]*t 
    trend = x[1]*1.00
    
    return y , trend


def cooper_trend(s):

    
    def model(t, coeffs):
       return  (coeffs[0] + coeffs[1]*t + coeffs[2]*np.sin(2*np.pi*t/12) + coeffs[3]*np.cos(2*np.pi*t/12) +
                coeffs[4]*np.sin(4*np.pi*t/12) + coeffs[5]*np.cos(4*np.pi*t/12) + 
                coeffs[6]*np.sin(6*np.pi*t/12) + coeffs[7]*np.cos(6*np.pi*t/12) +
                coeffs[8]*np.sin(8*np.pi*t/12) + coeffs[9]*np.cos(8*np.pi*t/12) +
                coeffs[10]*np.sin(10*np.pi*t/12) + coeffs[11]*np.cos(10*np.pi*t/12) +
                coeffs[12]*np.sin(12*np.pi*t/12) 
    )
    
    def residuals(coeffs, y, t):
        return y - model(t, coeffs)
    
    
    
    x0 = np.array([1, 1 ,1, 1,1 ,1,1,1,1,1,1,1,1,1,1,1,1,1,1], dtype=float)
    
    t = np.arange(len(s))
    x, flag = leastsq(residuals, x0, args=(s, t))
    y = model(t,x)
#    y = x[0] + x[1]*t 
    trend = x[1]*0.9
    y = t*trend+ x[0]
    
    return y , trend
 

def stl_trend(s_df):

    from statsmodels.tsa.seasonal import STL
    stl = STL(s_df, seasonal=15)
    res = stl.fit()

    y = res.trend
#    trend = (y[-1] - y[0])/len(y)
    trend = np.nanmean(np.diff(y))

    return res.trend , trend


from sklearn.linear_model import LinearRegression, TheilSenRegressor

def TheillSen_trend(s) :
    t = np.arange(len(s))
    X = t[:, np.newaxis]
    
    reg = TheilSenRegressor(random_state=0).fit(X, s)
    y =  reg.predict(X)

#    trend = (y[-1] - y[0])/len(y)
    trend = np.nanmean(np.diff(y))

    return y , trend



def linear_trend(s) :
    t = np.arange(len(s))
    X = t[:, np.newaxis]
    
    reg = LinearRegression().fit(X, s)
    y =  reg.predict(X)

#    trend = (y[-1] - y[0])/len(y)
    trend = np.nanmean(np.diff(y))

    return y , trend
    
    
############################################################## Tiao##################################################################

def tiao(mod,obs) : 
    """
    Tiao et al 1990 https://doi.org/10.1029/JD095iD12p20507
    http://stackoverflow.com/q/14297012/190597
    http://en.wikipedia.org/wiki/Autocorrelation#Estimation
    """
    
    def autocorr(x):
        x = pd.Series(x)
        n = len(x)
        variance = x.var()
        x = x-x.mean()
        r = np.correlate(x, x, mode = 'full')[-n:]
        result = r/(variance*(np.arange(n, 0, -1)))
        return result

    
    residuo = obs - mod
    Tiao  = (1-autocorr(mod)[1])**(-1/2)*np.std(residuo)*0.023/12      
    
    return Tiao
        
    


