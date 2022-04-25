import pickle
import numpy as np
import matplotlib.pylab as plt
import matplotlib as mpl

M1 = pickle.load(open('../DataFiles/MilkyWay.1.sim.pickle','rb'))
M2 = pickle.load(open('../DataFiles/MilkyWay.4.300.pickle','rb'))

ms1,ms2,c,mv1,mv2 = [[],[],[],[],[]]

for mw in M1:
    ms1.append(np.log10(M1[mw]['Mstar']))
    mv1.append(np.log10(M1[mw]['Mvir']))
for mw in M2:
    ms2.append(np.log10(M2[mw]['Mstar']))
    mv2.append(np.log10(M2[mw]['Mvir']))
    c.append(len(M2[mw]['Satellites']))

f,ax = plt.subplots(1,1,figsize=(6,6))
ax.set_xlim([10,13])
ax.set_ylim([9.4,11.2])#[8.8,11.2])
ax.plot([10,13],[10,10],c='k',linestyle='--',alpha=.5)
ax.plot([10,13],[11,11],c='k',linestyle='--',alpha=.5)
ax.axvline(11.5,c='k',linestyle='--',alpha=.5)
ax.axvline(12.5,c='k',linestyle='--',alpha=.5)
ax.set_xlabel(r'Log(M$_{vir}$)',fontsize=20)
ax.set_ylabel(r'Log(M$_*$)',fontsize=20)
ax.tick_params(labelsize=13)

norm = plt.Normalize(0,6)
p = ax.scatter(mv2,ms2,s=7**2,c=c,cmap='viridis',label=r'M$_K$+Env. II')
cbar = f.colorbar(p,cax=f.add_axes([.91,.11,.03,.77]))
cbar.set_label(r'N$_{sat}$',fontsize=20)
cbar.ax.tick_params(labelsize=13)
ax.scatter(mv1,ms1,facecolor='None',edgecolor='r',s=7.2**2,label=r'M$_{vir}$')
ax.legend(loc='upper left',prop={'size':15})
f.savefig('Data/DefComp.png',bbox_inches='tight',pad_inches=.1)