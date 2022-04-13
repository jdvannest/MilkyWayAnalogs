import pickle
import numpy as np
import matplotlib.pylab as plt

M1 = pickle.load(open('../DataFiles/MilkyWay.1.sim.pickle','rb'))
M2 = pickle.load(open('../DataFiles/MilkyWay.2.sim.pickle','rb'))

ms1,ms2,mv1,mv2 = [[],[],[],[]]

for mw in M1:
    ms1.append(np.log10(M1[mw]['Mstar']))
    mv1.append(np.log10(M1[mw]['Mvir']))
for mw in M2:
    ms2.append(np.log10(M2[mw]['Mstar']))
    mv2.append(np.log10(M2[mw]['Mvir']))

f,ax = plt.subplots(1,1,figsize=(6,6))
ax.set_xlim([10,13])
ax.set_ylim([8.8,11.2])
ax.plot([10,13],[10,10],c='r',linestyle='--',alpha=.5)
ax.plot([10,13],[11,11],c='r',linestyle='--',alpha=.5)
ax.axvline(11.5,c='k',linestyle='--',alpha=.5)
ax.axvline(12.6,c='k',linestyle='--',alpha=.5)
ax.set_xlabel(r'Log(M$_{vir}$)',fontsize=15)
ax.set_ylabel(r'Log(M$_*$)',fontsize=15)
ax.scatter(mv2,ms2,c='r',s=7**2,linewidth=.5,marker='x',label=r'M$_K$')
ax.scatter(mv1,ms1,c='k',s=9**2,linewidth=.5,marker='+',label=r'M$_{vir}$')
ax.legend(loc='upper left',prop={'size':15})
f.savefig('Data/DefComp.png',bbox_inches='tight',pad_inches=.1)