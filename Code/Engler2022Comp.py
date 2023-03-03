## Figure 3(d) from Engler2022 (https://arxiv.org/pdf/2211.00010.pdf)

import pickle
import numpy as np
import matplotlib.pylab as plt

Sats = pickle.load(open('../Datafiles/Satellite.2.sim.Yov.pickle','rb'))
Host = pickle.load(open('../Datafiles/MilkyWay.2.sim.Yov.pickle','rb'))

bins = np.linspace(7,10.6,7)
qnp,qfp,qni,qfi = [],[],[],[]

for mw in Host:
    if Host[mw]['Closest_MW+'][0]/1e3<1:
        for s in Host[mw]['Satellites']:
            if Sats[s]['Orbit'][0]<300: qnp.append(s)
            else: qfp.append(s)
    else:
        for s in Host[mw]['Satellites']:
            if Sats[s]['Orbit'][0]<300: qni.append(s)
            else: qfi.append(s)

dnp,dfp,dni,dfi = [],[],[],[]
qlist,dlist = [qnp,qfp,qni,qfi],[dnp,dfp,dni,dfi]

for x in [0,1,2,3]:
    for i in np.arange(len(bins)-1):
        q,t = 0,0
        for s in qlist[x]:
            if bins[i] < np.log10(Sats[s]['Mstar']) < bins[i+1]:
                t+=1
                if Sats[s]['Quenched']: q+=1
        if t>0: dlist[x].append(q/t)
        else: dlist[x].append(np.NaN)

f,ax=plt.subplots(1,1,figsize=(5,5))
ax.set_ylim([0,1])
ax.set_xlim([6.7,10.3])
ax.set_xticks([7,8,9,10])
ax.set_xlabel(r'Log[M$_*$/M$_\odot$]',fontsize=15)
ax.set_ylabel('Quenched Fraction',fontsize=15)

ax.plot(bins[:-1],dnp,c='r')
ax.plot(bins[:-1],dni,c='b')
ax.plot(bins[:-1],dfp,c='r',linestyle='--')
ax.plot(bins[:-1],dfi,c='b',linestyle='--')

f.savefig('Data/EnglerComp.png',bbox_inches='tight',pad_inches=.1)