import pickle
import numpy as np 
import matplotlib as mpl
import matplotlib.pylab as plt
from matplotlib.markers import MarkerStyle

for i in [1,2,7]:
    rvir = pickle.load(open(f'../DataFiles/MilkyWay.{i}.sim.Yov.pickle','rb'))
    r300 = pickle.load(open(f'../DataFiles/MilkyWay.{i}.300.Yov.pickle','rb'))
    svir = pickle.load(open(f'../DataFiles/Satellite.{i}.sim.Yov.pickle','rb'))
    s300 = pickle.load(open(f'../DataFiles/Satellite.{i}.300.Yov.pickle','rb'))

    f,ax = plt.subplots(1,1,figsize=(8,6))
    ax.set_ylabel(r'f$_q$',fontsize=15)
    ax.set_xlabel(r'Closest Milky Way or Larger [Mpc]',fontsize=15)
    ax.tick_params(labelsize=12)
    ax.set_xlim([.06,5])
    ax.set_ylim([-.15,1.03])
    ax.semilogx()
    ax.plot([-1,11],[1,1],c='.5',linestyle=':',zorder=0)
    ax.plot([-1,11],[0,0],c='.5',linestyle=':',zorder=0)
    ax.axvline(.767,linestyle='--',label='MW - M31',color='.5',zorder=1)

    rvx,rvy,rvn,rvi,r3x,r3y,r3n,r3i = [],[],[],[],[],[],[],[]
    #Lower hemispheres; Rvir
    for mw in rvir:
        t,q = 0,0
        for sat in rvir[mw]['Satellites']:
            if svir[sat]['Mstar']>1e8:
                t+=1
                if svir[sat]['Quenched']: q+=1
        if t>0:
            rvx.append(rvir[mw]['Closest_MW+'][0]/1e3)
            rvy.append(q/t)
            rvn.append(t)
            rvi.append(mw)
    
    #Upper hemispheres; 300kpc
    for mw in r300:
        t,q = 0,0
        for sat in r300[mw]['Satellites']:
            if s300[sat]['Mstar']>1e8:
                t+=1
                if s300[sat]['Quenched']: q+=1
        if t>0:
            r3x.append(r300[mw]['Closest_MW+'][0]/1e3)
            r3y.append(q/t)
            r3n.append(t)
            r3i.append(mw)

    #Vertical Lines        
    for mw in rvi:
        if mw in r3i:
            up = rvy[rvi.index(mw)]
            dn = r3y[r3i.index(mw)]
            x = rvx[rvi.index(mw)]
            ax.vlines(x,ymin=min([up,dn]),ymax=max([up,dn]),color='k',zorder=0)

    norm = mpl.colors.BoundaryNorm(np.arange(.5,max(rvn+r3n)+1.5), mpl.cm.viridis.N)
    p = ax.scatter(r3x,r3y,c=r3n,cmap='viridis',norm=norm,marker=MarkerStyle('o', fillstyle='top'),s=7**2,label='300 kpc')
    ax.scatter(rvx,rvy,c=rvn,cmap='viridis',norm=norm,marker=MarkerStyle('o', fillstyle='bottom'),s=7**2,label=r'R$_{vir}$')
    cbar = f.colorbar(p,cax=f.add_axes([.91,.11,.03,.77]))
    cbar.set_label(r'N$_{sat}$',fontsize=15)
    cbar.set_ticks(np.arange(1,max(rvn+r3n)+1))
    ax.legend(loc='lower left',prop={'size':15},ncol=3)
    f.savefig(f'Data/QuenchedFractionComp.{i}.png',bbox_inches='tight',pad_inches=.1)