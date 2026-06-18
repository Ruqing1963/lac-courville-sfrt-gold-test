import numpy as np, matplotlib, math
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from matplotlib.lines import Line2D
from scipy.ndimage import gaussian_filter
OUT='../figures/'
PFIG='../paper/figures/'
def save(fig,name):
    for d in (OUT,PFIG):
        fig.savefig(d+name+'.pdf',bbox_inches='tight'); 
    fig.savefig(OUT+name+'.png',dpi=150,bbox_inches='tight'); plt.close(fig)

# ---------- FIG 1: Zp/Zs ----------
p=np.load('../data/processed/proc.npz'); Zp,Zs,R,score,st,dp=p['Zp'],p['Zs'],p['R'],p['score'],p['st'],p['dp']
ext=[st.min(),st.max(),dp.max(),dp.min()]
F={'F1':10620,'F2':11260,'F3':12100,'F4':13030}
targets=[(11380,12000,120,1000,'T1'),(12380,12840,340,660,'T2'),(13240,13340,280,500,'T3'),(10280,10460,0,170,'T4?')]
fig,axs=plt.subplots(4,1,figsize=(15,17),sharex=True)
def panel(ax,A,title,cmap,vlo,vhi,cb):
    im=ax.imshow(A,aspect='auto',extent=ext,cmap=cmap,vmin=vlo,vmax=vhi,interpolation='bilinear')
    ax.set_ylabel('Depth (m)'); ax.set_title(title,fontsize=13,loc='left',fontweight='bold')
    c=plt.colorbar(im,ax=ax,pad=0.01,fraction=0.025); c.set_label(cb,fontsize=9)
    for k,v in F.items():
        ax.axvline(v,color='k',lw=0.7,ls=':',alpha=0.5); ax.text(v,70,k,ha='center',va='top',fontsize=10,fontweight='bold',bbox=dict(fc='white',ec='none',alpha=0.6,pad=1))
panel(axs[0],Zp,'(a) Zp - P-impedance (used alone in the original report)','jet',np.nanpercentile(Zp,3),np.nanpercentile(Zp,97),'Zp')
panel(axs[1],Zs,'(b) Zs - S-impedance (new): low Zs = shearing / fracturing','jet',np.nanpercentile(Zs,3),np.nanpercentile(Zs,97),'Zs')
panel(axs[2],gaussian_filter(R,1),'(c) Zp/Zs ratio (new): high (red) = fluid-saturated / altered shear damage','RdYlBu_r',np.nanpercentile(R,5),np.nanpercentile(R,95),'Zp/Zs')
ax=axs[3]; sc=gaussian_filter(score,1)
im=ax.imshow(sc,aspect='auto',extent=ext,cmap='inferno',vmin=np.nanpercentile(sc,40),vmax=np.nanpercentile(sc,99),interpolation='bilinear')
ax.set_ylabel('Depth (m)'); ax.set_xlabel('DAS station (~m along Line 1)')
ax.set_title('(d) Composite gold prospectivity = low Zp + high Zp/Zs + structural gradient',fontsize=13,loc='left',fontweight='bold')
c=plt.colorbar(im,ax=ax,pad=0.01,fraction=0.025); c.set_label('score',fontsize=9)
for k,v in F.items(): ax.axvline(v,color='cyan',lw=0.8,ls=':',alpha=0.6); ax.text(v,70,k,ha='center',va='top',fontsize=10,color='cyan',fontweight='bold')
ax.axvspan(12100,13030,color='lime',alpha=0.06)
for d0,d1,z0,z1,lab in targets:
    col='lime' if '?' not in lab else 'white'
    ax.add_patch(Rectangle((d0,z0),d1-d0,z1-z0,fill=False,ec=col,lw=2.2)); ax.text((d0+d1)/2,z0-15,lab,ha='center',va='bottom',color=col,fontsize=12,fontweight='bold')
for a in axs: a.set_ylim(1498,0)
fig.tight_layout(); save(fig,'fig01_zpzs_analysis')

# ---------- FIG 2: structural tie ----------
exec(open('utm.py').read())
poly=np.array([[324545,5354204],[326399,5354147],[326427,5355074],[328898,5354999],
[328982,5357777],[325895,5357870],[325866,5356945],[325249,5356964],[325192,5355113],[324574,5355130]],float)
anch={10000:(327127,5357856),10460:(326854,5357471),10940:(326558,5357057),11500:(326202,5356559),
 11820:(326013,5356294),12380:(325677,5355827),12940:(325339,5355352),13500:(325014,5354896)}
