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
save_loc =  './Plots/qe_optimal_angles_all.png' #insert filepath to output folder and desired name
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
    if  wave == '1450nm':
        df['flux'] = df['flux'] * 0
    elif wave == '1550nm':
        df['flux'] = df['flux'] * 0
    elif wave == '1650nm':
        df['flux'] = df['flux'] * 0
    elif wave == '1750nm':
        df['flux'] = df['flux'] * 0
    elif wave == '1850nm':
        df['flux'] = df['flux'] * 0
    elif wave == '1950nm':
        df['flux'] = df['flux'] * 0
    elif wave == 'UVCi':
        df['flux'] = df['flux'] * 0
    elif wave == 'UVCii':
        df['flux'] = df['flux'] * 0
    elif wave == 'UVCiii':
        df['flux'] = df['flux'] * 0
    elif wave == 'UVCiv':
        df['flux'] = df['flux'] * 0
    elif wave == 'UVA':
        df['flux'] = df['flux'] / 88775 / (3E8 / 358E-9 * 6.626E-34) *  0.4
        waveint = 358
    elif wave == 'UVB':
        df['flux'] = df['flux'] / 88775 / (3E8 / 298E-9 * 6.626E-34) *  0.035
        waveint = 298
    elif wave == '425nm':
        df['flux'] = df['flux'] / 88775 / (3E8 / 425E-9 * 6.626E-34) *  0.79
        waveint = 425
    elif wave == '475nm':
        df['flux'] = df['flux'] / 88775 / (3E8 / 475E-9 * 6.626E-34) *  0.8
        waveint = 475
    elif wave == '525nm':
        df['flux'] = df['flux'] / 88775 / (3E8 / 525E-9 * 6.626E-34) *  0.74
        waveint = 525
    elif wave == '575nm':
        df['flux'] = df['flux'] / 88775 / (3E8 / 575E-9 * 6.626E-34) *  0.67
        waveint = 575
    elif wave == '625nm':
        df['flux'] = df['flux'] / 88775 / (3E8 / 625E-9 * 6.626E-34) *  0.5
        waveint = 625
    elif wave == '675nm':
        df['flux'] = df['flux'] / 88775 / (3E8 / 675E-9 * 6.626E-34) *  0.76
        waveint = 675
    elif wave == '725nm':
        df['flux'] = df['flux'] / 88775 / (3E8 / 725E-9 * 6.626E-34) *  0.84
        waveint = 725
    elif wave == '775nm':
        df['flux'] = df['flux'] / 88775 / (3E8 / 775E-9 * 6.626E-34) *  0.86
        waveint = 775
    elif wave == '825nm':
        df['flux'] = df['flux'] / 88775 / (3E8 / 825E-9 * 6.626E-34) *  0.84
        waveint = 825
    elif wave == '875nm':
        df['flux'] = df['flux'] / 88775 / (3E8 / 875E-9 * 6.626E-34) *  0.55
        waveint = 875
    elif wave == '925nm':
        df['flux'] = df['flux'] / 88775 / (3E8 / 925E-9 * 6.626E-34) *  0.85
        waveint = 925
    elif wave == '975nm':
        df['flux'] = df['flux'] / 88775 / (3E8 / 975E-9 * 6.626E-34) *  0.86
        waveint = 975
    elif wave == '1050nm':
        df['flux'] = df['flux'] / 88775 / (3E8 / 1050E-9 * 6.626E-34) *  0.82
        waveint = 1050
    elif wave == '1150nm':
        df['flux'] = df['flux'] / 88775 / (3E8 / 1150E-9 * 6.626E-34) *  0.76
        waveint = 1150
    elif wave == '1250nm':
        df['flux'] = df['flux'] / 88775 / (3E8 / 1250E-9 * 6.626E-34) *  0.55
        waveint = 1250
    elif wave == '1350nm':
        df['flux'] = df['flux'] / 88775 / (3E8 / 1350E-9 * 6.626E-34) *  0.01
        waveint = 1350
    df_all = pd.concat([df_all, df])
