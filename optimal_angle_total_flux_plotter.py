#!/usr/bin/env python3
#Plots integrated solar energy data
#Justin Kerr, May 2022

import numpy as np
import sys
import os
import pandas as pd
import holoviews as hv
from holoviews import opts
from bokeh.plotting import show
import seaborn as sns
import matplotlib.pyplot as plt

panel_angle_list = [15, 30, 45, 60, 75, 90]
panel_direction_list = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
save_loc =  './Plots/optimal_angles_all.png' #insert filepath to output folder and desired name
filename = 'optimal_angles_all.png' #output file name
wavelengths = ['425nm', '475nm', '525nm', '575nm', '625nm', '675nm', '725nm', '775nm', '825nm', '875nm', '925nm', '975nm', '1050nm', '1150nm', '1250nm', '1350nm', '1450nm', '1550nm', '1650nm', '1750nm', '1850nm', '1950nm', 'UVA', 'UVB', 'UVCi', 'UVCii', 'UVCiii', 'UVCiv']
latitudes = range(-90,100,10)
solar_longs = range(0,360,10) #***SOME LONGITUDES MISSING FOR <-60 LATITUDES***
datapath = './Data/'
df_optimal = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux', 'pointing', 'tilt'])


#Set zero angle/pointing direction as default values
panel_angle_0 = 0
panel_direction_0 = 0
df_all = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux'])
for wave in wavelengths:
    input_loc = datapath + 'integrated_flux_' + str(wave) + '_' + str(panel_angle_0) + 'degrees' + '_azimuth_' + str(panel_direction_0)
    df = pd.read_csv(input_loc)
    df_all = pd.concat([df_all, df])
for a in latitudes:
    for b in solar_longs:
        df_wavsplit = df_all[(df_all['latitude'] == a) & (df_all['solar_longitude'] == b)]
        waven = df_wavsplit['flux'].sum()
        df_wavsum = pd.DataFrame([{'latitude':a, 'solar_longitude':b, 'flux':waven, 'pointing':panel_direction_0, 'tilt':panel_angle_0}])
        df_optimal = pd.concat([df_optimal, df_wavsum])
df_optimal['flux'] = df_optimal['flux']/1000000 #unit conversion for plot

#Find highest energy across all angle/direction combinations for every Lat/Ls pair
for panel_angle in panel_angle_list:
    for panel_direction in panel_direction_list:
        df_all = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux'])
        for wave in wavelengths:
            input_loc = datapath + 'integrated_flux_' + str(wave) + '_' + str(panel_angle) + 'degrees' + '_azimuth_' + str(panel_direction)
            df = pd.read_csv(input_loc)
            df_all = pd.concat([df_all, df])
        allwavelengths = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux', 'pointing', 'tilt'])
        for a in latitudes:
            for b in solar_longs:
                df_wavsplit = df_all[(df_all['latitude'] == a) & (df_all['solar_longitude'] == b)]
                waven = df_wavsplit['flux'].sum()
                df_wavsum = pd.DataFrame([{'latitude':a, 'solar_longitude':b, 'flux':waven, 'pointing':panel_direction, 'tilt':panel_angle}])
                allwavelengths = pd.concat([allwavelengths, df_wavsum])
        allwavelengths['flux'] = allwavelengths['flux']/1000000 #unit conversion for plot

        for i in range(df_optimal.shape[0]):
            print(allwavelengths.iloc[i]['flux'])
            print(df_optimal.iloc[i]['flux'])
            if allwavelengths.iloc[i]['flux'] > df_optimal.iloc[i]['flux']:
                df_optimal.iloc[i] = allwavelengths.iloc[i]
                print('higher!')
            else:
                print('lower!')

df_optimal.to_csv(path_or_buf = './Data/optimal_flux_values', index=False)
sns.set(rc={'figure.figsize':(19.2,10.8)})
sns.set(font_scale=2)
print(df_optimal)
df_plot = df_optimal.drop(columns = ['pointing', 'tilt'])
df_plot = df_plot.pivot('latitude', 'solar_longitude', 'flux')
print(df_plot)

hm = sns.heatmap(df_plot, cmap='viridis', xticklabels = 6, yticklabels = 3, cbar_kws={'label': 'Energy per Sol ($10^6$J)'})
hm = hm.invert_yaxis()
hm = plt.xlabel('Solar Longitude ($^\circ$)')
hm = plt.ylabel('Latitude ($^\circ$)')
hm = plt.title('Available Solar Energy at Optimal Facing and Elevation Angle')
hm = plt.savefig(save_loc)
print('All plots completed.')
plt.show()
