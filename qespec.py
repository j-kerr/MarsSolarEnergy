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
from scipy import integrate

panel_angle = 45
panel_direction = 90
save_loc =  './Plots/qespec' + str(panel_angle) + 'degree_' + str(panel_direction) + 'azimuth_heatmap_all.png' #insert filepath to output folder and desired name
filename = 'qe_whole_sky_heatmap_' + str(panel_angle) + '.png' #output file name
wavelengths = ['UVCi', 'UVCii', 'UVCiii', 'UVCiv', 'UVB', 'UVA', '425nm', '475nm', '525nm', '575nm', '625nm', '675nm', '725nm', '775nm', '825nm', '875nm', '925nm', '975nm', '1050nm', '1150nm', '1250nm', '1350nm', '1450nm', '1550nm', '1650nm', '1750nm', '1850nm', '1950nm']
solar_longs = range(0,360,10) #***SOME LONGITUDES MISSING FOR <-60 LATITUDES***
datapath = './Data/'

df_all = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux', 'wavelength'])
for wave in wavelengths:
    a = 0
    b = 0
    input_loc = datapath + 'integrated_flux_' + str(wave) + '_' + str(panel_angle) + 'degrees' + '_azimuth_' + str(panel_direction)
    df = pd.read_csv(input_loc)

    #Convert to photons/second, multiply by quantum efficiency
    if  wave == '1450nm':
        waveint = 1450
    elif wave == '1550nm':
        waveint = 1550
    elif wave == '1650nm':
        waveint = 1650
    elif wave == '1750nm':
        waveint = 1750
    elif wave == '1850nm':
        waveint = 1850
    elif wave == '1950nm':
        waveint = 1950
    elif wave == 'UVCi':
        waveint = 210
    elif wave == 'UVCii':
        waveint = 230
    elif wave == 'UVCiii':
        waveint = 250
    elif wave == 'UVCiv':
        waveint = 270
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
    df_wavsplit = df[(df['latitude'] == a) & (df['solar_longitude'] == b)]
    waven = df_wavsplit['flux'].sum()
    waven = waven * 1.6E-19 * 88775 #convert back to energy/day
    df_wavsum = pd.DataFrame([{'latitude':a, 'solar_longitude':b, 'flux':waven, 'wave': waveint}])
    df_all = pd.concat([df_all, df_wavsum])
    print(df_all)
df_all['flux'] = df_all['flux']/1000000 #unit conversion for plot
x = df_all['wave'].to_numpy()
y = df_all['flux'].to_numpy()
#allwavelengths = df_all.pivot('latitude', 'solar_longitude', 'flux')
print(x)
print(y)
hm = plt.plot(x, y)
hm = plt.xlabel('Wavelength (nm)')
hm = plt.ylabel('Daily Solar Flux at Lat 0, Ls 0 (10^6 J)')
hm = plt.title('Mars Surface Solar Panel Energy by Wavelength')
hm = plt.savefig(save_loc)
print('All plots completed.')
plt.show()
exit()
allwavelengths = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux'])
for a in latitudes:
    for b in solar_longs:
        df_wavsplit = df_all[(df_all['latitude'] == a) & (df_all['solar_longitude'] == b)]
        wavfl = df_wavsplit['flux'].to_numpy()
        waves = df_wavsplit['wavelength'].to_numpy()
        waven = df_wavsplit['flux'].sum()
        waven = waven * 1.6E-19 * 88775 #convert back to energy/day
        df_wavsum = pd.DataFrame([{'latitude':a, 'solar_longitude':b, 'flux':waven}])
        allwavelengths = pd.concat([allwavelengths, df_wavsum])
        print(waven)

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
