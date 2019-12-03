import pandas as pd
import numpy as np
import os
import geopandas as gpd
from tkinter import *
from tkinter import ttk
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import seaborn as sns

main = Tk()
main.title("Pollutant over Time")

files = [f for f in os.listdir('Data\\') if f.endswith('.csv')]
pollutants = list(set([f.split('_')[0] for f in files]))
pollutant = StringVar()
site = StringVar()
sites = list(set([f.split('_')[1] for f in files if pollutant.get() in f]))
df = pd.DataFrame()

def pick_sites(cmb):
    sites = list(set([f.split('_')[1] for f in files if pollutant.get() in f]))
    cmb.config(state='readonly',values=sites)

def update(i,x,y,line):
    line.set_data(x[:i],y[:i])
    return line,

def plot_data():
    df= pd.DataFrame()
    ff = [f for f in files if (pollutant.get() in f) & (site.get() in f)]
    for f in ff: 
        temp = pd.read_csv('Data\\'+f,header=0, usecols=[0,4,6,7,16,17,18,19])
        df = pd.concat([df,temp])
    df.reset_index(drop=True)
    df['Date'] = df['Date'].astype('datetime64[ns]')

    fig,ax = plt.subplots(figsize=(12,5))
    plt.title(pollutant.get()+' levels in ' + site.get())
    line, = ax.plot(df['Date'],df[df.columns[1]],color='red')
    ani = animation.FuncAnimation(fig, update, len(df), fargs=[df['Date'],df[df.columns[1]], line],interval=15, blit=True)
    plt.show()



################################# Widgets ################################
Label(main, text = "Select Pollutant : ",padx=15, pady=15).grid(row=0,column=0, sticky= W)
cmb1 = ttk.Combobox(main,textvariable=pollutant, width = 17, values = pollutants, state='readonly')
cmb1.grid(row=0,column=1,sticky=W)


Label(main, text = "Select Site : ",padx=15, pady=15).grid(row=1,column=0, sticky= W)
cmb2 = ttk.Combobox(main,textvariable=site,values = sites, width = 17)
cmb2.grid(row=1,column=1,sticky=W)
cmb2.config(postcommand=pick_sites(cmb2))

Button(main, width =10, text="Print", command=plot_data).grid(row=2, column=1, sticky=W)

main.mainloop()

