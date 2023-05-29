import pickle
import numpy as np 
import matplotlib as mpl
import matplotlib.pylab as plt
from matplotlib.markers import MarkerStyle

NoBH = False
Weight = False
MagCut = True
lines = 'semi'#['yes','semi','no']
sw = 10**(11) #scale weight
app = '.Subset' if NoBH else ''
appw = '.Weighted' if Weight else ''
appm = '.MagCut' if MagCut else ''
SB = pickle.load(open('../DataFiles/SBProfiles.pickle','rb'))

for i in [1,2,7]:
    rvir = pickle.load(open(f'../DataFiles/MilkyWay.{i}.sim.Yov.pickle','rb'))
    r300 = pickle.load(open(f'../DataFiles/MilkyWay.{i}.300.Yov.pickle','rb'))
    svir = pickle.load(open(f'../DataFiles/Satellite.{i}.sim.Yov.pickle','rb'))
    s300 = pickle.load(open(f'../DataFiles/Satellite.{i}.300.Yov.pickle','rb'))
    with open(f'../DataFiles/Satellite.{i}.sim.Yov.BlackHoles.txt') as f:
        bvir = f.readlines()
        bvir = [x.rstrip('\n') for x in bvir]
    with open(f'../DataFiles/Satellite.{i}.300.Yov.BlackHoles.txt') as f:
        b300 = f.readlines()
        b300 = [x.rstrip('\n') for x in b300]

    f,ax = plt.subplots(1,1,figsize=(8,6))
    ax.set_ylabel(r'N$_{sat,SF}$',fontsize=25)
    ax.set_xlabel(r'D$_{MW+}$ [Mpc]',fontsize=25)
    ax.tick_params(labelsize=20)
    ax.set_xlim([2e-1,5])
    #ax.set_ylim([-.15,1.03])
    ax.semilogx()
    ax.axvline(.767,linestyle='--',label='MW - M31',color='.5',zorder=0)
    ax.axvline(1,color='.5',zorder=0)
    ax.text(.925,.5,'Pairs',rotation='vertical',horizontalalignment='center',verticalalignment='center',color='.5',fontsize=18)
    ax.text(1.12,.5,'Isolated',rotation='vertical',horizontalalignment='center',verticalalignment='center',color='.5',fontsize=18)

    rvx,rvy,rvn,rvi,r3x,r3y,r3n,r3i = [],[],[],[],[],[],[],[]
    #Lower hemispheres; Rvir
    for mw in rvir:
        t,sf = 0,0
        for sat in rvir[mw]['Satellites']:
            if NoBH:
                BHCheck=True if sat not in bvir else False
            else: BHCheck=True
            if MagCut:
                MagCheck=True if SB[sat]['Mueff,r']<25 else False
            else: MagCheck=True
            if svir[sat]['Mstar']>1e8 and BHCheck and MagCheck:
                t+=1
                if not svir[sat]['Quenched']: sf+=1
        if t>0:
            rvx.append(rvir[mw]['Closest_MW+'][0]/1e3)
            w = rvir[mw]['Mstar']/sw if Weight else 1
            rvy.append(sf)
            rvn.append(t)
            rvi.append(mw)
    
    #Upper hemispheres; 300kpc
    for mw in r300:
        t,sf = 0,0
        for sat in r300[mw]['Satellites']:
            if NoBH:
                BHCheck=True if sat not in b300 else False
            else: BHCheck=True
            if MagCut:
                MagCheck=True if SB[sat]['Mueff,r']<25 else False
            if s300[sat]['Mstar']>1e8 and BHCheck and MagCheck:
                t+=1
                if not s300[sat]['Quenched']: sf+=1
        if t>0:
            r3x.append(r300[mw]['Closest_MW+'][0]/1e3)
            w = r300[mw]['Mstar']/sw if Weight else 1
            r3y.append(sf)
            r3n.append(t)
            r3i.append(mw)

    #Vertical Lines        
    for mw in rvi:
        if mw in r3i:
            up = rvy[rvi.index(mw)]
            dn = r3y[r3i.index(mw)]
            x = rvx[rvi.index(mw)]
            if lines=='yes':
                ax.vlines(x,ymin=min([up,dn]),ymax=max([up,dn]),color='k',zorder=0)
            elif lines=='semi':
                ax.vlines(x,ymin=min([up,dn]),ymax=max([up,dn]),color='.5',zorder=0)

    norm = mpl.colors.BoundaryNorm(np.arange(.5,max(rvn+r3n)+1.5), mpl.cm.viridis.N)
    p = ax.scatter(r3x,r3y,c=r3n,cmap='viridis',norm=norm,marker=MarkerStyle('o', fillstyle='top'),s=7**2,label='300 kpc')
    ax.scatter(rvx,rvy,c=rvn,cmap='viridis',norm=norm,marker=MarkerStyle('o', fillstyle='bottom'),s=7**2,label=r'R$_{vir}$')
    cbar = f.colorbar(p,cax=f.add_axes([.91,.11,.03,.77]))
    cbar.set_label(r'N$_{sat}$ [M$_*>10^8$ M$_\odot$]',fontsize=25)
    cbar.ax.tick_params(labelsize=20)
    cbar.set_ticks(np.arange(1,max(rvn+r3n)+1))
    #Add medians
    ax.scatter(.925,np.mean(np.array(r3y)[np.where(np.array(r3x)<1)]),c='r',marker=MarkerStyle('D', fillstyle='top'),s=7**2)
    ax.scatter(1.12,np.mean(np.array(r3y)[np.where(np.array(r3x)>1)]),c='r',marker=MarkerStyle('D', fillstyle='top'),s=7**2)
    ax.scatter(.925,np.mean(np.array(rvy)[np.where(np.array(rvx)<1)]),c='r',marker=MarkerStyle('D', fillstyle='bottom'),s=7**2)
    ax.scatter(1.12,np.mean(np.array(rvy)[np.where(np.array(rvx)>1)]),c='r',marker=MarkerStyle('D', fillstyle='bottom'),s=7**2)
    ax.vlines(.925,ymin=min([np.mean(np.array(r3y)[np.where(np.array(r3x)<1)]),np.mean(np.array(rvy)[np.where(np.array(rvx)<1)])]),zorder=0,
                   ymax=max([np.mean(np.array(r3y)[np.where(np.array(r3x)<1)]),np.mean(np.array(rvy)[np.where(np.array(rvx)<1)])]),color='k')
    ax.vlines(1.12,ymin=min([np.mean(np.array(r3y)[np.where(np.array(r3x)>1)]),np.mean(np.array(rvy)[np.where(np.array(rvx)>1)])]),zorder=0,
                   ymax=max([np.mean(np.array(r3y)[np.where(np.array(r3x)>1)]),np.mean(np.array(rvy)[np.where(np.array(rvx)>1)])]),color='k')
    ax.scatter(-1,-1,c='r',marker='D',s=7**2,label='Mean')
    ax.set_ylim([-.8,max(rvy+r3y)+.5])
    ax.legend(loc='lower left',prop={'size':14.4},ncol=4)
    f.savefig(f'Data/StarFormingComp{app}{appm}{appw}.{i}.png',bbox_inches='tight',pad_inches=.1)