ax_=np.array(sorted(anch)); E=np.array([anch[k][0] for k in ax_]); Nn=np.array([anch[k][1] for k in ax_])
def utm(d): return float(np.interp(d,ax_,E)),float(np.interp(d,ax_,Nn))
das=np.arange(10000,13520,20); LE=np.interp(das,ax_,E); LN=np.interp(das,ax_,Nn)
m=np.load('../data/processed/mann.npz'); mann=m['mann']; Af=m['fit']
zoneA=np.array([321000.,5354500.]); pershing=np.array([318500.,5358800.]); uniacke=np.array([323929.,5360257.])
fig,axp=plt.subplots(figsize=(13.5,9.6))
xs=np.array([317800,326500]); axp.plot(xs,Af[0]*xs+Af[1],color='purple',lw=2.6,zorder=4)
axp.fill_between(xs,Af[0]*xs+Af[1]-700/math.cos(math.atan(Af[0])),Af[0]*xs+Af[1]+700/math.cos(math.atan(Af[0])),color='purple',alpha=0.08,zorder=1)
axp.scatter(mann[:,0],mann[:,1],c='purple',s=18,zorder=5,marker='s')
axp.text(318300,5356000,'Manneville Fault - digitized from\ngeoreferenced GM-49463 (strike N61W)',color='purple',fontsize=9,rotation=-29)
for sk,c in [(305,'#bbb'),(315,'darkorange'),(325,'#bbb')]:
    s=math.radians(sk); d=np.array([math.sin(s),math.cos(s)]); P2=uniacke-d*6500
    axp.plot([uniacke[0],P2[0]],[uniacke[1],P2[1]],ls='--',color=c,lw=2 if sk==315 else 1,alpha=.9,zorder=3)
axp.add_patch(Polygon([uniacke,uniacke-np.array([math.sin(math.radians(305)),math.cos(math.radians(305))])*6500,
   uniacke-np.array([math.sin(math.radians(325)),math.cos(math.radians(325))])*6500],closed=True,fc='orange',alpha=.07,zorder=1))
axp.text(323700,5358600,'Au-bearing porphyry/shear branch\n(N45W) -> projects to Line 1',color='darkorange',fontsize=8.5,rotation=-46)
axp.add_patch(Polygon(poly,closed=True,fc='#3a7',alpha=0.10,ec='green',lw=2))
axp.text(327000,5357500,'Minesound\nLac Courville Property',fontsize=9,color='darkgreen',ha='center',fontweight='bold')
for P,lab,off2 in [(zoneA,'Zone A (GM-46483/73005)\nstockwork 1-7 g/t; free gold 9 g/t',(8,-40)),
                   (pershing,'Pershing-Manitou\n7.9 g/t Au',(6,8)),(uniacke,'Uniacke/Obradovich\nVC-10 23.3 g/t',(8,6))]:
    axp.plot(*P,'^',color='gold',ms=14,mec='k',mew=1.2,zorder=8)
    axp.annotate(lab,P,fontsize=8,xytext=off2,textcoords='offset points',bbox=dict(fc='white',ec='gray',alpha=.88,pad=1.3),zorder=9)
axp.plot(LE,LN,'-',color='black',lw=3.5,zorder=6)
for dd in range(10000,13501,500):
    e,n=utm(dd); axp.plot(e,n,'|',color='k',ms=9,mew=1.4,zorder=7); axp.annotate(str(dd),(e,n),fontsize=7,xytext=(4,-9),textcoords='offset points')
for nm,dd in [('F1',10620),('F2',11260),('F3',12100),('F4',13030)]:
    e,n=utm(dd); axp.plot(e,n,'o',mfc='none',mec='blue',ms=12,mew=1.3,zorder=8); axp.annotate(nm,(e,n),fontsize=8,color='blue',xytext=(-15,5),textcoords='offset points')
for nm,dd in [('T1',11750),('T2',12610),('T3',13290)]:
    e,n=utm(dd); axp.plot(e,n,'*',color='red',ms=18,mec='k',zorder=9); axp.annotate(nm,(e,n),fontsize=11,fontweight='bold',color='red',xytext=(7,4),textcoords='offset points')
