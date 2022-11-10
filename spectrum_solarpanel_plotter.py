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
save_loc =  './Plots/spectrum.png' #insert filepath to output folder and desired name
filename = 'whole_sky_heatmap_' + str(panel_angle) + 'south.png' #output file name
wavelengths = ['UVCi', 'UVCii', 'UVCiii', 'UVCiv', 'UVB', 'UVA', '425nm', '475nm', '525nm', '575nm', '625nm', '675nm', '725nm', '775nm', '825nm', '875nm', '925nm', '975nm', '1050nm', '1150nm', '1250nm', '1350nm', '1450nm', '1550nm', '1650nm', '1750nm', '1850nm', '1950nm']
latitudes = range(-90,100,10)
solar_longs = range(0,360,10) #***SOME LONGITUDES MISSING FOR <-60 LATITUDES***
datapath = './Data/'

df_all = pd.DataFrame(columns=['latitude', 'solar_longitude', 'flux', 'wave'])
for wave in wavelengths:
    input_loc = datapath + 'integrated_flux_' + str(wave) + '_' + str(panel_angle) + 'degrees' + '_azimuth_' + str(panel_direction)
    df = pd.read_csv(input_loc)
    a = 0
    b = 0
    df_wavsplit = df[(df['latitude'] == a) & (df['solar_longitude'] == b)]
    waven = df_wavsplit['flux'].sum()
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
        waveint = 358
    elif wave == 'UVB':
        waveint = 298
    elif wave == '425nm':
        waveint = 425
    elif wave == '475nm':
        waveint = 475
    elif wave == '525nm':
        waveint = 525
    elif wave == '575nm':
        waveint = 575
    elif wave == '625nm':
        waveint = 625
    elif wave == '675nm':
        waveint = 675
    elif wave == '725nm':
        waveint = 725
    elif wave == '775nm':
        waveint = 775
    elif wave == '825nm':
        waveint = 825
    elif wave == '875nm':
        waveint = 875
    elif wave == '925nm':
        waveint = 925
    elif wave == '975nm':
        waveint = 975
    elif wave == '1050nm':
        waveint = 1050
    elif wave == '1150nm':
        waveint = 1150
    elif wave == '1250nm':
        waveint = 1250
    elif wave == '1350nm':
        waveint = 1350
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
hm = plt.title('Mars Surface Solar Flux by Wavelength')
hm = plt.savefig(save_loc)
print('All plots completed.')
plt.show()
marssum = np.sum(y)
print(df_all)
df_all.loc[df_all['wave'] == 1450, 'flux'] = df_all.loc[df_all['wave'] == 1450, 'flux'] * 0
df_all.loc[df_all['wave'] == 1550, 'flux'] = df_all.loc[df_all['wave'] == 1550, 'flux'] * 0
df_all.loc[df_all['wave'] == 1650, 'flux'] = df_all.loc[df_all['wave'] == 1650, 'flux'] * 0
df_all.loc[df_all['wave'] == 1750, 'flux'] = df_all.loc[df_all['wave'] == 1750, 'flux'] * 0
df_all.loc[df_all['wave'] == 1850, 'flux'] = df_all.loc[df_all['wave'] == 1850, 'flux'] * 0
df_all.loc[df_all['wave'] == 1950, 'flux'] = df_all.loc[df_all['wave'] == 1950, 'flux'] * 0
df_all.loc[df_all['wave'] == 210, 'flux'] = df_all.loc[df_all['wave'] == 210, 'flux'] * 0
df_all.loc[df_all['wave'] == 230, 'flux'] = df_all.loc[df_all['wave'] == 230, 'flux'] * 0
df_all.loc[df_all['wave'] == 250, 'flux'] = df_all.loc[df_all['wave'] == 250, 'flux'] * 0
df_all.loc[df_all['wave'] == 270, 'flux'] = df_all.loc[df_all['wave'] == 270, 'flux'] * 0
df_all.loc[df_all['wave'] == 358, 'flux'] = df_all.loc[df_all['wave'] == 358, 'flux'] * 0.4
df_all.loc[df_all['wave'] == 298, 'flux'] = df_all.loc[df_all['wave'] == 298, 'flux'] * 0.035
df_all.loc[df_all['wave'] == 425, 'flux'] = df_all.loc[df_all['wave'] == 425, 'flux'] * 0.79
df_all.loc[df_all['wave'] == 475, 'flux'] = df_all.loc[df_all['wave'] == 475, 'flux'] * 0.8
df_all.loc[df_all['wave'] == 525, 'flux'] = df_all.loc[df_all['wave'] == 525, 'flux'] * 0.74
df_all.loc[df_all['wave'] == 575, 'flux'] = df_all.loc[df_all['wave'] == 575, 'flux'] * 0.67
df_all.loc[df_all['wave'] == 625, 'flux'] = df_all.loc[df_all['wave'] == 625, 'flux'] * 0.5
df_all.loc[df_all['wave'] == 675, 'flux'] = df_all.loc[df_all['wave'] == 675, 'flux'] * 0.76
df_all.loc[df_all['wave'] == 725, 'flux'] = df_all.loc[df_all['wave'] == 725, 'flux'] * 0.84
df_all.loc[df_all['wave'] == 775, 'flux'] = df_all.loc[df_all['wave'] == 775, 'flux'] * 0.86
df_all.loc[df_all['wave'] == 825, 'flux'] = df_all.loc[df_all['wave'] == 825, 'flux'] * 0.84
df_all.loc[df_all['wave'] == 875, 'flux'] = df_all.loc[df_all['wave'] == 875, 'flux'] * 0.55
df_all.loc[df_all['wave'] == 925, 'flux'] = df_all.loc[df_all['wave'] == 925, 'flux'] * 0.85
df_all.loc[df_all['wave'] == 975, 'flux'] = df_all.loc[df_all['wave'] == 975, 'flux'] * 0.86
df_all.loc[df_all['wave'] == 1050, 'flux'] = df_all.loc[df_all['wave'] == 1050, 'flux'] * 0.82
df_all.loc[df_all['wave'] == 1150, 'flux'] = df_all.loc[df_all['wave'] == 1150, 'flux'] * 0.76
df_all.loc[df_all['wave'] == 1250, 'flux'] = df_all.loc[df_all['wave'] == 1250, 'flux'] * 0.55
df_all.loc[df_all['wave'] == 1350, 'flux'] = df_all.loc[df_all['wave'] == 1350, 'flux'] * 0.1

