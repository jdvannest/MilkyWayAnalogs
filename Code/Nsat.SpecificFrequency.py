import pickle
import numpy as np
import matplotlib.pylab as plt

def SnM(Nsat,Ms):
	#Calculates specific frequency of Nsat normalized to Log(stellar mass)
	return(Nsat*10**((np.log10(Ms) - 10.6)))

def SnD(Nsat,D):
	#Calculates specific frequency of Nsat normalized to distance to large halo [Mpc]
	return(Nsat*10**((D/1000 - 4)))

f,ax=plt.subplots(1,1,figsize=(6.4,3.8))
ax.set_xlabel(r'Log(M$_*$/M$_\odot$)',fontsize=20)
ax.set_ylabel(r'S$_{N,mass}$',fontsize=20)
ax.set_ylim([-.5,15])
#ax.set_xlim([10,11.1])
ax.tick_params(labelsize=15)

x_bins = np.arange(9.25,11.2,.25)
x = x_bins[:-1]+.25/2
fname,name,c,lw = ['1.sim','2.sim','7.300'],[r'M$_{vir}$,R$_{vir}$',r'M$_*$,R$_{vir}$',r'SAGA II'],['k','r','turquoise'],[4.5,3.75,3]

for i in [0,1,2]:
    M = pickle.load(open(f'../DataFiles/MilkyWay.{fname[i]}.Yov.pickle','rb'))
    S = pickle.load(open(f'../DataFiles/Satellite.{fname[i]}.Yov.pickle','rb'))
    y,yu,yl,ye = np.zeros(len(x)),np.zeros(len(x)),np.zeros(len(x)),np.zeros(len(x))
    for j in np.arange(len(x_bins)-1):
        Nsats = []
        for mw in M:
            if x_bins[j] < np.log10(M[mw]['Mstar']) < x_bins[j+1]:
                Nsats.append(SnM(len(M[mw]['Satellites']),M[mw]['Mstar']))
        if len(Nsats)>0:
            y[j],yu[j],yl[j],ye[j] = np.mean(Nsats),np.percentile(Nsats,75),np.percentile(Nsats,25),np.std(Nsats)/np.sqrt(len(Nsats))
        else:
            y[j],yu[j],yl[j],ye[j] = np.NaN,np.NaN,np.NaN,np.NaN
    #ax.errorbar(x,y,yerr=[yl,yu],capsize=5,c=c[i],zorder=i)
    ax.errorbar(x,y,yerr=ye,capsize=0,c=c[i],zorder=i)
    ax.plot(x,y,c=c[i],marker='.',ms=lw[i]**2,label=name[i],zorder=i)

ax.legend(loc='upper left',prop={'size':15})
f.savefig('Data/BinnedSpecificFrequency.NsatMass.png',bbox_inches='tight',pad_inches=0.1)

f,ax=plt.subplots(1,1,figsize=(6.4,3.8))
ax.set_xlabel(r'D$_{MW+}$ [Mpc]',fontsize=20)
ax.set_ylabel(r'S$_{N,env}$',fontsize=20)
ax.set_ylim([-.5,15])
ax.set_xlim([0,8])
ax.tick_params(labelsize=15)

x_bins = np.arange(0,9,1)
x = x_bins[:-1]+.5
minob = 0
for i in [0,1,2]:
    M = pickle.load(open(f'../DataFiles/MilkyWay.{fname[i]}.Yov.pickle','rb'))
    S = pickle.load(open(f'../DataFiles/Satellite.{fname[i]}.Yov.pickle','rb'))
    #y,yu,yl,ye = np.zeros(len(x)),np.zeros(len(x)),np.zeros(len(x)),np.zeros(len(x))
    x = []
    y,yu,yl,ye = [],[],[],[]
    for j in np.arange(len(x_bins)-1):
        Nsats = []
        for mw in M:
            if x_bins[j] < M[mw]['Closest_MW+'][0]/1e3 < x_bins[j+1]:
                Nsats.append(SnD(len(M[mw]['Satellites']),M[mw]['Closest_MW+'][0]))
        if len(Nsats)>0:
            #y[j],yu[j],yl[j],ye[j] = np.mean(Nsats),np.percentile(Nsats,75),np.percentile(Nsats,25),np.std(Nsats)/np.sqrt(len(Nsats))
            x.append(np.mean(x_bins[j:j+2]))
            y.append(np.mean(Nsats))
            yu.append(np.percentile(Nsats,75))
            yl.append(np.percentile(Nsats,25))
            ye.append(np.std(Nsats)/np.sqrt(len(Nsats)))
        #else:
            #y[j],yu[j],yl[j],ye[j] = np.NaN,np.NaN,np.NaN,np.NaN
    #ax.errorbar(x,y,yerr=[yl,yu],capsize=5,c=c[i],zorder=i)
    for k in np.arange(len(y)):
        if y[k]>15:
            ax.text(x[k]+.15,14-i,f'{round(y[k],2)}',verticalalignment='center',fontsize=15,color=c[i])
            y[k],x[k] = np.NaN,np.NaN
            minob+=1
    ax.errorbar(x,y,yerr=ye,capsize=0,c=c[i],zorder=i)
    ax.plot(x,y,c=c[i],marker='.',ms=lw[i]**2,label=name[i],zorder=i)
ax.vlines(6.5,ymin=15-minob,ymax=15,color='.5',linestyle='--')
ax.legend(loc='upper left',prop={'size':15})
f.savefig('Data/BinnedSpecificFrequency.NsatEnvironment.png',bbox_inches='tight',pad_inches=0.1)