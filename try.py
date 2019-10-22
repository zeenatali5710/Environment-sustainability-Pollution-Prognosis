import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
from matplotlib.animation import FFMpegWriter as ffm

data = pd.read_csv('O3 16-19.csv')
data['Date (UTC)'] = data['Date (UTC)'].astype('datetime64[ns]')
data['Time (UTC)'] = pd.to_datetime(data['Time (UTC)'], format='%H:%M').dt.time
data['Date (LST)'] = data['Date (LST)'].astype('datetime64[ns]')
data['Time (LST)'] = pd.to_datetime(data['Time (LST)'], format='%H:%M').dt.time
data = data.sort_values(by='Date (UTC)')
data = data.reset_index(drop=True)
df = data.sample(frac=1)
fig,axs=plt.subplots(2,1,figsize=(14,8))
axs[0].set_xlim([data['Date (UTC)'].iloc[0],data['Date (UTC)'].iloc[1080]])
plt.ylabel('OZONE Concentration')

#writer = ffm(fps=15, metadata=dict(artist='Me'), bitrate=1800,extra_args=['-vcodec', 'libx264'])
ims = []
for i in range(len(data)):
    im = axs[0].scatter(data['Date (UTC)'].iloc[:i],data['Value'].iloc[:i],marker='_', c='red')
    im2 = axs[1].scatter(data['Date (UTC)'].iloc[:i],df['Value'].iloc[:i],marker='_', c='blue')
    ims.append([im])
    ims.append([im2])
ani = animation.ArtistAnimation(fig, ims, interval=2, blit=True, repeat_delay=10)
plt.show()


