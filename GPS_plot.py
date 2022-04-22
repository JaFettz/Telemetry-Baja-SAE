import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from multiprocessing import Process,Pipe 
import pandas as pd

def update(i):
    point.set_data()

def plot(child_conn,map=0):
    Mode = True
    background = (64/255, 67/255, 71/255)

    fig, ax = plt.subplots(nrows=1,ncols=1)


    if map:
        ax.plot(map['Longitude'],map['Latitude'],'#a6a6a6',linewidth=5.0)

    fig.set_facecolor(background)
    ax.set_facecolor(background)
    ax.axis('off')

    while Mode:
        print("plot")