qesum = df_all['flux'].sum()
print(qesum)
eff = qesum / marssum
print('Ratio for mars spectrum is ' + str(eff))

df_all.loc[df_all['wave'] == 1450, 'flux'] = 2.6699E-02
df_all.loc[df_all['wave'] == 1550, 'flux'] = 2.6226E-01
df_all.loc[df_all['wave'] == 1650, 'flux'] = 2.1902E-01
df_all.loc[df_all['wave'] == 1750, 'flux'] = 1.6162E-01
df_all.loc[df_all['wave'] == 1850, 'flux'] = 2.9348E-06
df_all.loc[df_all['wave'] == 1950, 'flux'] = 1.6482E-02
df_all.loc[df_all['wave'] == 210, 'flux'] = 0
df_all.loc[df_all['wave'] == 230, 'flux'] = 0
df_all.loc[df_all['wave'] == 250, 'flux'] = 0
df_all.loc[df_all['wave'] == 270, 'flux'] = 0
df_all.loc[df_all['wave'] == 358, 'flux'] = 2.7936E-01
df_all.loc[df_all['wave'] == 298, 'flux'] = 1.1127E-04
df_all.loc[df_all['wave'] == 425, 'flux'] = 9.9312E-01
df_all.loc[df_all['wave'] == 475, 'flux'] = 1.3755E+00
df_all.loc[df_all['wave'] == 525, 'flux'] = 1.3859E+00
df_all.loc[df_all['wave'] == 575, 'flux'] = 1.3225E+00
df_all.loc[df_all['wave'] == 625, 'flux'] = 1.2667E+00
df_all.loc[df_all['wave'] == 675, 'flux'] = 1.2639E+00
df_all.loc[df_all['wave'] == 725, 'flux'] = 9.4741E-01
df_all.loc[df_all['wave'] == 775, 'flux'] = 1.0801E+00
df_all.loc[df_all['wave'] == 825, 'flux'] = 8.9752E-01
df_all.loc[df_all['wave'] == 875, 'flux'] = 8.6204E-01
df_all.loc[df_all['wave'] == 925, 'flux'] = 8.4515E-01
df_all.loc[df_all['wave'] == 975, 'flux'] = 5.5536E-01
df_all.loc[df_all['wave'] == 1050, 'flux'] = 6.1802E-01
df_all.loc[df_all['wave'] == 1150, 'flux'] = 1.1648E-01
df_all.loc[df_all['wave'] == 1250, 'flux'] = 4.3684E-01
df_all.loc[df_all['wave'] == 1350, 'flux'] = 1.5488E-02
earthsum = df_all['flux'].sum()