for a in latitudes:
    for b in solar_longs:
        df_wavsplit = df_all[(df_all['latitude'] == a) & (df_all['solar_longitude'] == b)]
        waven = df_wavsplit['flux'].sum()
        waven = waven * 1.6E-19 * 88775 #convert back to energy/day
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
            if  wave == '1450nm':
                df['flux'] = df['flux'] * 0
            elif wave == '1550nm':
                df['flux'] = df['flux'] * 0
            elif wave == '1650nm':
                df['flux'] = df['flux'] * 0
            elif wave == '1750nm':
                df['flux'] = df['flux'] * 0
            elif wave == '1850nm':
                df['flux'] = df['flux'] * 0
            elif wave == '1950nm':
                df['flux'] = df['flux'] * 0
            elif wave == 'UVCi':
                df['flux'] = df['flux'] * 0
            elif wave == 'UVCii':
                df['flux'] = df['flux'] * 0
            elif wave == 'UVCiii':
                df['flux'] = df['flux'] * 0
            elif wave == 'UVCiv':
                df['flux'] = df['flux'] * 0
            elif wave == 'UVA':
                df['flux'] = df['flux'] / 88775 / (3E8 / 358E-9 * 6.626E-34) *  0.4
                waveint = 358
            elif wave == 'UVB':
                df['flux'] = df['flux'] / 88775 / (3E8 / 298E-9 * 6.626E-34) *  0.035
                waveint = 298
            elif wave == '425nm':
                df['flux'] = df['flux'] / 88775 / (3E8 / 425E-9 * 6.626E-34) *  0.79
                waveint = 425
            elif wave == '475nm':
                df['flux'] = df['flux'] / 88775 / (3E8 / 475E-9 * 6.626E-34) *  0.8
                waveint = 475
            elif wave == '525nm':
                df['flux'] = df['flux'] / 88775 / (3E8 / 525E-9 * 6.626E-34) *  0.74
                waveint = 525
            elif wave == '575nm':
                df['flux'] = df['flux'] / 88775 / (3E8 / 575E-9 * 6.626E-34) *  0.67
                waveint = 575
            elif wave == '625nm':
                df['flux'] = df['flux'] / 88775 / (3E8 / 625E-9 * 6.626E-34) *  0.5
                waveint = 625
            elif wave == '675nm':
                df['flux'] = df['flux'] / 88775 / (3E8 / 675E-9 * 6.626E-34) *  0.76
                waveint = 675
            elif wave == '725nm':
                df['flux'] = df['flux'] / 88775 / (3E8 / 725E-9 * 6.626E-34) *  0.84
                waveint = 725
            elif wave == '775nm':
                df['flux'] = df['flux'] / 88775 / (3E8 / 775E-9 * 6.626E-34) *  0.86
                waveint = 775
            elif wave == '825nm':
                df['flux'] = df['flux'] / 88775 / (3E8 / 825E-9 * 6.626E-34) *  0.84
                waveint = 825
            elif wave == '875nm':
                df['flux'] = df['flux'] / 88775 / (3E8 / 875E-9 * 6.626E-34) *  0.55
                waveint = 875
            elif wave == '925nm':
                df['flux'] = df['flux'] / 88775 / (3E8 / 925E-9 * 6.626E-34) *  0.85
                waveint = 925
            elif wave == '975nm':
                df['flux'] = df['flux'] / 88775 / (3E8 / 975E-9 * 6.626E-34) *  0.86
                waveint = 975
            elif wave == '1050nm':
                df['flux'] = df['flux'] / 88775 / (3E8 / 1050E-9 * 6.626E-34) *  0.82
                waveint = 1050
            elif wave == '1150nm':
                df['flux'] = df['flux'] / 88775 / (3E8 / 1150E-9 * 6.626E-34) *  0.76
                waveint = 1150
            elif wave == '1250nm':
                df['flux'] = df['flux'] / 88775 / (3E8 / 1250E-9 * 6.626E-34) *  0.55
                waveint = 1250
            elif wave == '1350nm':
                df['flux'] = df['flux'] / 88775 / (3E8 / 1350E-9 * 6.626E-34) *  0.01
                waveint = 1350
            df_all = pd.concat([df_all, df])
        allwavelengths = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux', 'pointing', 'tilt'])
        for a in latitudes:
            for b in solar_longs:
                df_wavsplit = df_all[(df_all['latitude'] == a) & (df_all['solar_longitude'] == b)]
                waven = df_wavsplit['flux'].sum()
                waven = waven * 1.6E-19 * 88775 #convert back to energy/day
                df_wavsum = pd.DataFrame([{'latitude':a, 'solar_longitude':b, 'flux':waven, 'pointing':panel_direction, 'tilt':panel_angle}])
                allwavelengths = pd.concat([allwavelengths, df_wavsum])
        allwavelengths['flux'] = allwavelengths['flux']/1000000 #unit conversion for plot
        for i in range(df_optimal.shape[0]):
            #print(allwavelengths.iloc[i]['flux'])
            #print(df_optimal.iloc[i]['flux'])
            if allwavelengths.iloc[i]['flux'] > df_optimal.iloc[i]['flux']:
                df_optimal.iloc[i] = allwavelengths.iloc[i]
                print('higher!')
            #else:
                #print('lower!')
df_optimal.to_csv(path_or_buf = './Data/qe_optimal_flux_values', index=False)
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
hm = plt.title('Available Solar Energy at Optimal Azimuth and Elevation Angles on the Surface of Mars')
hm = plt.savefig(save_loc)
print('All plots completed.')
plt.show()
