import pandas as pd
import numpy as np
import geopandas as gpd
from tkinter import *
import os
from tkinter import ttk
from matplotlib import pyplot as plt
from PIL import ImageTk,Image 

main = Tk()
global img
main.title('AQI by Year')
files = [f for f in os.listdir('YearData\\') if f.endswith('.csv')]
pollutants = list(set([f.split('_')[0] for f in files]))
pollutant = StringVar()
year = StringVar()
years = list(set([f.split('_')[1].split('.')[0] for f in files if pollutant.get() in f]))
years.sort()
df = pd.DataFrame()



def plot_data():
    md = gpd.read_file('Maryland//Maryland_Physical_Boundaries__County_Boundaries_Generalized.shp')
    md['value'] = 0
    ff = [f for f in files if (pollutant.get() in f) & (year.get() in f)]
    for f in ff:
        temp = pd.read_csv('YearData\\'+f,header=0, usecols=[0,4,6,7,16,17,18,19])
        sites = temp['COUNTY_CODE'].unique()
        for s in sites:
            md.loc[md['county_fip']==s,'value']=temp.loc[temp['COUNTY_CODE']==s].iloc[:,1].mean()
    fig,ax=plt.subplots(figsize=(12,10))
    plt.title(pollutant.get()+' levels in Maryland,'+year.get())
    md.plot( color='black',alpha=0.5, legend=True,ax=ax, label = 'NA')
    md.loc[md['value']>0].plot( column='value',alpha=0.8, legend=True,ax=ax,cmap='viridis')
    plt.axis('off')
    plt.show()

################################# Widgets ################################
Label(main, text = "Select Pollutant : ",padx=15, pady=15).grid(row=0,column=0, sticky= W)
cmb1 = ttk.Combobox(main,textvariable=pollutant, width = 17, values = pollutants, state='readonly')
cmb1.grid(row=0,column=1,sticky=W)


Label(main, text = "Select Year : ",padx=15, pady=15).grid(row=1,column=0, sticky= W)
cmb2 = ttk.Combobox(main,textvariable=year,values = years, width = 17)
cmb2.grid(row=1,column=1,sticky=W)

Button(main, width =10, text="Print", command=plot_data).grid(row=2, column=1, sticky=W)

main.mainloop()
