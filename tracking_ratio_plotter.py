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

panel_angle2 = 0
panel_direction2 = 0
save_loc =  './Plots/' + 'tracking' + str(panel_angle2) + '_ratio_all.png' #insert filepath to output folder and desired name
wavelengths = ['425nm', '475nm', '525nm', '575nm', '625nm', '675nm', '725nm', '775nm', '825nm', '875nm', '925nm', '975nm', '1050nm', '1150nm', '1250nm', '1350nm', '1450nm', '1550nm', '1650nm', '1750nm', '1850nm', '1950nm', 'UVA', 'UVB', 'UVCi', 'UVCii', 'UVCiii', 'UVCiv']
latitudes = range(-90,100,10)
solar_longs = range(0,360,10) #***SOME LONGITUDES MISSING FOR <-60 LATITUDES***
datapath = './Data/'

df_all1 = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux'])
for wave in wavelengths:
    input_loc1 = datapath + 'integrated_flux_' + str(wave) + '_' + 'tracking'
    df1 = pd.read_csv(input_loc1)
    df_all1 = pd.concat([df_all1, df1])

allwavelengths1 = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux'])
for a in latitudes:
    for b in solar_longs:
        df_wavsplit = df_all1[(df_all1['latitude'] == a) & (df_all1['solar_longitude'] == b)]
        waven = df_wavsplit['flux'].sum()
        df_wavsum = pd.DataFrame([{'latitude':a, 'solar_longitude':b, 'flux':waven}])
        allwavelengths1 = pd.concat([allwavelengths1, df_wavsum])

df_all2 = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux'])
for wave in wavelengths:
    input_loc2 = datapath + 'integrated_flux_' + str(wave) + '_' + str(panel_angle2) + 'degrees' + '_azimuth_' + str(panel_direction2)
    df2 = pd.read_csv(input_loc2)
    df_all2 = pd.concat([df_all2, df2])

allwavelengths2 = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux'])
for a in latitudes:
    for b in solar_longs:
        df_wavsplit = df_all2[(df_all1['latitude'] == a) & (df_all2['solar_longitude'] == b)]
        waven = df_wavsplit['flux'].sum()
        df_wavsum = pd.DataFrame([{'latitude':a, 'solar_longitude':b, 'flux':waven}])
        allwavelengths2 = pd.concat([allwavelengths2, df_wavsum])

sns.set(rc={'figure.figsize':(19.2,10.8)})

allwavelengths1['flux'] = allwavelengths1['flux']/1000000 #unit conversion for plot
allwavelengths2['flux'] = allwavelengths2['flux']/1000000 #unit conversion for plot


allwavelengths = allwavelengths1.copy(deep=True)
print(allwavelengths)
allwavelengths.insert(3, 'flux2', allwavelengths2['flux'])
allwavelengths['flux'] = allwavelengths['flux'].replace(0,1)
allwavelengths['flux2'] = allwavelengths['flux2'].replace(0,1)
print(allwavelengths)
allwavelengths['ratio'] = allwavelengths['flux'] / allwavelengths['flux2']
allwavelengths = allwavelengths.drop(columns=['flux2'])
allwavelengths = allwavelengths.drop(columns=['flux'])

sns.set(font_scale=2)
allwavelengths = allwavelengths.pivot('latitude', 'solar_longitude', 'ratio')
print(allwavelengths)
hm = sns.heatmap(allwavelengths, cmap='viridis', xticklabels = 6, yticklabels = 3, cbar_kws={'label': 'Energy per Sol ($10^6$J)'})
hm = hm.invert_yaxis()
hm = plt.xlabel('Solar Longitude ($^\circ$)')
hm = plt.ylabel('Latitude ($^\circ$)')
hm = plt.title('Available Solar Energy for a ' + 'Sun Tracking' + ' vs ' + str(panel_angle2) + ' Degree Panel Pointing to Azimuth ' + str(panel_direction2))
hm = plt.savefig(save_loc)
print('All plots completed.')
plt.show()