df_all.loc[df_all['wave'] == 1450, 'flux'] = 0 * 2.6699E-02
df_all.loc[df_all['wave'] == 1550, 'flux'] = 0 * 2.6226E-01
df_all.loc[df_all['wave'] == 1650, 'flux'] = 0 * 2.1902E-01
df_all.loc[df_all['wave'] == 1750, 'flux'] = 0 * 1.6162E-01
df_all.loc[df_all['wave'] == 1850, 'flux'] = 0 * 2.9348E-06
df_all.loc[df_all['wave'] == 1950, 'flux'] = 0 * 1.6482E-02
df_all.loc[df_all['wave'] == 210, 'flux'] = 0
df_all.loc[df_all['wave'] == 230, 'flux'] = 0
df_all.loc[df_all['wave'] == 250, 'flux'] = 0
df_all.loc[df_all['wave'] == 270, 'flux'] = 0
df_all.loc[df_all['wave'] == 358, 'flux'] = 2.7936E-01 * 0.4
df_all.loc[df_all['wave'] == 298, 'flux'] = 1.1127E-04 * 0.035
df_all.loc[df_all['wave'] == 425, 'flux'] = 9.9312E-01 * 0.79
df_all.loc[df_all['wave'] == 475, 'flux'] = 1.3755E+00 * 0.8
df_all.loc[df_all['wave'] == 525, 'flux'] = 1.3859E+00 * 0.74
df_all.loc[df_all['wave'] == 575, 'flux'] = 1.3225E+00 * 0.67
df_all.loc[df_all['wave'] == 625, 'flux'] = 1.2667E+00 * 0.5
df_all.loc[df_all['wave'] == 675, 'flux'] = 1.2639E+00 * 0.76
df_all.loc[df_all['wave'] == 725, 'flux'] = 9.4741E-01 * 0.84
df_all.loc[df_all['wave'] == 775, 'flux'] = 1.0801E+00 * 0.86
df_all.loc[df_all['wave'] == 825, 'flux'] = 8.9752E-01 * 0.84
df_all.loc[df_all['wave'] == 875, 'flux'] = 8.6204E-01 * 0.55
df_all.loc[df_all['wave'] == 925, 'flux'] = 8.4515E-01 * 0.85
df_all.loc[df_all['wave'] == 975, 'flux'] = 5.5536E-01 * 0.86
df_all.loc[df_all['wave'] == 1050, 'flux'] = 6.1802E-01 * 0.82
df_all.loc[df_all['wave'] == 1150, 'flux'] = 1.1648E-01 * 0.76
df_all.loc[df_all['wave'] == 1250, 'flux'] = 4.3684E-01 * 0.55
df_all.loc[df_all['wave'] == 1350, 'flux'] = 1.5488E-02 * 0.1
qeearth = df_all['flux'].sum()

earthratio = qeearth / earthsum

print('Ratio for earth spectrum is ' + str(earthratio))
