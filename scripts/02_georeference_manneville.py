"""
02_georeference_manneville.py
Georeference the GM-49463 1:10,000 compilation map (lat/long graticule) to UTM Zone 18N,
then convert the digitized Manneville-Fault pixel trace to UTM and fit its strike.

The pixel->UTM transform is built from the map neat-line corners whose graticule values are
77 deg 30'00" W (top-left) and 77 deg 22'30" W / 48 deg 22'30" N (top-right), assuming an
isotropic map scale. Reconstructing the NE corner from the transform reproduces the printed
graticule value to the metre. Outputs are stored in georef4.npz and mann.npz.

NOTE: the Manneville trace was digitized by hand from the georeferenced raster (corner-only
graticule, NAD27, scan distortion) -> absolute accuracy ~ +/-100-150 m. The pixel picks are
embedded below for reproducibility.
"""
import numpy as np
from utm import ll2utm                              # local UTM forward (WGS84)

# --- graticule corners (deg) ---
TL_ll=(48+22.5/60, -(77+30/60)); TR_ll=(48+22.5/60, -(77+22.5/60))
TL=np.array(ll2utm(*TL_ll)); TR=np.array(ll2utm(*TR_ll))

# --- neat-line pixels (from 300-dpi raster of GM-49463 sheet 4) ---
lL,rR,tT = 28, 3822, 241                            # left, right, top neat-line columns/row
uhat=(TR-TL)/np.linalg.norm(TR-TL); scale=np.linalg.norm(TR-TL)/(rR-lL)
vhat=np.array([uhat[1],-uhat[0]]);  vhat = vhat if vhat[1]<0 else -vhat
def px2utm(col,row): return TL + (col-lL)*scale*uhat + (row-tT)*scale*vhat
np.savez("../data/processed/georef4.npz", TL=TL,lL=lL,tT=tT,scale=scale,uhat=uhat,vhat=vhat)

# --- digitized Manneville lineament (col%, row%) on the same raster, NW->SE ---
pts_pct=[(40,53),(52,58),(63,65),(75,73),(86,80)]
W,H=4037,3485
mann=np.array([px2utm(c/100*W, r/100*H) for c,r in pts_pct])
Afit=np.polyfit(mann[:,0],mann[:,1],1)              # N = a*E + b
dE,dN=mann[-1]-mann[0]; azim=(np.degrees(np.arctan2(dE,dN)))%360
np.savez("../data/processed/mann.npz", mann=mann, fit=Afit, azim=azim)
print("Graticule check (NE corner): %s  vs printed %s" % (px2utm(rR,tT).round(0), TR.round(0)))
print("Manneville strike: %.1f deg (N%.0fW);  fit  N = %.4f*E + %.0f" % (azim, 180-azim, Afit[0], Afit[1]))
