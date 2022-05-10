import pickle
import numpy as np
import matplotlib.pylab as plt

def SnQ(Q,Ms):
	#Calculates specific frequency of Quench Fraction normalized to Stellar Mass
	return(Q*10**((np.log10(Ms) - 10.6)))

f,ax=plt.subplots(1,1,figsize=(8,6))
ax.set_xlabel(r'Log(M$_*$/M$_\odot$)',fontsize=15)
ax.set_ylabel(r'S$_{f_q,mass}$',fontsize=15) 

x_bins = np.arange(9.4,11.1,.1)
x = x_bins[:-1]+.05
fname,name,c = ['1.sim','2.sim','7.300'],[r'M$_{vir}$',r'M$_*$',r'SAGA II'],['k','r','b']

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
    ax.errorbar(x,y,yerr=ye,capsize=5,c=c[i],zorder=i)
    ax.plot(x,y,c=c[i],marker='.',ms=3**2,label=name[i],zorder=i)

ax.legend(loc='upper left',prop={'size':15})
f.savefig('Data/BinnedSpecificFrequency.QuenchFraction.png',bbox_inches='tight',pad_inches=0.1)