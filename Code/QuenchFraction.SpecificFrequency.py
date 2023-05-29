import pickle
import numpy as np
import matplotlib.pylab as plt

def SnQ(Q,Ms):
	#Calculates specific frequency of Quench Fraction normalized to Stellar Mass
	return(Q*10**(.4*(np.log10(Ms) - 10.3)))
def SnQ_E(Q,D):
	#Calculates specific frequency of Quench Fraction normalized to Stellar Mass
	return(Q*10**(.4*(D - 1.5)))
NoBH = False
MagCut = True
app = '.Subset' if NoBH else ''
appm = '.MagCut' if MagCut else ''

f,ax=plt.subplots(1,1,figsize=(6.4,3.8))
ax.set_xlabel(r'Log(M$_*$/M$_\odot$)',fontsize=20)
ax.set_ylabel(r'S$_{f_q,mass}$',fontsize=20)
ax.set_ylim([-.1,2.5])
ax.tick_params(labelsize=15)

x_bins = np.arange(9.4,11.1,.1)
x = x_bins[:-1]+.05
fname,name,c,lw = ['1.sim','2.sim','7.300'],[r'M$_{vir}$, R$_{vir}$',r'M$_*$, R$_{vir}$',r'M$_K$, 300'],['k','r','turquoise'],[4.5,3.75,3]

for i in [0,1,2]:
    M = pickle.load(open(f'../DataFiles/MilkyWay.{fname[i]}.Yov.pickle','rb'))
    S = pickle.load(open(f'../DataFiles/Satellite.{fname[i]}.Yov.pickle','rb'))
    SB = pickle.load(open(f'../DataFiles/SBProfiles.pickle','rb'))
    with open(f'../DataFiles/Satellite.{fname[i]}.Yov.BlackHoles.txt') as fl:
        B = fl.readlines()
        B = [x.rstrip('\n') for x in B]
    y,yu,yl,ye = np.zeros(len(x)),np.zeros(len(x)),np.zeros(len(x)),np.zeros(len(x))
    for j in np.arange(len(x_bins)-1):
        qfs = []
        for mw in M:
            if x_bins[j] < np.log10(M[mw]['Mstar']) < x_bins[j+1]:
                t,q = 0,0
                for sat in M[mw]['Satellites']:
                    if NoBH:
                        BHCheck=True if sat not in B else False
                    else: BHCheck=True
                    if MagCut:
                        MagCheck=True if SB[sat]['Mueff,r']<25 else False
                    else: MagCheck=True
                    if S[sat]['Mstar']>1e8 and BHCheck and MagCheck:
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
f.savefig(f'Data/BinnedSpecificFrequency.QuenchFraction.Mass{app}{appm}.png',bbox_inches='tight',pad_inches=0.1)




f,ax=plt.subplots(1,1,figsize=(6.4,3.8))
ax.set_xlabel(r'D$_{MW+}$ [Mpc]',fontsize=20)
ax.set_ylabel(r'S$_{f_q,env}$',fontsize=20)
ax.set_ylim([-.1,2.5])
ax.set_xlim([0,5])
ax.tick_params(labelsize=15)

x_bins = np.arange(0,11,.5)
minob,obx = 0,[]
for i in [0,1,2]:
    x = x_bins[:-1]+.25
    M = pickle.load(open(f'../DataFiles/MilkyWay.{fname[i]}.Yov.pickle','rb'))
    S = pickle.load(open(f'../DataFiles/Satellite.{fname[i]}.Yov.pickle','rb'))
    SB = pickle.load(open(f'../DataFiles/SBProfiles.pickle','rb'))
    with open(f'../DataFiles/Satellite.{fname[i]}.Yov.BlackHoles.txt') as fl:
        B = fl.readlines()
        B = [x.rstrip('\n') for x in B]
    y,yu,yl,ye = np.zeros(len(x)),np.zeros(len(x)),np.zeros(len(x)),np.zeros(len(x))
    for j in np.arange(len(x_bins)-1):
        qfs = []
        for mw in M:
            if x_bins[j] < M[mw]['Closest_MW+'][0]/1e3 < x_bins[j+1]:
                t,q = 0,0
                for sat in M[mw]['Satellites']:
                    if NoBH:
                        BHCheck=True if sat not in B else False
                    else: BHCheck=True
                    if MagCut:
                        MagCheck=True if SB[sat]['Mueff,r']<25 else False
                    else: MagCheck=True
                    if S[sat]['Mstar']>1e8 and BHCheck and MagCheck:
                        t+=1
                        if S[sat]['Quenched']: q+=1
                if t>0: qfs.append(SnQ_E(q/t,M[mw]['Closest_MW+'][0]/1e3))
        if len(qfs)>0:
            y[j],yu[j],yl[j],ye[j] = np.mean(qfs),np.percentile(qfs,75),np.percentile(qfs,25),np.std(qfs)/np.sqrt(len(qfs))
        else:
            y[j],yu[j],yl[j],ye[j] = np.NaN,np.NaN,np.NaN,np.NaN
    #ax.errorbar(x,y,yerr=[yl,yu],capsize=5,c=c[i],zorder=i)
    for k in np.arange(len(y)):
        if y[k]>2.5:
            if x[k] not in obx: obx.append(x[k])
            ax.text(x[k]+.05,2.4-.2*i,f'{round(y[k],2)}',verticalalignment='center',fontsize=15,color=c[i])
            y[k],x[k] = np.NaN,np.NaN
            minob+=.15
    ax.errorbar(x,y,yerr=ye,capsize=0,c=c[i],zorder=i)
    ax.plot(x,y,c=c[i],marker='.',ms=lw[i]**2,label=name[i],zorder=i)
