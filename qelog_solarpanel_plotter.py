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

panel_angle = 15
panel_direction = 0
save_loc =  './Plots/qe' + str(panel_angle) + 'degree_' + str(panel_direction) + 'azimuth_heatmap_all.png' #insert filepath to output folder and desired name
filename = 'qe_whole_sky_heatmap_' + str(panel_angle) + '.png' #output file name
wavelengths = ['425nm', '475nm', '525nm', '575nm', '625nm', '675nm', '725nm', '775nm', '825nm', '875nm', '925nm', '975nm', '1050nm', '1150nm', '1250nm', '1350nm', 'UVA', 'UVB']
latitudes = range(-90,100,10)
solar_longs = range(0,360,10) #***SOME LONGITUDES MISSING FOR <-60 LATITUDES***
datapath = './Data/'

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
        df['flux'] = df['flux'] * 0.4
    elif wave == 'UVB':
        df['flux'] = df['flux'] * 0.035
    elif wave == '425nm':
        df['flux'] = df['flux'] * 0.79
    elif wave == '475nm':
        df['flux'] = df['flux'] * 0.8
    elif wave == '525nm':
        df['flux'] = df['flux'] * 0.74
    elif wave == '575nm':
        df['flux'] = df['flux'] * 0.67
    elif wave == '625nm':
        df['flux'] = df['flux'] * 0.5
    elif wave == '675nm':
        df['flux'] = df['flux'] * 0.76
    elif wave == '725nm':
        df['flux'] = df['flux'] * 0.84
    elif wave == '775nm':
        df['flux'] = df['flux'] * 0.86
    elif wave == '825nm':
        df['flux'] = df['flux'] * 0.84
    elif wave == '875nm':
        df['flux'] = df['flux'] * 0.55
    elif wave == '925nm':
        df['flux'] = df['flux'] * 0.85
    elif wave == '975nm':
        df['flux'] = df['flux'] * 0.86
    elif wave == '1050nm':
        df['flux'] = df['flux'] * 0.82
    elif wave == '1150nm':
        df['flux'] = df['flux'] * 0.76
    elif wave == '1250nm':
        df['flux'] = df['flux'] * 0.55
    elif wave == '1350nm':
        df['flux'] = df['flux'] * 0.01
    df_all = pd.concat([df_all, df])
    print(df_all)
allwavelengths = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux'])
for a in latitudes:
    for b in solar_longs:
        df_wavsplit = df_all[(df_all['latitude'] == a) & (df_all['solar_longitude'] == b)]
        waven = df_wavsplit['flux'].sum()
        df_wavsum = pd.DataFrame([{'latitude':a, 'solar_longitude':b, 'flux':waven}])
        allwavelengths = pd.concat([allwavelengths, df_wavsum])

sns.set(rc={'figure.figsize':(19.2,10.8)})
allwavelengths['flux'] = allwavelengths['flux']/1000000 #unit conversion for plot
sns.set(font_scale=2)
allwavelengths = allwavelengths.pivot('latitude', 'solar_longitude', 'flux')
print(allwavelengths)
hm = sns.heatmap(allwavelengths, cmap='viridis', xticklabels = 6, yticklabels = 3, cbar_kws={'label': 'Energy per Sol ($10^6$J)'})
hm = hm.invert_yaxis()
hm = plt.xlabel('Solar Longitude ($^\circ$)')
hm = plt.ylabel('Latitude ($^\circ$)')
hm = plt.title('Available Energy for a Solar Panel Elevated ' + str(panel_angle) + '\u00b0 from the Surface Facing Azimuth ' + str(panel_direction) + '\u00b0')
hm = plt.savefig(save_loc)
print('All plots completed.')
plt.show()
