import pickle
import numpy as np
import matplotlib.pylab as plt


Rk,Rf,Ek,Ef,Sk,Sf = [],[],[],[],[],[]

EH = pickle.load(open('../DataFiles/AdditionalData/ELVES_Hosts.pickle','rb'))
ES = pickle.load(open('../DataFiles/AdditionalData/ELVES_Satellites.pickle','rb'))
for mw in EH:
    Ek.append(EH[mw]['Kmag'])
    f = 0
    for sat in EH[mw]['Satellites']:
        if ES[sat]['Vmag']<-14: f+=ES[sat]['Likelihood']
    Ef.append(f)

SH = pickle.load(open('../Datafiles/AdditionalData/SAGA_Hosts.pickle','rb'))
SS = pickle.load(open('../Datafiles/AdditionalData/SAGA_Satellites.pickle','rb'))
for mw in SH:
    Sk.append(SH[mw]['Kmag'])
    f = 0
    for sat in SH[mw]['Satellites']:
        if SS[sat]['Vmag']<-14: f+=1
    Sf.append(f)

RH = pickle.load(open('../Datafiles/MilkyWay.2.sim.Yov.pickle','rb'))
RS = pickle.load(open('../Datafiles/Satellite.2.sim.Yov.pickle','rb'))
for mw in RH:
    Rk.append(RH[mw]['Kmag'])
    f = 0
    for sat in RH[mw]['Satellites']:
        if RS[sat]['Vmag']<-14: f+=1
    Rf.append(f)

f,ax = plt.subplots(1,1,figsize=(9,3))
ax.set_xlabel(r'Host M$_K$',fontsize=23)
ax.set_ylabel(r'N$_{sat}$ [M$_V<$'+'-14]',fontsize=23)
ax.set_xlim([-21.5,-25.5])
ax.set_ylim([.9,60])
ax.axvline(-23,linestyle='--',c='0.5')

ax.scatter(Rk,Rf,c='k',label='Romulus25')
ax.scatter(Ek,Ef,c='sandybrown',label='ELVES')
ax.scatter(Sk,Sf,c='olivedrab',label='SAGA II')
ax.semilogy()
ax.legend(loc='upper left',prop={'size':15})
f.savefig('Data/FaintHostComparison.png',bbox_inches='tight',pad_inches=.1)