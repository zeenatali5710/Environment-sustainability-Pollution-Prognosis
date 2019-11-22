import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
from matplotlib.animation import FFMpegWriter as ffm
from scipy.interpolate import interp1d

data = pd.read_csv('O3.csv')
data2 = pd.read_csv('PM 25.csv')


data['Date (UTC)'] = data['Date (UTC)'].astype('datetime64[ns]')
data['Time (UTC)'] = pd.to_datetime(data['Time (UTC)'], format='%H:%M').dt.time
data['Date (LST)'] = data['Date (LST)'].astype('datetime64[ns]')
data['Time (LST)'] = pd.to_datetime(data['Time (LST)'], format='%H:%M').dt.time
data['temp']=data['Date (UTC)'].dt.strftime("%Y%m%d").astype(int)
data = data.sort_values(by='Date (UTC)')
data = data.reset_index(drop=True)
temp = data[['Date (UTC)','Value','temp']].dropna()
data = data.loc[data['Date (UTC)']<= temp['Date (UTC)'].iloc[-1]]
f= interp1d(temp['temp'],temp['Value'])
print(f(data['temp']))

data2['Date (UTC)'] = data2['Date (UTC)'].astype('datetime64[ns]')
data2['Time (UTC)'] = pd.to_datetime(data2['Time (UTC)'], format='%H:%M').dt.time
data2['Date (LST)'] = data2['Date (LST)'].astype('datetime64[ns]')
data2['Time (LST)'] = pd.to_datetime(data2['Time (LST)'], format='%H:%M').dt.time
data2 = data2.sort_values(by='Date (UTC)')
data2 = data2.reset_index(drop=True)

fig,axs=plt.subplots(2,1,figsize=(12,6))
line, = axs[0].plot(data['Date (UTC)'],f(data['temp']), color = 'red')
line2, = axs[1].plot(data2['Date (UTC)'],data2['Value'], color = 'blue')
axs[0].set_ylabel('OZONE Concentration')
axs[1].set_ylabel('PM 2.5 Concentration')

#writer = ffm(fps=15, metadata=dict(artist='Me'), bitrate=1800,extra_args=['-vcodec', 'libx264'])
ims = []
def update(i,x,y,line):
    line.set_data(x[:i],y[:i])
    return line,
ani = animation.FuncAnimation(fig, update, len(data), fargs=[data['Date (UTC)'],f(data['temp']), line],interval=15, blit=True)
ani2 = animation.FuncAnimation(fig, update, len(data), fargs=[data2['Date (UTC)'],data2['Value'], line2],interval=15, blit=True)
plt.show()


