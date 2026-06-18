"""
01_zpzs_analysis.py
Dual-impedance (Zp/Zs) re-analysis of SFRT Line 1, Lac Courville Property.

Input : ../data/raw/Valdor-Zp-f0.txt , ../data/raw/Valdor-Zs.txt
        (3-column ASCII: DAS_station  depth_m  impedance ; 176 stations x 750 depths)
Output: ../data/processed/proc.npz  (Zp, Zs, ratio, detrended fields, prospectivity score)

Method
------
Zp = rho*Vp , Zs = rho*Vs  ->  Zp/Zs = Vp/Vs (density-independent lithology/fluid proxy).
The Line-1 impedances are RELATIVE (uncalibrated): Zp/Zs ~ 1.40-1.55, below physical rock
Vp/Vs (1.7-1.9). All interpretation therefore uses depth-detrended *relative* anomalies.

Composite orogenic-gold prospectivity = relatively LOW Zp (alteration/fracture/fluid, low
velocity) + relatively HIGH Zp/Zs (fluid-saturated shear damage) + HIGH lateral gradient
(structural contact / dilational site).
"""
import numpy as np
from scipy.ndimage import gaussian_filter

RAW = "../data/raw/"
def load(fn):
    d = np.loadtxt(fn); das=d[:,0].astype(int); dep=d[:,1]; val=d[:,2]
    stations=np.unique(das); depths=np.unique(dep)
    grid=np.full((len(depths),len(stations)), np.nan)
    si={s:i for i,s in enumerate(stations)}; di={round(x,1):i for i,x in enumerate(depths)}
    for s,z,v in zip(das,dep,val): grid[di[round(z,1)], si[s]]=v
    return stations, depths, grid

st, dp, Zp = load(RAW+"Valdor-Zp-f0.txt")
st2,dp2,Zs = load(RAW+"Valdor-Zs.txt")
assert np.array_equal(st,st2) and np.array_equal(dp,dp2)

Zp[Zp<1000]=np.nan                                  # remove 2 edge zeros
for r,c in zip(*np.where(np.isnan(Zp))): Zp[r,c]=Zp[r-1,c]
R = Zp/Zs                                           # Vp/Vs proxy

def detrend(A):                                     # subtract median-at-depth, /std-at-depth
    med=np.nanmedian(A,axis=1,keepdims=True); sd=np.nanstd(A,axis=1,keepdims=True)+1e-9
    return (A-med)/sd
Zp_a, Zs_a, R_a = detrend(Zp), detrend(Zs), detrend(R)

gx = np.gradient(gaussian_filter(Zp,2), axis=1)     # lateral gradient (structural edge)
grad_n = (np.abs(gx)-np.nanmean(np.abs(gx)))/np.nanstd(np.abs(gx))

score = gaussian_filter(0.9*(-Zp_a) + 1.0*R_a + 0.8*grad_n, 1.5)

np.savez("../data/processed/proc.npz", Zp=Zp,Zs=Zs,R=R,Zp_a=Zp_a,Zs_a=Zs_a,R_a=R_a,
         grad=grad_n, score=score, st=st, dp=dp)
print("Stations %d  Depths %d" % (len(st),len(dp)))
print("Zp/Zs  min/median/max  %.3f / %.3f / %.3f" % (np.nanmin(R),np.nanmedian(R),np.nanmax(R)))
print("saved ../data/processed/proc.npz")
