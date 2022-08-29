import pickle
import numpy as np
import matplotlib.pylab as plt

def SnQ(Q,Ms):
	#Calculates specific frequency of Quench Fraction normalized to Stellar Mass
	return(Q*10**((np.log10(Ms) - 10.6)))
def SnQ_E(Q,D):
	#Calculates specific frequency of Quench Fraction normalized to Stellar Mass
	return(Q*10**((D - 5)))

f,ax=plt.subplots(1,1,figsize=(6.4,3.8))
ax.set_xlabel(r'Log(M$_*$/M$_\odot$)',fontsize=20)
ax.set_ylabel(r'S$_{f_q,mass}$',fontsize=20)
ax.set_ylim([-.1,2.5])
ax.tick_params(labelsize=15)

x_bins = np.arange(9.4,11.1,.1)
x = x_bins[:-1]+.05
fname,name,c,lw = ['1.sim','2.sim','7.300'],[r'M$_{vir}$,R$_{vir}$',r'M$_*$,R$_{vir}$',r'SAGA II'],['k','r','turquoise'],[4.5,3.75,3]

for i in [0,1,2]:
    M = pickle.load(open(f'../DataFiles/MilkyWay.{fname[i]}.Yov.pickle','rb'))
    S = pickle.load(open(f'../DataFiles/Satellite.{fname[i]}.Yov.pickle','rb'))
    y,yu,yl,ye = np.zeros(len(x)),np.zeros(len(x)),np.zeros(len(x)),np.zeros(len(x))
    for j in np.arange(len(x_bins)-1):
        qfs = []
        for mw in M:
            if x_bins[j] < np.log10(M[mw]['Mstar']) < x_bins[j+1]:
                t,q = 0,0
                for sat in M[mw]['Satellites']:
                    if S[sat]['Mstar']>1e8:
                        t+=1
                        if S[sat]['Quenched']: q+=1
                if t>0: qfs.append(SnQ(q/t,M[mw]['Mstar']))
        if len(qfs)>0:
            y[j],yu[j],yl[j],ye[j] = np.mean(qfs),np.percentile(qfs,75),np.percentile(qfs,25),np.std(qfs)/np.sqrt(len(qfs))
        else:
            y[j],yu[j],yl[j],ye[j] = np.NaN,np.NaN,np.NaN,np.NaN
    #ax.errorbar(x,y,yerr=[yl,yu],capsize=5,c=c[i],zorder=i)
    ax.errorbar(x,y,yerr=ye,capsize=0,c=c[i],zorder=i)
    ax.plot(x,y,c=c[i],marker='.',ms=lw[i]**2,label=name[i],zorder=i)

ax.legend(loc='upper left',prop={'size':15})
f.savefig('Data/BinnedSpecificFrequency.QuenchFraction.png',bbox_inches='tight',pad_inches=0.1)




f,ax=plt.subplots(1,1,figsize=(6.4,3.8))
ax.set_xlabel(r'D$_{MW+}$ [Mpc]',fontsize=20)
ax.set_ylabel(r'S$_{f_q,env}$',fontsize=20)
ax.set_ylim([-.1,2.5])
ax.set_xlim([0,5])
ax.tick_params(labelsize=15)

x_bins = np.arange(0,11,.5)
x = x_bins[:-1]+.25

for i in [0,1,2]:
    M = pickle.load(open(f'../DataFiles/MilkyWay.{fname[i]}.Yov.pickle','rb'))
    S = pickle.load(open(f'../DataFiles/Satellite.{fname[i]}.Yov.pickle','rb'))
    y,yu,yl,ye = np.zeros(len(x)),np.zeros(len(x)),np.zeros(len(x)),np.zeros(len(x))
    for j in np.arange(len(x_bins)-1):
        qfs = []
        for mw in M:
            if x_bins[j] < M[mw]['Closest_MW+'][0]/1e3 < x_bins[j+1]:
                t,q = 0,0
                for sat in M[mw]['Satellites']:
                    if S[sat]['Mstar']>1e8:
                        t+=1
                        if S[sat]['Quenched']: q+=1
                if t>0: qfs.append(SnQ_E(q/t,M[mw]['Closest_MW+'][0]/1e3))
        if len(qfs)>0:
            y[j],yu[j],yl[j],ye[j] = np.mean(qfs),np.percentile(qfs,75),np.percentile(qfs,25),np.std(qfs)/np.sqrt(len(qfs))
        else:
            y[j],yu[j],yl[j],ye[j] = np.NaN,np.NaN,np.NaN,np.NaN
    #ax.errorbar(x,y,yerr=[yl,yu],capsize=5,c=c[i],zorder=i)
    ax.errorbar(x,y,yerr=ye,capsize=0,c=c[i],zorder=i)
    ax.plot(x,y,c=c[i],marker='.',ms=lw[i]**2,label=name[i],zorder=i)

ax.legend(loc='upper left',prop={'size':15})
f.savefig('Data/BinnedSpecificFrequency.QuenchFraction.Environment.png',bbox_inches='tight',pad_inches=0.1)