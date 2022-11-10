#!/usr/bin/env python3
#Integrates solar energy files over each day and formats them for use with plotting script
#Justin Kerr, May 2022

import multiprocessing
import numpy as np
import sys
import os
import pandas as pd
import scipy.integrate as integrate

panel_angle_list = [15, 30, 45, 60, 75, 90]
panel_direction_list = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
datapath = './Data/' #insert filepath to folder containing data here
wavelengths = ['425nm', '475nm', '525nm', '575nm', '625nm', '675nm', '725nm', '775nm', '825nm', '875nm', '925nm', '975nm', '1050nm', '1150nm', '1250nm', '1350nm',  'UVA', 'UVB']
latitudes = range(-90,100,10)
solar_longs = range(0,360,10) #***SOME LONGITUDES MISSING FOR <-60 LATITUDES***

def integrate_all(wave):
    seconds_per_hour = 88775 / 24
    df_outputs = pd.DataFrame(columns = ['latitude', 'solar_longitude', 'flux'])
    save_loc = datapath + 'integrated_flux_' + str(wave) + '_' + str(panel_angle) + 'degrees' + '_azimuth_' + str(panel_direction)
    for a in latitudes:
        for b in solar_longs:
            input_loc = datapath + 'summedflux_' + str(wave) + '_latitude_' + str(a) + '_solarlongitude_' + str(b) + '_' + str(panel_angle) + 'degrees' + '_azimuth_' + str(panel_direction)
            print(input_loc)
            if os.path.exists(input_loc) == True:
                df = pd.read_csv(input_loc)
                df['ltst'] = df['ltst'] * seconds_per_hour
                df = df.sort_values(by=['ltst'])
                ltst = df['ltst'].to_numpy()
                flux = df['flux'].to_numpy()
                iflux = integrate.trapezoid(flux, ltst)
                #ifluxs = integrate.simpson(flux, ltst)
                print(iflux)
                if iflux >= 0:
                    df_loop = pd.DataFrame([{'latitude': a, 'solar_longitude': b, 'flux': iflux}])
                    df_outputs = pd.concat([df_outputs, df_loop])
                else:
                    df_loop = pd.DataFrame([{'latitude': a, 'solar_longitude': b, 'flux': 0}])
                    df_outputs = pd.concat([df_outputs, df_loop])
                    print('negative for' + str(a) + '_' + str(b))
            else:
                print('No data for' + input_loc)
            print(df_outputs)
    df_outputs.to_csv(path_or_buf=save_loc, index=False)
    print('Saved data for ' + str(wave))
for panel_angle in panel_angle_list:
   for panel_direction in panel_direction_list:
       if __name__ == '__main__':
            print(f'Running analysis on {multiprocessing.cpu_count()} CPU cores')
            pool_obj = multiprocessing.Pool()
            pool_obj.map(integrate_all, wavelengths)
