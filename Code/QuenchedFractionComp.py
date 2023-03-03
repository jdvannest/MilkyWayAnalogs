import pickle
import numpy as np 
import matplotlib as mpl
import matplotlib.pylab as plt
from matplotlib.markers import MarkerStyle

NoBH = False
Weight = True
sw = 10**(11) #scale weight
app = '.Subset' if NoBH else ''
appw = '.Weighted' if Weight else ''

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
    ax.set_ylabel(r'f$_q$',fontsize=25)
    ax.set_xlabel(r'D$_{MW+}$ [Mpc]',fontsize=25)
    ax.tick_params(labelsize=20)
    ax.set_xlim([2e-1,5])
    ax.set_ylim([-.15,1.03])
    ax.semilogx()
    ax.plot([-1,11],[1,1],c='.5',linestyle=':',zorder=0)
    ax.plot([-1,11],[0,0],c='.5',linestyle=':',zorder=0)
    ax.axvline(.767,linestyle='--',label='MW - M31',color='.5',zorder=0)
    ax.axvline(1,color='.5',zorder=0)
    ax.text(.925,.18,'Pairs',rotation='vertical',horizontalalignment='center',verticalalignment='center',color='.5',fontsize=18)
    ax.text(1.12,.18,'Isolated',rotation='vertical',horizontalalignment='center',verticalalignment='center',color='.5',fontsize=18)

    rvx,rvy,rvn,rvi,r3x,r3y,r3n,r3i = [],[],[],[],[],[],[],[]
    #Lower hemispheres; Rvir
    for mw in rvir:
        t,q = 0,0
        for sat in rvir[mw]['Satellites']:
            if svir[sat]['Mstar']>1e8 and not (NoBH & (sat in bvir)):
                t+=1
                if svir[sat]['Quenched']: q+=1
        if t>0:
            rvx.append(rvir[mw]['Closest_MW+'][0]/1e3)
            w = rvir[mw]['Mstar']/sw if Weight else 1
            rvy.append(q/t*w)
            rvn.append(t)
            rvi.append(mw)
    
    #Upper hemispheres; 300kpc
    for mw in r300:
        t,q = 0,0
        for sat in r300[mw]['Satellites']:
            if s300[sat]['Mstar']>1e8 and not (NoBH & (sat in b300)):
                t+=1
                if s300[sat]['Quenched']: q+=1
        if t>0:
            r3x.append(r300[mw]['Closest_MW+'][0]/1e3)
            w = r300[mw]['Mstar']/sw if Weight else 1
            r3y.append(q/t*w)
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
    ax.legend(loc='lower left',prop={'size':14.4},ncol=4)
    f.savefig(f'Data/QuenchedFractionComp{app}{appw}.{i}.png',bbox_inches='tight',pad_inches=.1)





    rad = np.linspace(0,1,num=11)
    xv,yv,x3,y3 = [[],[],[],[]]
    for r in np.arange(len(rad)-1):
        t,q = 0,0
        for h in svir:
            if svir[h]['Mstar']>1e8 and rad[r]<svir[h]['Orbit'][1]<rad[r+1]:
                t+=1
                if svir[h]['Quenched']: q+=1
        ynew = np.nan if t==0 else q/t
        yv.append(ynew)
        xv.append((rad[r+1]-rad[r])/2+rad[r])
        t,q = 0,0
        for h in s300:
            if s300[h]['Mstar']>1e8 and rad[r]<s300[h]['Orbit'][0]/300<rad[r+1]:
                t+=1
                if s300[h]['Quenched']: q+=1
        ynew = np.nan if t==0 else q/t
        y3.append(ynew)
        x3.append((rad[r+1]-rad[r])/2+rad[r])

    f,ax=plt.subplots(1,1)
    ax.set_xlabel(r'Orbital Distance [R$_{vir}$]',fontsize=20)
    ax.set_ylabel('Quenched Fraction',fontsize=20)
    ax.set_ylim([0,1.05])
    ax.set_xlim([0,1])
    ax.tick_params(which='major',labelsize=15,direction='in', length=5, width=1,top=True)
    ax.tick_params(which='minor',labelsize=5,direction='in', length=3, width=1,top=True)
    ax.plot(x3,y3,c='r',label='300 kpc')
    ax.plot(xv,yv,c='k',label=r'R$_{vir}$')
    ax.plot([0,1],[.5,.5],c='k',linestyle=':',linewidth=.7)
    ax.plot([0,1],[1,1],c='k',linestyle=':',linewidth=.7)
    ax.legend(loc='upper right',prop={'size':15})
    f.savefig(f'Data/QuenchedFractionVsOrbitComp.{i}.png',bbox_inches='tight',pad_inches=.1)