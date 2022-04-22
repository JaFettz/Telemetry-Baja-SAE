import gpxpy
import matplotlib.pyplot as plt
import datetime
from geopy import distance
from math import sqrt, floor
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
#import plotly.plotly as py
#import plotly.graph_objs as go
#import haversine
from itertools import count


def update(i):
    point.set_data(df['lon'][i], df['lat'][i])

    return point,


def plot(i):
    t = df['lon'][i]
    y = df['lat'][i]
    print(t," ",y)
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()

    if t >= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,

def init():
    # ax.set_xlim(df['lon'].min() -.1, df['lon'].max() +.1 )
    # ax.set_xlim(df['lat'].min() -.1, df['lat'].max() +.1 )
    print("min and max")
    print(df['lon'].min()," ",df['lon'].max())
    print(df['lat'].min()," ",df['lat'].max())
    del xdata[:]
    del ydata[:]
    line.set_data(xdata,ydata)
    return line,

background = (64/255, 67/255, 71/255)

#read data file for ploting of the map
def gps_data(file):
    gpx_file = open(file,'r')
    gpx = gpxpy.parse(gpx_file)

    data = gpx.tracks[0].segments[0].points

    ## Start Position
    start = data[0]
    ## End Position
    finish = data[-1]

    df = pd.DataFrame(columns=['lon', 'lat', 'alt', 'time'])
    for point in data:
        df = df.append({'lon': point.longitude, 'lat' : point.latitude, 'alt' : point.elevation, 'time' : point.time}, ignore_index=True)
    
    return(df)




df = gps_data('gpsdata.gpx')

fig, ax = plt.subplots(nrows=1, ncols=1)

ax.plot(df['lon'], df['lat'],'#a6a6a6',linewidth=5.0)


# point, = ax.plot(df['lon'][0], df['lat'][0],'ro')
line, = ax.plot([],[], lw = 2)
ax.grid()
xdata, ydata= [],[]

# ani = FuncAnimation(fig, update, interval=100, frames= range(len(df['lon'])))
ani = FuncAnimation(fig,plot,interval=100,frames= range(len(df['lon'])), init_func=init)

fig.set_facecolor(background)
ax.set_facecolor(background)
# ax.axis('off')
plt.show()

print(df['alt'])
