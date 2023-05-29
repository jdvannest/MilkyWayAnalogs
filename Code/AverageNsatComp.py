import pickle
import numpy as np 
import matplotlib as mpl
import matplotlib.pylab as plt
from matplotlib.markers import MarkerStyle

magcut = True
appm = '.MagCut' if magcut else ''
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
    ax.set_ylabel(r'Average N$_sat$',fontsize=25)
    ax.set_xlabel(r'D$_{MW+}$ [Mpc]',fontsize=25)
    ax.tick_params(labelsize=20)
    ax.set_xlim([2e-1,5])
    ax.set_ylim([0,3.2])
    ax.semilogx()
    ax.axvline(.767,linestyle='--',label='MW - M31',color='.5',zorder=0)
    ax.axvline(1,color='.5',zorder=0)
    ax.text(.925,1,'Pairs',rotation='vertical',horizontalalignment='center',verticalalignment='center',color='.5',fontsize=18)
    ax.text(1.12,1,'Isolated',rotation='vertical',horizontalalignment='center',verticalalignment='center',color='.5',fontsize=18)

    rbins = np.logspace(np.log10(2e-1),np.log10(5),6)
    rvx,rvy,r3x,r3y = [],[],[],[]
    #Lower hemispheres; Rvir
    for j in np.arange(len(rbins)-1):
        current = []
        for mw in rvir:
            if rbins[j]<rvir[mw]['Closest_MW+'][0]/1e3<rbins[j+1]:
                if magcut:
                    t = 0
                    for sat in rvir[mw]['Satellites']:
                        if SB[sat]['Mueff,r']<25: t+=1
                    current.append(t)
                else:
                    current.append(len(rvir[mw]['Satellites']))
        rvx.append((rbins[j+1]+rbins[j])/2)
        rvy.append(np.mean(current))

    #Upper hemispheres; Rvir
    for j in np.arange(len(rbins)-1):
        current = []
        for mw in r300:
            if rbins[j]<r300[mw]['Closest_MW+'][0]/1e3<rbins[j+1]:
                if magcut:
                    t = 0
                    for sat in r300[mw]['Satellites']:
                        if SB[sat]['Mueff,r']<25: t+=1
                    current.append(t)
                else:
                    current.append(len(r300[mw]['Satellites']))
        r3x.append((rbins[j+1]+rbins[j])/2)
        r3y.append(np.mean(current))    

    x,up,dn = [],[],[]
    for j in np.arange(len(rbins)-1):
        x.append((rbins[j+1]+rbins[j])/2)
        up.append(max([rvy[j],r3y[j]]))
        dn.append(min([rvy[j],r3y[j]]))
    ax.vlines(x,ymin=dn,ymax=up,color='.75',zorder=0)
    
    ax.scatter(r3x,r3y,c='k',marker=MarkerStyle('o', fillstyle='top'),s=10**2,label='300 kpc')
    ax.scatter(rvx,rvy,c='k',marker=MarkerStyle('o', fillstyle='bottom'),s=10**2,label=r'R$_{vir}$')
    #Add medians
    ax.scatter(np.mean(np.array(r3x)[np.where(np.array(r3x)<1)]),np.mean(np.array(r3y)[np.where(np.array(r3x)<1)]),c='r',marker=MarkerStyle('D', fillstyle='top'),s=10**2)
    ax.scatter(np.mean(np.array(r3x)[np.where(np.array(r3x)>1)]),np.mean(np.array(r3y)[np.where(np.array(r3x)>1)]),c='r',marker=MarkerStyle('D', fillstyle='top'),s=10**2)
    ax.scatter(np.mean(np.array(rvx)[np.where(np.array(rvx)<1)]),np.mean(np.array(rvy)[np.where(np.array(rvx)<1)]),c='r',marker=MarkerStyle('D', fillstyle='bottom'),s=10**2)
    ax.scatter(np.mean(np.array(rvx)[np.where(np.array(rvx)>1)]),np.mean(np.array(rvy)[np.where(np.array(rvx)>1)]),c='r',marker=MarkerStyle('D', fillstyle='bottom'),s=10**2)
    ax.vlines(np.mean(np.array(r3x)[np.where(np.array(r3x)<1)]),ymin=min([np.mean(np.array(r3y)[np.where(np.array(r3x)<1)]),np.mean(np.array(rvy)[np.where(np.array(rvx)<1)])]),zorder=0,
                   ymax=max([np.mean(np.array(r3y)[np.where(np.array(r3x)<1)]),np.mean(np.array(rvy)[np.where(np.array(rvx)<1)])]),color='k')
    ax.vlines(np.mean(np.array(r3x)[np.where(np.array(r3x)>1)]),ymin=min([np.mean(np.array(r3y)[np.where(np.array(r3x)>1)]),np.mean(np.array(rvy)[np.where(np.array(rvx)>1)])]),zorder=0,
                   ymax=max([np.mean(np.array(r3y)[np.where(np.array(r3x)>1)]),np.mean(np.array(rvy)[np.where(np.array(rvx)>1)])]),color='k')
    ax.scatter(-1,-1,c='r',marker='D',s=7**2,label='Mean')
    ax.legend(loc='lower left',prop={'size':14.4},ncol=4)
    f.savefig(f'Data/AverageNsatComp{appm}.{i}.png',bbox_inches='tight',pad_inches=.1)