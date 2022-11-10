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

panel_angle1 = 45
panel_angle2 = 45
panel_direction1 = 120
panel_direction2 = 0
save_loc =  './Plots/qe' + str(panel_angle1) + '_az' + str(panel_direction1) + '_to_' + str(panel_angle2) + '_az' + str(panel_direction2) + '_ratio.png' #insert filepath to output folder and desired name
wavelengths = ['425nm', '475nm', '525nm', '575nm', '625nm', '675nm', '725nm', '775nm', '825nm', '875nm', '925nm', '975nm', '1050nm', '1150nm', '1250nm', '1350nm', '1450nm', '1550nm', '1650nm', '1750nm', '1850nm', '1950nm', 'UVA', 'UVB', 'UVCi', 'UVCii', 'UVCiii', 'UVCiv']
latitudes = range(-90,100,10)
solar_longs = range(0,360,10) #***SOME LONGITUDES MISSING FOR <-60 LATITUDES***
datapath = './Data/'

df_all1 = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux'])
for wave in wavelengths:
    input_loc1 = datapath + 'integrated_flux_' + str(wave) + '_' + str(panel_angle1) + 'degrees' + '_azimuth_' + str(panel_direction1)
    df = pd.read_csv(input_loc1)
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
    df['wavelength'] = waveint
    df_all1 = pd.concat([df_all1, df])

allwavelengths1 = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux'])
for a in latitudes:
    for b in solar_longs:
        df_wavsplit = df_all1[(df_all1['latitude'] == a) & (df_all1['solar_longitude'] == b)]
        waven = df_wavsplit['flux'].sum()
        waven = waven * 1.6E-19 * 88775 #convert back to energy/day
        df_wavsum = pd.DataFrame([{'latitude':a, 'solar_longitude':b, 'flux':waven}])
        allwavelengths1 = pd.concat([allwavelengths1, df_wavsum])

df_all2 = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux'])
for wave in wavelengths:
    input_loc2 = datapath + 'integrated_flux_' + str(wave) + '_' + str(panel_angle2) + 'degrees' + '_azimuth_' + str(panel_direction2)
    #input_loc2 = datapath + 'integrated_flux_' + str(wave) + '_' + str(panel_angle2) + 'degrees' + 'south'
    df = pd.read_csv(input_loc2)
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
    df['wavelength'] = waveint
    df_all2 = pd.concat([df_all2, df])

allwavelengths2 = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux'])
for a in latitudes:
    for b in solar_longs:
        df_wavsplit = df_all2[(df_all1['latitude'] == a) & (df_all2['solar_longitude'] == b)]
        waven = df_wavsplit['flux'].sum()
        waven = waven * 1.6E-19 * 88775 #convert back to energy/day
        df_wavsum = pd.DataFrame([{'latitude':a, 'solar_longitude':b, 'flux':waven}])
        allwavelengths2 = pd.concat([allwavelengths2, df_wavsum])

sns.set(rc={'figure.figsize':(19.2,10.8)})

allwavelengths1['flux'] = allwavelengths1['flux']/1000000 #unit conversion for plot
allwavelengths2['flux'] = allwavelengths2['flux']/1000000 #unit conversion for plot


allwavelengths = allwavelengths1.copy(deep=True)
print(allwavelengths)
allwavelengths.insert(3, 'flux2', allwavelengths2['flux'])
#allwavelengths['flux'] = allwavelengths['flux'].replace(0,1)
#allwavelengths['flux2'] = allwavelengths['flux2'].replace(0,1)
print(allwavelengths)
allwavelengths['ratio'] = allwavelengths['flux'] / allwavelengths['flux2']
allwavelengths = allwavelengths.drop(columns=['flux2'])
allwavelengths = allwavelengths.drop(columns=['flux'])

sns.set(font_scale=2)
allwavelengths = allwavelengths.pivot('latitude', 'solar_longitude', 'ratio')
print(allwavelengths)
hm = sns.heatmap(allwavelengths, norm=LogNorm(), cmap='viridis', xticklabels = 6, yticklabels = 3, cbar_kws={'label': 'Energy per Sol Ratio (Logarithmic Scale)'})
hm = hm.invert_yaxis()
hm = plt.xlabel('Solar Longitude ($^\circ$)')
hm = plt.ylabel('Latitude ($^\circ$)')
hm = plt.title('Available Solar Energy for a ' + str(panel_angle1) + '\u00b0 (facing az ' + str(panel_direction1) + '\u00b0) vs ' + str(panel_angle2) + '\u00b0 (facing az ' + str(panel_direction2) + '\u00b0) Degree Panel')
hm = plt.savefig(save_loc)
print('All plots completed.')
plt.show()