for d in obx:
    ax.vlines(d,ymin=2.5-minob,ymax=2.5,color='.5',linestyle='--')
ax.legend(loc='upper left',prop={'size':15})
f.savefig(f'Data/BinnedSpecificFrequency.QuenchFraction.Environment{app}{appm}.png',bbox_inches='tight',pad_inches=0.1)


# f,ax=plt.subplots(1,1,figsize=(6.4,3.8))
# ax.set_xlabel(r'Log(M$_{gas}$/M$_\odot$)',fontsize=20)
# ax.set_ylabel(r'S$_{f_q,mass}$',fontsize=20)
# ax.set_ylim([-.1,2.5])
# ax.tick_params(labelsize=15)

# x_bins = np.arange(9,12,.25)
# x = x_bins[:-1]+.125
# fname,name,c,lw = ['1.sim','2.sim','7.300'],[r'M$_{vir}$,R$_{vir}$',r'M$_*$,R$_{vir}$',r'SAGA II'],['k','r','turquoise'],[4.5,3.75,3]

# for i in [0,1,2]:
#     M = pickle.load(open(f'../DataFiles/MilkyWay.{fname[i]}.Yov.pickle','rb'))
#     S = pickle.load(open(f'../DataFiles/Satellite.{fname[i]}.Yov.pickle','rb'))
#     y,yu,yl,ye = np.zeros(len(x)),np.zeros(len(x)),np.zeros(len(x)),np.zeros(len(x))
#     for j in np.arange(len(x_bins)-1):
#         qfs = []
#         for mw in M:
#             if x_bins[j] < np.log10(M[mw]['Mgas']) < x_bins[j+1]:
#                 t,q = 0,0
#                 for sat in M[mw]['Satellites']:
#                     if S[sat]['Mstar']>1e8:
#                         t+=1
#                         if S[sat]['Quenched']: q+=1
#                 if t>0: qfs.append(SnQ(q/t,M[mw]['Mstar']))
#         if len(qfs)>0:
#             y[j],yu[j],yl[j],ye[j] = np.mean(qfs),np.percentile(qfs,75),np.percentile(qfs,25),np.std(qfs)/np.sqrt(len(qfs))
#         else:
#             y[j],yu[j],yl[j],ye[j] = np.NaN,np.NaN,np.NaN,np.NaN
#     #ax.errorbar(x,y,yerr=[yl,yu],capsize=5,c=c[i],zorder=i)
#     ax.errorbar(x,y,yerr=ye,capsize=0,c=c[i],zorder=i)
#     ax.plot(x,y,c=c[i],marker='.',ms=lw[i]**2,label=name[i],zorder=i)

# ax.legend(loc='upper left',prop={'size':15})
# f.savefig('Data/BinnedSpecificFrequency.QuenchFraction.Gas.png',bbox_inches='tight',pad_inches=0.1)


# ## Check if smaller hosts are more susceptible to environment
# mass_limits = [10.2,10.3,10.4,10.5,10.6,10.7,10.8]

# for lim in mass_limits:
#     f,ax=plt.subplots(1,1,figsize=(6.4,3.8))
#     ax.set_xlabel(r'D$_{MW+}$ [Mpc]',fontsize=20)
#     ax.set_ylabel(r'S$_{f_q,env}$',fontsize=20)
#     #ax.set_ylim([-.1,2.5])
#     ax.set_xlim([0,5])
#     ax.tick_params(labelsize=15)

#     x_bins = np.arange(0,11,.5)
#     x = x_bins[:-1]+.25

#     for i in [0,1,2]:
#         M = pickle.load(open(f'../DataFiles/MilkyWay.{fname[i]}.Yov.pickle','rb'))
#         S = pickle.load(open(f'../DataFiles/Satellite.{fname[i]}.Yov.pickle','rb'))
#         y,yu,yl,ye = np.zeros(len(x)),np.zeros(len(x)),np.zeros(len(x)),np.zeros(len(x))
#         for j in np.arange(len(x_bins)-1):
#             qfs = []
#             for mw in M:
#                 if x_bins[j] < M[mw]['Closest_MW+'][0]/1e3 < x_bins[j+1] and np.log10(M[mw]['Mstar'])<lim:
#                     t,q = 0,0
#                     for sat in M[mw]['Satellites']:
#                         if S[sat]['Mstar']>1e8:
#                             t+=1
#                             if S[sat]['Quenched']: q+=1
#                     if t>0: qfs.append(SnQ_E(q/t,M[mw]['Closest_MW+'][0]/1e3))
#             if len(qfs)>0:
#                 y[j],yu[j],yl[j],ye[j] = np.mean(qfs),np.percentile(qfs,75),np.percentile(qfs,25),np.std(qfs)/np.sqrt(len(qfs))
#             else:
#                 y[j],yu[j],yl[j],ye[j] = np.NaN,np.NaN,np.NaN,np.NaN
#         #ax.errorbar(x,y,yerr=[yl,yu],capsize=5,c=c[i],zorder=i)
#         ax.errorbar(x,y,yerr=ye,capsize=0,c=c[i],zorder=i)
#         ax.plot(x,y,c=c[i],marker='.',ms=lw[i]**2,label=name[i],zorder=i)

#     ax.legend(loc='upper left',prop={'size':15})
#     f.savefig(f'Data/BinnedSpecificFrequency.QuenchFraction.Environment.{lim}.png',bbox_inches='tight',pad_inches=0.1)