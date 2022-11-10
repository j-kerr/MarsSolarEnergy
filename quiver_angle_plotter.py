#!/usr/bin/env python3
#Plots integrated solar energy data
#Justin Kerr, May 2022

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

save_loc =  './Plots/optimal_angles_all_quiver.png' #insert filepath to output folder and desired name
filename = './Data/optimal_flux_values' #data file name

datapath = './Data/'

df = pd.read_csv(filename)
print(df)
df['pointing'] = 450 - df['pointing']
print(df.iloc[388])



plot = plt.quiver(df['solar_longitude'].values, df['latitude'].values, 1, 1, [df['tilt'].values], angles = df['pointing'].values)
plot = plt.xlabel('Solar Longitude ($^\circ$)')
plot = plt.ylabel('Latitude ($^\circ$)')
plot = plt.title('Available Solar Energy at Optimal Facing and Elevation Angle')
plot = plt.colorbar()
plot = plt.savefig(save_loc)
print('All plots completed.')
plt.show()
