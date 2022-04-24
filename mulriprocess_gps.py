import gpxpy
import matplotlib.pyplot as plt
import datetime
from geopy import distance
from math import sqrt, floor
import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
#import plotly.plotly as py
#import plotly.graph_objs as go
#import haversine
from itertools import count
import staticmaps
from GPSplot import plotting
from multiprocessing import Process,Queue,Pipe,Array


def gps_data(file):
    gpx_file = open(file,'r')
    gpx = gpxpy.parse(gpx_file)

    data = gpx.tracks[0].segments[0].points

    ## Start Position
    start = data[0]
    ## End Position
    finish = data[-1]

    df = pd.DataFrame(columns=['Longitude', 'Latitude', 'Height', 'Time'])
    for point in data:
        df = df.append({'Longitude': point.longitude, 'Latitude' : point.latitude, 'Height' : point.elevation, 'Time' : point.time}, ignore_index=True)
    
    return(df)



df = gps_data('gpsdata.gpx')

parent_conn,child_conn = Pipe()
p = Process(target=plotting,args=(child_conn, df))
p.start()



for i in range(len(df['Longitude'])):
    x = df['Longitude'][i]
    y = df['Latitude'][i]
    parent_conn.send([x,y,i])
    
