"""
03_drill_design.py
Compute collar coordinates, azimuth, dip and target intersections for the three planned
600 m diamond-drill holes testing SFRT targets T1-T3.

Design rule: azimuth 225 deg (grid), perpendicular to the N45W gold-branch strike; collars
NE of and up-dip from each target so the hole drills SW-and-down, cutting the steeply
NE-dipping (WNW-ESE) shears at a high angle. Dips chosen so a 600 m hole brackets each target.
"""
import numpy as np

AZ, LEN = 225.0, 600.0
targets={  # name:(E,N,depth_lo,depth_hi,dip_deg)
 "DDH-LC-01 (T1)":(326054,5356352,250,550,60),
 "DDH-LC-02 (T2)":(325538,5355632,340,660,65),
 "DDH-LC-03 (T3)":(325135,5355067,280,500,58)}
A=np.array([327127,5357856.]); B=np.array([325014,5354896.])
u=(B-A)/np.linalg.norm(B-A); LL=np.linalg.norm(B-A)
das=lambda E,N: 10000+np.dot(np.array([E,N])-A,u)/LL*3500
hdir=np.array([np.sin(np.radians(AZ)), np.cos(np.radians(AZ))])   # SW advance

print(f"{'hole':16s}{'collar_E':>9s}{'collar_N':>10s}{'DAS':>7s}{'az':>5s}{'dip':>5s}"
      f"{'EOH_depth':>10s}  target_MD(from-to)")
for nm,(E,N,zlo,zhi,dip) in targets.items():
    d=np.radians(dip); zc=(zlo+zhi)/2; run=zc/np.tan(d)
    collar=np.array([E,N]) - hdir*run
    md_top, md_bot = zlo/np.sin(d), zhi/np.sin(d)
    print(f"{nm:16s}{collar[0]:9.0f}{collar[1]:10.0f}{das(*collar):7.0f}{AZ:5.0f}{-dip:5.0f}"
          f"{LEN*np.sin(d):10.0f}  {md_top:.0f}-{md_bot:.0f} m")
print("\nGrid convergence ~ -1.7 deg (true az = grid - 1.7); magnetic declination ~ -14 deg (2026).")
print("Collar elevations to be fixed by RTK survey.")
