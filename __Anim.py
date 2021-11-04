import plotly.graph_objects as go # or plotly.express as px
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import os as os
import pandas as pd


def AnimENG(ozonosondes_data, encoded_image_cr2_celeste, encoded_image_DMC, 
            encoded_image_GWA, ozonosondes_climatology_90, ozonosondes_climatology_70,
                       ozonosondes_climatology_30, ozonosondes_climatology_10, 
                       ozonosondes_climatology_mean):


    df = ozonosondes_data.copy()
    df.index = df.index.map(str)
    
    dates = [i for i in df.index[df.index.duplicated()==False]]
    # make list of continents
    
    
    ################################# configuracion layout ######################
    # make figure
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }
    
    # fill in most of layout
    fig_dict["layout"]["xaxis"] = {"range": [0, 20], "title": "O3 [mPa]"}
    fig_dict["layout"]["yaxis"] = {"range":[0,36],"title": "Height [Km]",}
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 500, "redraw": False},
                                    "fromcurrent": True, "transition": {"duration": 300,
                                                                        "easing": "quadratic-in-out"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]
    
    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Date:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }
    
    # make data
    date = dates[0]
    ozone_data= ozonosondes_data[ozonosondes_data.index==date]
    
    data_dict = {
            "x": list(ozone_data.O3_mPa),
            "y": list(ozone_data["Alt"]),
            "mode": "markers",
            "text": "AAAA",
            "marker": {
                "sizemode": "area",
                #"sizeref": 200000,
                #"size": 10
            },
            "name": "Sounding"
        }
    fig_dict["data"].append(data_dict)
    
    # make frames
    for dates in dates:
        frame = {"data": [], "name": str(dates)}
        ozone_data= ozonosondes_data[ozonosondes_data.index==dates]
    
        data_dict = {
                "x": list(ozone_data.O3_mPa),
                "y": list(ozone_data["Alt"]),
                "mode": "markers",
                "text": "AA",
                "marker": {
                    "sizemode": "area",
                    #"sizeref": 200000,
                    #"size": "10"
                },
                "name": "Sounding"
            }
        frame["data"].append(data_dict)
    
        fig_dict["frames"].append(frame)
        slider_step = {"args": [
            [dates],
            {"frame": {"duration": 0, "redraw": False},
             "mode": "immediate",
             "transition": {"duration": 0}}
        ],
            "label": dates,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)
    
    
    fig_dict["layout"]["sliders"] = [sliders_dict]
    
    fig = go.Figure(fig_dict)
    fig.update_layout(
            width=540,
            height=400,
            autosize=False,
            margin=dict(t=25, b=0, l=0, r = 0),
            title_font_family="Times New Roman",
    #        title_font_color="red",        
            title_font_size=30,
            title_font_color = 'dimgray',
            plot_bgcolor='#f6f6f6',
            paper_bgcolor='#f6f6f6',
            titlefont=dict(size=14,color='black'),
            # xaxis_title=xlabel,
            # yaxis_title=ylabel,
            )
    fig.add_trace(
        go.Scatter(
            name="90%",legendgroup='90%',
            x=ozonosondes_climatology_90.O3_mba,
            y=ozonosondes_climatology_90.index,
            marker=dict(color="#444"),
            line=dict(width=0),
             mode='lines',
            
        )
        )
    
    fig.add_trace(
        go.Scatter(
        x=ozonosondes_climatology_10.O3_mba,
        y=ozonosondes_climatology_10.index,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
         name="10%",legendgroup='10%')
        
        )
    
    fig.add_trace(
        go.Scatter(
            name="30%",legendgroup='30%',
            x=ozonosondes_climatology_30.O3_mba,
            y=ozonosondes_climatology_30.index,
            marker=dict(color="#444"),
            line=dict(width=0),
             mode='lines',
            
        )
        )
    
    fig.add_trace(
        go.Scatter(
        name="70%",legendgroup='70%',
        x=ozonosondes_climatology_70.O3_mba,
        y=ozonosondes_climatology_70.index,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty')
        
        )
    
    fig.add_trace(
        go.Scatter(x=ozonosondes_climatology_mean.O3_mba, y=ozonosondes_climatology_mean.index
        ,showlegend=False, line_color='red',  name="Promedio",legendgroup='Promedio')
        )
    fig.update_layout(
            images= [       dict(
                    source='data:image/png;base64,{}'.format(encoded_image_cr2_celeste),
                    xref="paper", yref="paper",
                    x=0.25, y=1.0,
                    sizex=0.2, sizey=0.2,
                    xanchor="right",
                    yanchor="bottom",
                    #sizing="stretch",
                    layer="above")    ,dict(
                    source='data:image/png;base64,{}'.format(encoded_image_DMC),
                    xref="paper", yref="paper",
                    x=0.58, y=1.05,
                    sizex=0.15, sizey=0.15,
                    xanchor="right",
                    yanchor="bottom",
                    #sizing="stretch",
                    layer="above"), dict(
                    source='data:image/png;base64,{}'.format(encoded_image_GWA),
                    xref="paper", yref="paper",
                    x=0.95, y=1.05,
                    sizex=0.17, sizey=0.17,
                    xanchor="right",
                    yanchor="bottom",
                    #sizing="stretch",
                    layer="above")])
    
    # update layout properties
    fig.update_layout(
        autosize=False,
        height=480,
        width=540,
        bargap=0.15,
        bargroupgap=0.1,
        barmode="stack",
        hovermode="x",
        margin=dict(t=100, b=10, l=10, r = 10),
    )
    return fig

def AnimESP(ozonosondes_data, encoded_image_cr2_celeste, encoded_image_DMC, 
            encoded_image_GWA, ozonosondes_climatology_90, ozonosondes_climatology_70,
                       ozonosondes_climatology_30, ozonosondes_climatology_10, 
                       ozonosondes_climatology_mean):


    df = ozonosondes_data.copy()
    df.index = df.index.map(str)
    
    dates = [i for i in df.index[df.index.duplicated()==False]]
    # make list of continents
    
    
    ################################# configuracion layout ######################
    # make figure
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }
    
    # fill in most of layout
    fig_dict["layout"]["xaxis"] = {"range": [0, 20], "title": "O3 [mPa]"}
    fig_dict["layout"]["yaxis"] = {"range":[0,36],"title": "Altura [Km]",}
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 500, "redraw": False},
                                    "fromcurrent": True, "transition": {"duration": 300,
                                                                        "easing": "quadratic-in-out"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]
    
    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Date:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }
    
    # make data
    date = dates[0]
    ozone_data= ozonosondes_data[ozonosondes_data.index==date]
    
    data_dict = {
            "x": list(ozone_data.O3_mPa),
            "y": list(ozone_data["Alt"]),
            "mode": "markers",
            "text": "AAAA",
            "marker": {
                "sizemode": "area",
                #"sizeref": 200000,
                #"size": 10
            },
            "name": "Sondeo"
        }
    fig_dict["data"].append(data_dict)
    
    # make frames
    for dates in dates:
        frame = {"data": [], "name": str(dates)}
        ozone_data= ozonosondes_data[ozonosondes_data.index==dates]
    
        data_dict = {
                "x": list(ozone_data.O3_mPa),
                "y": list(ozone_data["Alt"]),
                "mode": "markers",
                "text": "AA",
                "marker": {
                    "sizemode": "area",
                    #"sizeref": 200000,
                    #"size": "10"
                },
                "name": "Sondeo"
            }
        frame["data"].append(data_dict)
    
        fig_dict["frames"].append(frame)
        slider_step = {"args": [
            [dates],
            {"frame": {"duration": 0, "redraw": False},
             "mode": "immediate",
             "transition": {"duration": 0}}
        ],
            "label": dates,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)
    
    
    fig_dict["layout"]["sliders"] = [sliders_dict]
    
    fig = go.Figure(fig_dict)
    fig.update_layout(
            width=540,
            height=600,
            autosize=False,
            margin=dict(t=25, b=0, l=0, r = 0),
            title_font_family="Times New Roman",
    #        title_font_color="red",        
            title_font_size=30,
            title_font_color = 'dimgray',
            plot_bgcolor='#f6f6f6',
            paper_bgcolor='#f6f6f6',
            titlefont=dict(size=14,color='black'),
            # xaxis_title=xlabel,
            # yaxis_title=ylabel,
            )
    fig.add_trace(
        go.Scatter(
            name="90%",legendgroup='90%',
            x=ozonosondes_climatology_90.O3_mba,
            y=ozonosondes_climatology_90.index,
            marker=dict(color="#444"),
            line=dict(width=0),
             mode='lines',
            
        )
        )
    
    fig.add_trace(
        go.Scatter(
        x=ozonosondes_climatology_10.O3_mba,
        y=ozonosondes_climatology_10.index,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
         name="10%",legendgroup='10%')
        
        )
    
    fig.add_trace(
        go.Scatter(
            name="30%",legendgroup='30%',
            x=ozonosondes_climatology_30.O3_mba,
            y=ozonosondes_climatology_30.index,
            marker=dict(color="#444"),
            line=dict(width=0),
             mode='lines',
            
        )
        )
    
    fig.add_trace(
        go.Scatter(
        name="70%",legendgroup='70%',
        x=ozonosondes_climatology_70.O3_mba,
        y=ozonosondes_climatology_70.index,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty')
        
        )
    
    fig.add_trace(
        go.Scatter(x=ozonosondes_climatology_mean.O3_mba, y=ozonosondes_climatology_mean.index
        ,showlegend=False, line_color='red',  name="Promedio",legendgroup='Promedio')
        )
    fig.update_layout(
            images= [       dict(
                    source='data:image/png;base64,{}'.format(encoded_image_cr2_celeste),
                    xref="paper", yref="paper",
                    x=0.25, y=1.0,
                    sizex=0.2, sizey=0.2,
                    xanchor="right",
                    yanchor="bottom",
                    #sizing="stretch",
                    layer="above")    ,dict(
                    source='data:image/png;base64,{}'.format(encoded_image_DMC),
                    xref="paper", yref="paper",
                    x=0.58, y=1.05,
                    sizex=0.15, sizey=0.15,
                    xanchor="right",
                    yanchor="bottom",
                    #sizing="stretch",
                    layer="above"), dict(
                    source='data:image/png;base64,{}'.format(encoded_image_GWA),
                    xref="paper", yref="paper",
                    x=0.95, y=1.05,
                    sizex=0.17, sizey=0.17,
                    xanchor="right",
                    yanchor="bottom",
                    #sizing="stretch",
                    layer="above")])
    
    # update layout properties
    fig.update_layout(
        autosize=False,
        height=480,
        width=600,
        bargap=0.15,
        bargroupgap=0.1,
        barmode="stack",
        hovermode="x",
        margin=dict(t=100, b=10, l=10, r = 10),
    )
    return fig

