"""utm.py - minimal UTM forward conversion (WGS84) for Zone 18N georeferencing."""
import math
def ll2utm(lat,lon,zone=18):
    a=6378137.0; f=1/298.257223563; e2=f*(2-f); ep2=e2/(1-e2)
    k0=0.9996; lon0=math.radians(-183+6*zone)
    lat=math.radians(lat); lon=math.radians(lon)
    N=a/math.sqrt(1-e2*math.sin(lat)**2); T=math.tan(lat)**2
    C=ep2*math.cos(lat)**2; A=(lon-lon0)*math.cos(lat)
    M=a*((1-e2/4-3*e2**2/64-5*e2**3/256)*lat
       -(3*e2/8+3*e2**2/32+45*e2**3/1024)*math.sin(2*lat)
       +(15*e2**2/256+45*e2**3/1024)*math.sin(4*lat)
       -(35*e2**3/3072)*math.sin(6*lat))
    E=k0*N*(A+(1-T+C)*A**3/6+(5-18*T+T**2+72*C-58*ep2)*A**5/120)+500000
    Nn=k0*(M+N*math.tan(lat)*(A**2/2+(5-T+9*C+4*C**2)*A**4/24
       +(61-58*T+T**2+600*C-330*ep2)*A**6/720))
    return E,Nn
def dms(d,m,s,west=True): 
    v=d+m/60+s/3600
    return -v if west else v
