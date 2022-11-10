import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from scipy.integrate import *
import sys

def dist_calc(thetas):
	a=227.92 # 10^6 km
	e=0.0935
	costheta=np.cos(np.radians(thetas))
	r1=a*(1-e**2.0)/(1+e*costheta)
	r1=r1/149.597 # puts R in AU (1AU=1.49.597E6 km)
	return r1
	
theta=np.arange(0., 355., 10.0) #[float(sys.argv[1])]#

R=dist_calc(theta)

SolarData=open("whole_solar_spec_zeroairmass.txt", "r").readlines()

wavl_min=float(sys.argv[1])#0.315
wavl_max=float(sys.argv[2])#0.380

SD_wavl=[]
SD_fluxdens=[]

for line in SolarData[1:len(SolarData)]:
	temp=line.split()
	SD_wavl.append(float(temp[0]))
	SD_fluxdens.append(float(temp[1]))

SD_wavl=np.array(SD_wavl)
SD_fluxdens=np.array(SD_fluxdens)


index=np.where(SD_wavl>wavl_min)
SD_wavl=SD_wavl[index]
SD_fluxdens=SD_fluxdens[index]

index=np.where(SD_wavl<wavl_max)
SD_wavl=SD_wavl[index]
SD_fluxdens=SD_fluxdens[index]


F=trapz(SD_fluxdens, SD_wavl)

Fmars=F/R**2.0

#my theta and Ls theta are 90 degrees out - Ls at aphelion is 90 degrees, Ls at perihelion is 270 degrees
theta=theta-90.0
theta[np.where(theta < 0.0)]=theta[np.where(theta < 0.0)]+360.0
sorted_args=np.argsort(theta)

theta=theta[sorted_args]
Fmars=Fmars[sorted_args]

for i in range(0, len(Fmars)):
	print theta[i], Fmars[i]

Dmars_mean=1.524
Dmars_aph=1.666
Dmars_peri=1.38

print "##################################################"

print "Mean mars distance, flux in UVA band=", F/(Dmars_mean**2.0)
print "Aph mars distance, flux in UVA band=", F/(Dmars_aph**2.0)
print "Peri mars distance, flux in UVA band=", F/(Dmars_peri**2.0)

print "##################################################"