e1,n1=utm(10550); e2,n2=utm(11270); axp.plot([e1,e2],[n1,n2],lw=6,color='darkorange',alpha=.4,zorder=5,solid_capstyle='round')
axp.set_xlabel('UTM Easting (Zone 18N, m)'); axp.set_ylabel('UTM Northing (m)')
axp.set_title('Measured structural tie: digitized Manneville Fault + Au-branch projection onto SFRT Line 1',fontsize=12.5,fontweight='bold')
axp.set_aspect('equal'); axp.grid(alpha=.25); axp.set_xlim(316800,329400); axp.set_ylim(5352800,5361200)
leg=[Line2D([0],[0],color='black',lw=3.5,label='SFRT Line 1'),Line2D([0],[0],marker='*',color='red',ls='',ms=13,mec='k',label='Zp/Zs target'),
     Line2D([0],[0],marker='^',color='gold',ls='',ms=11,mec='k',label='Documented Au (drilled)'),Line2D([0],[0],marker='o',mfc='none',mec='blue',ls='',ms=11,label='SFRT shear F1-F4'),
     Line2D([0],[0],color='purple',lw=2.6,label='Manneville Fault (digitized)'),Line2D([0],[0],color='darkorange',lw=2,ls='--',label='Au-branch projection (N45W)'),Line2D([0],[0],color='green',lw=2,label='Property polygon')]
axp.legend(handles=leg,loc='lower right',fontsize=8.3,framealpha=.93); save(fig,'fig02_structural_tie')

# ---------- FIG 3: drill section ----------
A=np.array([327127,5357856.]);B=np.array([325014,5354896.]);u=(B-A)/np.linalg.norm(B-A);LLn=np.linalg.norm(B-A)
def dasf(E,N):return 10000+np.dot(np.array([E,N])-A,u)/LLn*3500
holes={'DDH-LC-01 (T1)':dict(E=326217,N=5356515,dip=60,L=600,c='red'),
       'DDH-LC-02 (T2)':dict(E=325703,N=5355797,dip=65,L=600,c='darkorange'),
       'DDH-LC-03 (T3)':dict(E=325307,N=5355239,dip=58,L=600,c='purple')}
tg=[('T1',11500,12000,250,550),('T2',12380,12840,340,660),('T3',13240,13340,280,500)]
F={'F1':10620,'F2':11260,'F3':12100,'F4':13030}; azL=math.atan2(*(B-A))
fig,ax=plt.subplots(figsize=(14,6.4))
for nm,d0,d1,z0,z1 in tg:
    ax.add_patch(Rectangle((d0,z0),d1-d0,z1-z0,fc='gold',ec='goldenrod',alpha=0.30,lw=1.5)); ax.text((d0+d1)/2,z0-18,nm,ha='center',va='bottom',color='saddlebrown',fontsize=12,fontweight='bold')
for k,v in F.items(): ax.axvline(v,color='steelblue',lw=1,ls=':',alpha=0.7); ax.text(v,-30,k,ha='center',color='steelblue',fontsize=9)
for nm,h in holes.items():
    dc=dasf(h['E'],h['N']); d=math.radians(h['dip']); ang=math.radians(225)-azL
    ax.plot([dc,dc+h['L']*math.cos(d)*math.cos(ang)],[0,h['L']*math.sin(d)],color=h['c'],lw=2.6,zorder=6)
    ax.plot(dc,0,'v',color=h['c'],ms=11,mec='k',zorder=7); ax.annotate(nm,(dc,0),xytext=(0,14),textcoords='offset points',ha='center',color=h['c'],fontsize=9,fontweight='bold')
    ax.plot(dc+h['L']*math.cos(d)*math.cos(ang),h['L']*math.sin(d),'o',color=h['c'],ms=5); ax.text(dc+h['L']*math.cos(d)*math.cos(ang)+20,h['L']*math.sin(d),'600 m',color=h['c'],fontsize=7,va='center')
ax.set_xlim(10000,13550); ax.set_ylim(700,-80); ax.set_xlabel('DAS (along Line 1, ~m)'); ax.set_ylabel('Depth (m)')
ax.set_title('Drill section (projected to Line 1 vertical plane): three 600 m holes testing T1-T3',fontsize=13,fontweight='bold'); ax.grid(alpha=0.25)
ax.legend(handles=[Line2D([0],[0],marker='v',color='red',ls='',ms=10,mec='k',label='Collar (azimuth 225)'),Rectangle((0,0),1,1,fc='gold',ec='goldenrod',alpha=.4,label='Zp/Zs target'),Line2D([0],[0],color='steelblue',ls=':',label='Shear zone F1-F4')],loc='lower left',framealpha=.9)
save(fig,'fig03_drill_section')
print('figures saved'); import os; print(os.listdir(OUT))
