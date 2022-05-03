import pickle
import numpy as np
import matplotlib.pylab as plt
import matplotlib as mpl

M1 = pickle.load(open('../DataFiles/MilkyWay.1.sim.pickle','rb'))
M2 = pickle.load(open('../DataFiles/MilkyWay.2.sim.pickle','rb'))
M3 = pickle.load(open('../DataFiles/MilkyWay.7.300.pickle','rb'))

ms1,ms2,ms3,mv1,mv2,mv3,km1,km2,km3,c = [[],[],[],[],[],[],[],[],[],[]]

for mw in M1:
    ms1.append(np.log10(M1[mw]['Mstar']))
    mv1.append(np.log10(M1[mw]['Mvir']))
    km1.append(M1[mw]['Kmag'])
    #print(f"{mw} : {round(np.log10(M1[mw]['Mstar']),2)} : {round(M1[mw]['Kmag'],2)}")
for mw in M2:
    ms2.append(np.log10(M2[mw]['Mstar']))
    mv2.append(np.log10(M2[mw]['Mvir']))
    km2.append(M2[mw]['Kmag'])
for mw in M3:
    ms3.append(np.log10(M3[mw]['Mstar']))
    mv3.append(np.log10(M3[mw]['Mvir']))
    km3.append(M3[mw]['Kmag'])
    c.append(len(M3[mw]['Satellites']))

fsize = (5.5,9)
lsize = 15

#Opaque overlays
f,ax = plt.subplots(2,1,figsize=fsize)
plt.subplots_adjust(hspace=0)

ax[1].set_ylim([9.3,11.2])
ax[0].set_ylim([11,13])
for i in [0,1]:
    ax[i].set_xlim([-20.75,-25.5])
    ax[i].tick_params(axis='y',direction='inout',length=7)
ax[0].xaxis.set_ticklabels([])
ax[1].tick_params(axis='x',direction='inout',length=7,top=True,labeltop=False)
ax[1].set_yticks(np.arange(9.5,11.25,.25))
ax[0].set_yticks(np.arange(11,13.25,.25))

ax[0].axvline(-23,c='0.75',linestyle='--')
ax[0].axvline(-24.6,c='0.75',linestyle='--')
ax[1].axvline(-23,c='0.75',linestyle='--')
ax[1].axvline(-24.6,c='0.75',linestyle='--')
ax[0].plot([-20.75,-25.5],[11.5,11.5],c='0.75',linestyle='--')
ax[0].plot([-20.75,-25.5],[12.5,12.5],c='0.75',linestyle='--')
ax[1].plot([-20.75,-25.5],[10,10],c='0.75',linestyle='--')
ax[1].plot([-20.75,-25.5],[11,11],c='0.75',linestyle='--')

ax[1].set_xlabel(r'M$_{K}$',fontsize=20)
ax[1].set_ylabel(r'Log(M$_*$)',fontsize=20)
ax[0].set_ylabel(r'Log(M$_{vir}$)',fontsize=20)

#norm = plt.Normalize(0,6)
#p = ax[1].scatter(mv2,ms2,s=7**2,c=c,cmap='viridis',label=r'M$_K$+Env. II')
#cbar = f.colorbar(p,cax=f.add_axes([.91,.11,.03,.77]))
#cbar.set_label(r'N$_{sat}$',fontsize=20)
#cbar.ax.tick_params(labelsize=13)

ax[1].scatter(km1,ms1,c='mediumorchid',alpha=.5,s=7.2**2,label=r'M$_{vir}$, R$_{vir}$')#$10^{11.5}<$Log(M$_{vir}$)$<10^{12.5}$')
ax[1].scatter(km2,ms2,c='limegreen',alpha=.5,s=7.2**2,label=r'M$_*$, R$_{vir}$')#$10^{10}<$Log(M$_{*}$)$<10^{11}$')
ax[1].scatter(km3,ms3,c='gold',alpha=.5,s=7.2**2,label='SAGA II')

ax[0].scatter(km1,mv1,c='mediumorchid',alpha=.5,s=7.2**2,label=r'M$_{vir}$, R$_{vir}$')#$10^{11.5}<$Log(M$_{vir}$)$<10^{12.5}$')
ax[0].scatter(km2,mv2,c='limegreen',alpha=.5,s=7.2**2,label=r'M$_*$, R$_{vir}$')#$10^{10}<$Log(M$_{*}$)$<10^{11}$')
ax[0].scatter(km3,mv3,c='gold',alpha=.5,s=7.2**2,label='SAGA II')

ax[0].legend(loc='upper left',prop={'size':lsize})
f.savefig('Data/DefComp1.png',bbox_inches='tight',pad_inches=.05)


#Concetric circles
f,ax = plt.subplots(2,1,figsize=fsize)
plt.subplots_adjust(hspace=0)

ax[1].set_ylim([9.3,11.2])
ax[0].set_ylim([11,13])
for i in [0,1]:
    ax[i].set_xlim([-20.75,-25.5])
    ax[i].tick_params(axis='y',direction='inout',length=7)
ax[0].xaxis.set_ticklabels([])
ax[1].tick_params(axis='x',direction='inout',length=7,top=True,labeltop=False)
ax[1].set_yticks(np.arange(9.5,11.25,.25))
ax[0].set_yticks(np.arange(11,13.25,.25))

ax[0].axvline(-23,c='0.75',linestyle='--')
ax[0].axvline(-24.6,c='0.75',linestyle='--')
ax[1].axvline(-23,c='0.75',linestyle='--')
ax[1].axvline(-24.6,c='0.75',linestyle='--')
ax[0].plot([-20.75,-25.5],[11.5,11.5],c='0.75',linestyle='--')
ax[0].plot([-20.75,-25.5],[12.5,12.5],c='0.75',linestyle='--')
ax[1].plot([-20.75,-25.5],[10,10],c='0.75',linestyle='--')
ax[1].plot([-20.75,-25.5],[11,11],c='0.75',linestyle='--')

ax[1].set_xlabel(r'M$_{K}$',fontsize=20)
ax[1].set_ylabel(r'Log(M$_*$)',fontsize=20)
ax[0].set_ylabel(r'Log(M$_{vir}$)',fontsize=20)

ax[1].scatter(km3,ms3,c='b',s=3**2,label='SAGA II')
ax[1].scatter(km2,ms2,edgecolor='r',facecolor='None',linewidth=1.5,s=4.5**2,label=r'M$_{*}$, R$_{vir}$')#$10^{10}<$Log(M$_{*}$)$<10^{11}$')
ax[1].scatter(km1,ms1,edgecolor='k',facecolor='None',linewidth=1.5,s=7**2,label=r'M$_{vir}$, R$_{vir}$')#$10^{11.5}<$Log(M$_{vir}$)$<10^{12.5}$')

ax[0].scatter(km3,mv3,c='b',s=3**2,label='SAGA II')
ax[0].scatter(km2,mv2,edgecolor='r',facecolor='None',linewidth=1.5,s=4.5**2,label=r'M$_*$, R$_{vir}$')#$10^{10}<$Log(M$_{*}$)$<10^{11}$')
ax[0].scatter(km1,mv1,edgecolor='k',facecolor='None',linewidth=1.5,s=7**2,label=r'M$_{vir}$, R$_{vir}$')#$10^{11.5}<$Log(M$_{vir}$)$<10^{12.5}$')

ax[0].legend(loc='upper left',prop={'size':lsize})
f.savefig('Data/DefComp2.png',bbox_inches='tight',pad_inches=.05)