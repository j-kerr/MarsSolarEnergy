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
from matplotlib.colors import LogNorm, Normalize
from matplotlib.ticker import MaxNLocator

wavelengths = ['425nm', '475nm', '525nm', '575nm', '625nm', '675nm', '725nm', '775nm', '825nm', '875nm', '925nm', '975nm', '1050nm', '1150nm', '1250nm', '1350nm', '1450nm', '1550nm', '1650nm', '1750nm', '1850nm', '1950nm', 'UVA', 'UVB', 'UVCi', 'UVCii', 'UVCiii', 'UVCiv']
latitudes = range(-90,100,10)
solar_longs = range(0,360,10) #***SOME LONGITUDES MISSING FOR <-60 LATITUDES***
datapath = './Data/'
save_loc = './Plots/qeTrackingToOptimalRatio.png'
df_all1 = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux'])
for wave in wavelengths:
    input_loc1 = datapath + 'integrated_flux_' + str(wave) + '_' + str(0) + 'degrees' + '_azimuth_' + str(0)
    df1 = pd.read_csv(input_loc1)
    if  wave == '1450nm':
        df1['flux'] = df1['flux'] * 0
    elif wave == '1550nm':
        df1['flux'] = df1['flux'] * 0
    elif wave == '1650nm':
        df1['flux'] = df1['flux'] * 0
    elif wave == '1750nm':
        df1['flux'] = df1['flux'] * 0
    elif wave == '1850nm':
        df1['flux'] = df1['flux'] * 0
    elif wave == '1950nm':
        df1['flux'] = df1['flux'] * 0
    elif wave == 'UVCi':
        df1['flux'] = df1['flux'] * 0
    elif wave == 'UVCii':
        df1['flux'] = df1['flux'] * 0
    elif wave == 'UVCiii':
        df1['flux'] = df1['flux'] * 0
    elif wave == 'UVCiv':
        df1['flux'] = df1['flux'] * 0
    elif wave == '425nm':
        df1['flux'] = df1['flux'] * 0.79
    elif wave == '475nm':
        df1['flux'] = df1['flux'] * 0.8
    elif wave == '525nm':
        df1['flux'] = df1['flux'] * 0.74
    elif wave == '575nm':
        df1['flux'] = df1['flux'] * 0.67
    elif wave == '625nm':
        df1['flux'] = df1['flux'] * 0.5
    elif wave == '675nm':
        df1['flux'] = df1['flux'] * 0.76
    elif wave == '725nm':
        df1['flux'] = df1['flux'] * 0.84
    elif wave == '775nm':
        df1['flux'] = df1['flux'] * 0.86
    elif wave == '825nm':
        df1['flux'] = df1['flux'] * 0.84
    elif wave == '875nm':
        df1['flux'] = df1['flux'] * 0.55
    elif wave == '925nm':
        df1['flux'] = df1['flux'] * 0.85
    elif wave == '975nm':
        df1['flux'] = df1['flux'] * 0.86
    elif wave == '1050nm':
        df1['flux'] = df1['flux'] * 0.82
    elif wave == '1150nm':
        df1['flux'] = df1['flux'] * 0.76
    elif wave == '1250nm':
        df1['flux'] = df1['flux'] * 0.55
    elif wave == '1350nm':
        df1['flux'] = df1['flux'] * 0.01
    df_all1 = pd.concat([df_all1, df1])

allwavelengths1 = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux'])
for a in latitudes:
    for b in solar_longs:
        df_wavsplit = df_all1[(df_all1['latitude'] == a) & (df_all1['solar_longitude'] == b)]
        waven = df_wavsplit['flux'].sum()
        df_wavsum = pd.DataFrame([{'latitude':a, 'solar_longitude':b, 'flux':waven}])
        allwavelengths1 = pd.concat([allwavelengths1, df_wavsum], ignore_index=True)


allwavelengths2 = pd.read_csv('./Data/qe_optimal_flux_values')
allwavelengths2 = allwavelengths2.drop(columns = ['pointing', 'tilt'])

print(allwavelengths1)
print(allwavelengths2.loc[[400]])


allwavelengths1['flux'] = allwavelengths1['flux']/1000000 #unit conversion for plot
#already done for optimal values

allwavelengths = allwavelengths1.copy(deep=True)
print(allwavelengths)
allwavelengths.insert(3, 'flux2', allwavelengths2['flux'])
#allwavelengths['flux'] = allwavelengths['flux'].replace(0,1)
#allwavelengths['flux2'] = allwavelengths['flux2'].replace(0,1)
print(allwavelengths.loc[[400]])
allwavelengths['ratio'] = allwavelengths['flux2'] / allwavelengths['flux']
allwavelengths = allwavelengths.drop(columns=['flux2'])
allwavelengths = allwavelengths.drop(columns=['flux'])

sns.set(rc={'figure.figsize':(19.2,10.8)})
sns.set(font_scale=2)
allwavelengths = allwavelengths.pivot('latitude', 'solar_longitude', 'ratio')
print(allwavelengths)
hm = sns.heatmap(allwavelengths, cmap='magma', xticklabels = 6, yticklabels = 3, cbar_kws={'label': 'Solar Energy Ratio (Logarithmic Scale)'})
hm = hm.invert_yaxis()
hm = plt.xlabel('Solar Longitude ($^\circ$)')
hm = plt.ylabel('Latitude ($^\circ$)')
hm = plt.title('Solar Energy Gain for an Optimally Placed Panel over a Horizontal Panel')
hm = plt.savefig(save_loc)
print('All plots completed.')
plt.show()
