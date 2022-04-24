import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from multiprocessing import Process,Pipe 
import staticmaps
import pandas as pd


def plotting(child_conn,map=None,background_img=None):
    def create(i):
        if child_conn.poll():
            x=child_conn.recv()[0]
            y=child_conn.recv()[1]
            sat=child_conn.recv()[2]
            xdata.append(x)
            ydata.append(y)
            xmin, xmax = ax.get_xlim()
            ymin, ymax = ax.get_ylim()
            print("multi ",sat)

            if max(xdata) >= xmax:
                print("t>=xmax")
                xmax= x+0.0002
                ax.set_xlim(xmin, xmax)
                ax.figure.canvas.draw()
            if min(xdata) <= xmin-0.0001 or min(xdata) >= xmin+0.0001:
                print("t>=xmin")
                ax.set_xlim(x-0.0002,xmax)
                ax.figure.canvas.draw()
               
            if max(ydata) >= ymax:
                print("y>=ymax")
                ymax= y+0.0002
                ax.set_ylim(ymin, ymax)
                ax.figure.canvas.draw()
            if min(ydata) <= ymin-0.0001 or min(ydata) >= ymin+0.0001:
                print("y>=ymin")
                ax.set_ylim(y-0.0002,ymax)
                ax.figure.canvas.draw()

            sat_text.set_text(f"Satellites: {sat}")
            trace.set_data(xdata, ydata)

        return trace, sat_text


    def update(i):
        if child_conn.poll():
            x=child_conn.recv()[0]
            y=child_conn.recv()[1]
            sat=child_conn.recv()[2]
            sat_text.set_text(f"Satellites: {sat}")
            trace.set_data(x,y)

        return trace, sat_text


    def init():
        del xdata[:]
        del ydata[:]
        trace.set_data(xdata,ydata)
        return trace,

    background = (64/255, 67/255, 71/255)

    mpl.rcParams['toolbar'] = 'None'
    
    fig, ax = plt.subplots(nrows=1,ncols=1)

    if map is not None:
        context = staticmaps.Context()
        context.set_tile_provider(staticmaps.tile_provider_OSM)

        ax.plot(map['Longitude'],map['Latitude'],'#a6a6a6',linewidth=5.0)

        ax.set_xlim(map['Longitude'].min()-0.0002, map['Longitude'].max()+0.0002)
        ax.set_ylim(map['Latitude'].min()-0.0002, map['Latitude'].max()+0.0002)

        print(background_img)
        if background_img is not None:
            line = [staticmaps.create_latlng(map['Latitude'][i],map['Longitude'][i]) for i in range(len(map['Longitude'])) ]
            context.add_object(staticmaps.Line(line))

            image = context.render_pillow(1600, 1000)
            xmin, xmax = ax.get_xlim()
            ymin, ymax = ax.get_ylim()
            ax.imshow(image, extent=[xmin,xmax,ymin,ymax])
        

    xdata,ydata = [],[]

    sat_text = ax.text(0.05,0.9,'',transform=ax.transAxes)

    if map is not None:
        trace, = ax.plot([],[],'ro',label='car')
        ani = FuncAnimation(fig,update,interval=100, init_func=init)
    else:
        trace, = ax.plot([],[],lw=2)
        ani = FuncAnimation(fig,create,interval=100, init_func=init)

    fig.set_facecolor(background)
    ax.set_facecolor(background)
    ax.axis('off')
    plt.legend(loc='upper right')
    plt.show()

