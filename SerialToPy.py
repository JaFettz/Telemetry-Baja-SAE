import serial
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from os import system, name
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm


def update(i):
    point.set_data(df["Latitude"].iloc[-1], df["Longitude"].iloc[-1])
    return point,

def clear():
    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')
        print('\033c')

serialPort = serial.Serial(port="/dev/pts/6", baudrate=38400,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

serialString = ""                           # Used to hold data coming over UART

data_pkg_size = [1,2,5,1,3,5,5,2]

# print(np.sum(data_pkg_size))
background = (64/255, 67/255, 71/255)

df=[]

# fig, ax = plt.subplots(nrows=1, ncols=1)

# point, = ax.plot(0, 0,'ro')

# ani = FuncAnimation(fig, update, interval=100, frames= range(len(df['lon'])))
# animation = FuncAnimation(fig, update, interval=100)

# fig.set_facecolor(background)
# ax.set_facecolor(background)
# ax.axis('off')



try:
    Estado = True
    while(Estado):
    # Wait until there is data waiting in the serial buffer
        Command = input('Insert command \n')
        if Command == "Create":
            print("Creating map")
            Loop = True
            Nombre = input('Map name? \n')
            Archivo = Path("./"+Nombre+".csv")

            if Archivo.is_file():
                df = pd.read_csv(Nombre + ".csv")
            else:
                df = pd.DataFrame(columns = ['Latitude','Longitude','Height','Time'])

            # plt.show(block=False)
            try:
                while(Loop):
                    if(serialPort.in_waiting > 0):

                        # Read data out of the buffer until a carraige return / new line is found
                        serialString = serialPort.readline()

                        stringData = serialString.decode('Ascii')

                        if(len(stringData)>25):
                            part = 0
                            data_pkg = []
                            stringData = stringData[1:]
                            for i in range(len(data_pkg_size )):
                                data_pkg.append(int(stringData[part:part+data_pkg_size[i]])) 
                                part += data_pkg_size[i]


                            Lat=data_pkg[1] + data_pkg[2]/100000
                            Lng=data_pkg[4] + data_pkg[5]/100000
                            Alt=data_pkg[6]
                            Sat=data_pkg[7]

                            if not data_pkg[0] : Lat= Lat * -1 
                            if not data_pkg[3] : Lng= Lng * -1 

                            print("Lat: ",Lat)
                            print("Lng: ",Lng)
                            print("Alt: ",Alt)
                            print("Sat: ",Sat)

                            print("Data:")
                            # Print the contents of the serial data
                            print(serialString.decode('Ascii'))

                            df = df.append({'Latitude': Lat, 'Longitude' : Lng, 'Height' : Alt, 'Time' : datetime.now().strftime("%d/%m/%Y %H:%M:%S")}, ignore_index=True)
                        # Tell the device connected over the serial port that we recevied the data!
                        # The b at the beginning is used to indicate bytes!

                        # serialPort.write(b"Thank you for sending data \r\n")
            except KeyboardInterrupt:
                pass
            Loop = False
            # plt.close(fig)
            df.to_csv(Nombre+".csv",index = False)
            print("Ok, Saving data")
            print("Going back to the menu")

        if Command == "Plot":
            print("Ploting")
        
        if Command == "Load":
            print("Load map")

            Nombre = input('File name? \n')
            Archivo = Path("./"+Nombre+".csv")

            if Archivo.is_file():
                df = pd.read_csv(Nombre + ".csv")
                print("File loaded")
            else:
                print("File does not exist")

        if Command == "Exit":
            Ask = input('Are you sure y/n?')
            if Ask == "y" or Ask == "Y" or Ask == "yes" : Estado = False

except KeyboardInterrupt:
    pass

print("Ok, exiting program")


