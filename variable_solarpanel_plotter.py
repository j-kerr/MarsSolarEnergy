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

panel_angle = 0
panel_direction = 0
save_loc =  './Plots/' + str(panel_angle) + 'degree_' + str(panel_direction) + 'azimuth_heatmap_all.png' #insert filepath to output folder and desired name
filename = 'whole_sky_heatmap_' + str(panel_angle) + 'south.png' #output file name
wavelengths = ['425nm', '475nm', '525nm', '575nm', '625nm', '675nm', '725nm', '775nm', '825nm', '875nm', '925nm', '975nm', '1050nm', '1150nm', '1250nm', '1350nm', '1450nm', '1550nm', '1650nm', '1750nm', '1850nm', '1950nm', 'UVA', 'UVB', 'UVCi', 'UVCii', 'UVCiii', 'UVCiv']
latitudes = range(-90,100,10)
solar_longs = range(0,360,10) #***SOME LONGITUDES MISSING FOR <-60 LATITUDES***
datapath = './Data/'

df_all = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux'])
for wave in wavelengths:
    input_loc = datapath + 'integrated_flux_' + str(wave) + '_' + str(panel_angle) + 'degrees' + '_azimuth_' + str(panel_direction)
    df = pd.read_csv(input_loc)
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
hm = plt.title('Available Solar Energy for a ' + str(panel_angle) + '\u00b0 Panel Facing Azimuth ' + str(panel_direction) + '\u00b0')
hm = plt.savefig(save_loc)
print('All plots completed.')
plt.show()
