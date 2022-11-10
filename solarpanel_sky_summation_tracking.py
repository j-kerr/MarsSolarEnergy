#!/usr/bin/env python3
#Reduces solar energy file sizes and formats them for use with other analysis scripts
#Justin Kerr, May 2022

import multiprocessing
import numpy as np
import sys
import os
import pandas as pd
from scipy.interpolate import griddata

input_folder = '../Solar_Energy/Results/' #insert filepath to results folder containing data here
datapath = './Data/'
wavelengths = ['425nm', '475nm', '525nm', '575nm', '625nm', '675nm', '725nm', '775nm', '825nm', '875nm', '925nm', '975nm', '1050nm', '1150nm', '1250nm', '1350nm', 'UVA', 'UVB']
latitudes = range(-90,100,10)
solar_longs = range(0,360,10) #***SOME LONGITUDES MISSING FOR <-60 LATITUDES***
marshourinseconds=88775.245/24.0

def skysum(wave):
    input_loc_all = input_folder + 'June2019_' + str(wave) + '/all_outputs.txt'
    df_all = pd.read_csv(input_loc_all, names=['solar longitude', 'latitude', 'longitude', 'azimuth', 'zenith', 'local true solar time', 'direct flux downward', 'diffuse flux downward', 'diffuse flux upward'])
    df_all = df_all.round({'zenith': 4})
    results = pd.DataFrame(columns=['latitude','longitude','energy','wavelength'])
    input_loc = input_folder + 'June2019_' + str(wave) + '/'
    save_name = 'summedflux_' + wave


    for a in latitudes:
        for b in solar_longs:
            df_outputs = pd.DataFrame(columns=['ltst', 'solarzenith', 'solarazimuth', 'flux'])
            rootdir = input_loc + 'Lat' + str(a) +'/' + 'Ls' + str(b)
            print('Now processing ' + rootdir + '...')
            #print(df_all)
            time = df_all.loc[(df_all['solar longitude'] == b) & (df_all['latitude'] == a)]['local true solar time'].to_numpy()
            time = time.transpose()
            if os.path.exists(rootdir) == True:
                for filename in os.listdir(rootdir):
                    data = rootdir + '/' + filename
                    #get zentih values and create list of column names for the data frame
                    zeniths = np.ndarray.tolist(np.loadtxt(data, skiprows = 229, max_rows = 1))
                    zeniths.insert(0, 'azimuth')
                    #load data into pandas dataframe with each row containing the azimuth value followed by intensity at each zenith value
                    df = pd.DataFrame(np.genfromtxt(data, skip_header = 364, usecols = (range(1,52))))
                    df_up = pd.DataFrame(np.genfromtxt(data, skip_header = 321, usecols = (range(1,52)), max_rows = 38))
                    df_gauss = pd.DataFrame(np.genfromtxt(data, skip_header = 64, usecols = (1,2,3), max_rows = 50), columns = ['mu', 'wt', 'zenith'])

                    df.columns = zeniths
                    azimuths = df['azimuth']
                    df = df.set_index('azimuth')
                    df_up.columns = zeniths
                    df_up = df_up.set_index('azimuth')

                    print(a)
                    print(b)
                    print(filename)

                    try:
                        df_totals = pd.DataFrame(np.genfromtxt(data, skip_header = 128, usecols = (3,4,5,6), max_rows = 1))
                    except ValueError:
                        print('Broken output file (Negative values)! ' + str(filename) + ' in ' + str(rootdir))
                        continue
                    df_totals = df_totals.T
                    df_totals.columns = 'DFD', 'FD', 'FU', 'FNET'
                    #print(df_totals)
                    #tidy data
                    #print(df)
                    df = df.stack()
                    df.index = df.index.rename('zenith', level=1)
                    df.name = 'intensity'
                    df = df.reset_index()
                    df.head(10)
                    #reflect for whole sky
                    df_reflect = df.copy(deep=True)
                    df_reflect = df.reindex(index=df.index[::-1]) #set order for reflection - could just sort later instead
                    df_reflect['azimuth'] = 360 - df_reflect['azimuth']   #set reflected azimuth values
                    df_reflect = df_reflect[df_reflect.azimuth !=180] #don't duplicate 180 degrees
                    df_reflect = df_reflect[df_reflect.azimuth !=360] #don't duplicate 0/360

                    #create whole sky dataframe
                    df = df.append(df_reflect, ignore_index=True)

                    df_up = df_up.stack()
                    df_up.index = df_up.index.rename('zenith', level=1)
                    df_up.name = 'intensity'
                    df_up = df_up.reset_index()
                    df_up.head(10)                    #get zentih values and create list of column names for the data frame

                    df_up_reflect = df_up.copy(deep=True)
                    df_up_reflect = df_up.reindex(index=df.index[::-1]) #set order for reflection - could just sort later instead
                    df_up_reflect['azimuth'] = 360 - df_up_reflect['azimuth']   #set reflected azimuth values
                    df_up_reflect = df_up_reflect[df_up_reflect.azimuth !=180] #don't duplicate 180 degrees
                    df_up_reflect = df_up_reflect[df_up_reflect.azimuth !=360] #don't duplicate 0/360
                    df_up = df_up.append(df_up_reflect, ignore_index=True)

                    #print(df)
                    #Find solar zenith

                    file = open(data)
                    all_lines = file.readlines()
                    solar_zen_line = all_lines[116]
                    solar_zen = []
                    for n in solar_zen_line.split():
                        try:
                            solar_zen.append(float(n))
                        except ValueError:
                            pass

                    azimuths = df['azimuth'].copy(deep=True)
                    azimuths = azimuths.drop_duplicates().values
                    deltaaz = []
                    deltaaz.append(0+(azimuths[1]-azimuths[0]) + (360 - azimuths[len(azimuths)-1]))


                    for i in range(1, (len(azimuths)-1)):
                        deltaaz.append(np.abs((azimuths[i] - azimuths[i-1]) + (azimuths[i+1] - azimuths[i])))
                    deltaaz.append((azimuths[len(azimuths)-1] - azimuths[len(azimuths)-2] + (360-azimuths[len(azimuths)-1])))
                    deltaaz = np.deg2rad(deltaaz)

                    az_df = pd.DataFrame({'azimuth': azimuths, 'deltaaz': deltaaz})
                    df = pd.merge(df, az_df, on = 'azimuth', how = 'inner')
                    df = pd.merge(df, df_gauss, on = 'zenith', how = 'inner')
                    df['intensity'] = df['intensity'] * df['wt'] * df['deltaaz']/2

                    df_up = pd.merge(df_up, az_df, on = 'azimuth', how = 'inner')
                    df_up = pd.merge(df_up, df_gauss, on = 'zenith', how = 'inner')
                    df_up['intensity'] = df_up['intensity'] * df_up['wt'] * df_up['deltaaz']/2
                    df_up['zenith'] = 180 - df_up['zenith']
                    #Get solar azimuth
                    solaraz = df_all.loc[(df_all['latitude'] == a) & (df_all['solar longitude'] == b) & (df_all['zenith'] == solar_zen[0]), 'azimuth'].values #find azimuth of sun from all outputs file

                    #Set panel angle perpendicular to sun
                    norm_angle = solar_zen[0]
                    panel_angle = norm_angle #angle from side opposite sun
                    df = pd.concat([df, df_up])
                    #convert to flux and add direct flux
                    dfd_rad =  df_totals.loc[0].at['DFD']/np.abs(np.cos(np.deg2rad(solar_zen[0])))
                    df['intensity'] = df['intensity'] * np.abs((np.sin(np.deg2rad(norm_angle)) * np.sin(np.deg2rad(df['zenith'])) * np.cos(np.deg2rad(df['azimuth']))) + (np.cos(np.deg2rad(norm_angle))*np.cos(np.deg2rad(df['zenith']))))
                    dfd_rad =  df_totals.loc[0].at['DFD']/np.cos(np.deg2rad(solar_zen[0])) * np.abs((np.sin(np.deg2rad(norm_angle)) * np.sin(np.deg2rad(solar_zen[0])) * np.cos(np.deg2rad(0))) + (np.cos(np.deg2rad(norm_angle))*np.cos(np.deg2rad(solar_zen[0]))))
                    dfd_data = {'azimuth': 0, 'zenith': solar_zen[0], 'intensity': dfd_rad}
                    df_dfd = pd.DataFrame([dfd_data])
                    df = pd.concat([df, df_dfd])
                    df = df.drop(columns = ['wt'])
                    df['intensity'].loc[(((df['azimuth'] >= 90) & (df['azimuth'] <= 270)) & ((90 - panel_angle) < df['zenith']))] = 0
                    df['intensity'].loc[(((df['azimuth'] < 90) | (df['azimuth'] > 270)) & ((90 + panel_angle) < df['zenith']))] = 0
                    #Filter out points behind panel
                    #Sum over each point
                    flux = df['intensity'].sum()
                    df_flux = pd.DataFrame([{'solarzenith': solar_zen[0], 'solarazimuth': solaraz[0], 'flux': flux}])
                    ltst = df_all.loc[(df_all['latitude'] == a) & (df_all['solar longitude'] == b) & (df_all['zenith'] == solar_zen[0]), 'local true solar time'].values #find ltst from all outputs file
                    df_flux.insert(0, 'ltst', ltst[0])
                    df_outputs = pd.concat([df_outputs, df_flux])
                    test = df.intensity.values.sum()
                    alltot = df_totals['FD'].values[0] + df_totals['DFD'].values[0]
                    print('Flux from Top of File: ' + str(alltot))
                    print('Sum of fluxes: ' + str(test))

            else:
                print('No data for latitude' + str(a) +', longitude' + str(b))
            save_loc = datapath + save_name + '_latitude_' + str(a) + '_solarlongitude_' + str(b) + '_' + 'tracking'
            df_outputs.to_csv(path_or_buf=save_loc, index=False)
            print('Saved data for ' + str(wave) +' latitude ' + str(a) + ' solar longitude ' + str(b))


if __name__ == '__main__':
	print(f'Running analysis on {multiprocessing.cpu_count()} CPU cores')
	pool_obj = multiprocessing.Pool()
	pool_obj.map(skysum, wavelengths)
